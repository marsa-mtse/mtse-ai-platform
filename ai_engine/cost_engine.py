# ==========================================================
# MTSE Cost Engine - Industrial Estimation Layer
# ==========================================================

import streamlit as st
import json
import google.generativeai as genai
from utils import t

class CostEngine:
    """
    Handles BOQ extraction and complex project cost estimation.
    """
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def normalize_boq_data(self, data):
        """Normalizes keys from AI output (handles Arabic/vague keys)."""
        if not isinstance(data, list):
            return data
            
        mapping = {
            "item": ["item", "البند", "بند", "الوصف", "description", "name", "الأداة"],
            "unit": ["unit", "الوحدة", "وحدة", "measurement"],
            "quantity": ["quantity", "الكمية", "كمية", "qty", "count", "العدد"]
        }
        
        normalized = []
        for entry in data:
            if not isinstance(entry, dict):
                continue
            
            new_entry = {}
            # Map standard keys
            for std_key, aliases in mapping.items():
                # Find matching key in entry
                found = False
                for k in entry.keys():
                    if k.lower() in [a.lower() for a in aliases]:
                        new_entry[std_key] = entry[k]
                        found = True
                        break
                if not found:
                    new_entry[std_key] = entry.get(std_key, "" if std_key != "quantity" else 0)
            
            # Clean quantity
            try:
                if isinstance(new_entry["quantity"], str):
                    import re
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", new_entry["quantity"])
                    new_entry["quantity"] = float(nums[0]) if nums else 0.0
                else:
                    new_entry["quantity"] = float(new_entry["quantity"] or 0)
            except:
                new_entry["quantity"] = 0.0
                
            normalized.append(new_entry)
        return normalized

    def extract_boq_from_file(self, file_bytes, file_type):
        """Extracts BOQ data from uploaded files (PDF/Image) using multimodal AI."""
        # For Excel, we might want to handle it locally, but for PDF/Images, we use Multimodal
        prompt = """
        Act as a Professional Quantity Surveyor.
        Analyze the provided document (PDF/Excel/Image) and extract all line items.
        
        Output only a JSON list of objects:
        [
            {"item": "اسم البند", "unit": "الوحدة", "quantity": 10.5},
            ...
        ]
        """
        
        candidates = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash']
        last_err = "Unknown"
        
        # Prepare content parts
        import io
        if "pdf" in file_type.lower():
            content_parts = [prompt, {"mime_type": "application/pdf", "data": file_bytes}]
        elif "excel" in file_type.lower() or "spreadsheet" in file_type.lower() or "xlsx" in file_type.lower():
            # Gemini 1.5 supports XLSX
            content_parts = [prompt, {"mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": file_bytes}]
        elif "image" in file_type.lower() or file_type in ["png", "jpg", "jpeg"]:
            from PIL import Image
            img = Image.open(io.BytesIO(file_bytes))
            content_parts = [prompt, img]
        else:
            # Try as raw data with a guess or generic mime
            content_parts = [prompt, {"mime_type": file_type, "data": file_bytes}]

        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(content_parts)
                txt = response.text.replace("```json", "").replace("```", "").strip()
                
                start = txt.find("[")
                end = txt.rfind("]")
                if start != -1 and end != -1:
                    raw_data = json.loads(txt[start:end+1])
                    return self.normalize_boq_data(raw_data)
                raw_data = json.loads(txt)
                return self.normalize_boq_data(raw_data)
            except Exception as e:
                last_err = str(e)
                continue
                
        return [{"error": f"Failed after rotation: {last_err}"}]

    def extract_boq_items(self, content):
        """Extracts Item, Unit, Quantity with model rotation."""
        prompt = f"""
        Act as a Professional Quantity Surveyor.
        Extract all line items from the following Bill of Quantities (BOQ).
        
        Content:
        {content[:5000]}
        
        Output only a JSON list of objects:
        [
            {{"item": "اسم البند", "unit": "الوحدة", "quantity": 10.5}},
            ...
        ]
        """
        candidates = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash']
        last_err = "Unknown"
        
        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                txt = response.text.replace("```json", "").replace("```", "").strip()
                
                # Robust extraction
                start = txt.find("[")
                end = txt.rfind("]")
                if start != -1 and end != -1:
                    raw_data = json.loads(txt[start:end+1])
                    return self.normalize_boq_data(raw_data)
                raw_data = json.loads(txt)
                return self.normalize_boq_data(raw_data)
            except Exception as e:
                last_err = str(e)
                if "429" in last_err or "404" in last_err or "Quota" in last_err:
                    continue
                break
        return [{"error": f"Failed after rotation: {last_err}"}]

    def calculate_cost_matrix(self, items, base_prices, overhead=0.15, waste=0.05, profit=0.20):
        """
        Calculates a full cost matrix based on user inputs and scenarios.
        """
        full_estimate = []
        total_direct = 0
        
        for i, item in enumerate(items):
            qty = item.get("quantity", 0)
            base_price = base_prices.get(str(i), 0)
            
            direct_cost = qty * base_price
            total_direct += direct_cost
            
            # Scenario calculations
            full_estimate.append({
                "item": item.get("item", t("بدون اسم", "Unnamed")),
                "qty": qty,
                "unit": item.get("unit", "-"),
                "base_price": base_price,
                "direct_total": direct_cost,
                "with_waste": direct_cost * (1 + waste),
                "with_overhead": direct_cost * (1 + waste + overhead),
                "final_price": direct_cost * (1 + waste + overhead + profit)
            })
            
        return {
            "items": full_estimate,
            "summary": {
                "total_direct": total_direct,
                "total_with_waste": total_direct * (1 + waste),
                "total_grand": total_direct * (1 + waste + overhead + profit)
            }
        }

def get_cost_engine():
    return CostEngine()
