# ==========================================================
# MTSE Cost Engine - Industrial Estimation Layer
# ==========================================================

import streamlit as st
import json
import re
from utils import t

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import groq as groq_lib
except ImportError:
    groq_lib = None


def _parse_json_list(txt):
    """Helper to robustly extract a JSON list from AI text."""
    txt = txt.replace("```json", "").replace("```", "").strip()
    start = txt.find("[")
    end = txt.rfind("]")
    if start != -1 and end != -1:
        return json.loads(txt[start:end+1])
    return json.loads(txt)


class CostEngine:
    """
    Handles BOQ extraction and complex project cost estimation.
    Tries Groq first (reliable), then Gemini as fallback.
    """
    def __init__(self):
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if google_key and genai:
            genai.configure(api_key=google_key.strip())

    def normalize_boq_data(self, data):
        """Normalizes keys from AI output (handles Arabic/English/vague keys)."""
        if not isinstance(data, list):
            return data

        mapping = {
            "item": ["item", "البند", "بند", "الوصف", "description", "name", "الاسم"],
            "unit": ["unit", "الوحدة", "وحدة", "measurement"],
            "quantity": ["quantity", "الكمية", "كمية", "qty", "count", "العدد"]
        }

        normalized = []
        for entry in data:
            if not isinstance(entry, dict):
                continue

            new_entry = {}
            for std_key, aliases in mapping.items():
                found = False
                for k in entry.keys():
                    if k.lower() in [a.lower() for a in aliases]:
                        new_entry[std_key] = entry[k]
                        found = True
                        break
                if not found:
                    new_entry[std_key] = entry.get(std_key, "" if std_key != "quantity" else 0)

            try:
                if isinstance(new_entry["quantity"], str):
                    nums = re.findall(r"[-+]?\d*\.\d+|\d+", new_entry["quantity"])
                    new_entry["quantity"] = float(nums[0]) if nums else 0.0
                else:
                    new_entry["quantity"] = float(new_entry["quantity"] or 0)
            except:
                new_entry["quantity"] = 0.0

            normalized.append(new_entry)
        return normalized

    def _call_groq(self, prompt_text):
        """Call Groq API for text-only BOQ extraction."""
        groq_key = st.secrets.get("GROQ_API_KEY")
        if not groq_key or not groq_lib:
            return None

        try:
            client = groq_lib.Groq(api_key=groq_key.strip())
            for model_name in ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt_text}],
                        response_format={"type": "json_object"}
                    )
                    raw = json.loads(response.choices[0].message.content)
                    # Handle Groq wrapping the list in a dict key
                    if isinstance(raw, list):
                        return raw
                    for key in ["items", "boq", "line_items", "data", "بنود", "المقايسة"]:
                        if key in raw and isinstance(raw[key], list):
                            return raw[key]
                    return raw
                except Exception as e:
                    if "429" in str(e) or "decommissioned" in str(e):
                        continue
                    raise e
        except Exception:
            return None
        return None

    def _call_gemini_text(self, prompt_text):
        """Call Gemini API for text-only BOQ extraction."""
        if not genai:
            return None
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if not google_key:
            return None

        for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt_text)
                return _parse_json_list(response.text)
            except Exception as e:
                if "404" in str(e) or "429" in str(e):
                    continue
                break
        return None

    def extract_boq_items(self, content):
        """Extracts BOQ items from pasted text — tries Groq first, then Gemini."""
        prompt = f"""You are a Professional Quantity Surveyor.
Extract all line items from this Bill of Quantities (BOQ) text.

Content:
{content[:5000]}

IMPORTANT: Output ONLY a JSON object with key "items" containing a list.
Each item must have EXACTLY these keys: "item", "unit", "quantity".
Example: {{"items": [{{"item": "Concrete", "unit": "m3", "quantity": 50.0}}]}}
"""
        # 1. Try Groq first (working for this user)
        result = self._call_groq(prompt)
        if result and isinstance(result, list) and len(result) > 0:
            return self.normalize_boq_data(result)

        # 2. Try Gemini as fallback
        result = self._call_gemini_text(prompt)
        if result and isinstance(result, list) and len(result) > 0:
            return self.normalize_boq_data(result)

        return [{"error": "فشل الاستخراج. تأكد من مفاتيح GROQ_API_KEY أو GOOGLE_API_KEY في الإعدادات."}]

    def extract_boq_from_file(self, file_bytes, file_type):
        """Extracts BOQ from uploaded files using Gemini multimodal (PDF/Image).
        Note: Groq is text-only, so files require Gemini.
        """
        google_key = st.secrets.get("GOOGLE_API_KEY")

        if not google_key or not genai:
            return [{"error": "رفع الملفات يتطلب مفتاح GOOGLE_API_KEY مع دعم Gemini. الرجاء لصق محتوى الملف في حقل النص."}]

        import io
        prompt = """You are a Professional Quantity Surveyor.
Analyze this document and extract all BOQ line items.
Output ONLY a JSON list: [{"item": "...", "unit": "...", "quantity": 0.0}]
"""
        if "pdf" in file_type.lower():
            content_parts = [prompt, {"mime_type": "application/pdf", "data": file_bytes}]
        elif "excel" in file_type.lower() or "spreadsheet" in file_type.lower():
            content_parts = [prompt, {"mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": file_bytes}]
        elif "image" in file_type.lower():
            from PIL import Image
            img = Image.open(io.BytesIO(file_bytes))
            content_parts = [prompt, img]
        else:
            content_parts = [prompt, {"mime_type": file_type, "data": file_bytes}]

        for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(content_parts)
                raw = _parse_json_list(response.text)
                return self.normalize_boq_data(raw)
            except Exception as e:
                if "404" in str(e) or "429" in str(e):
                    continue
                break

        return [{"error": "رفع الملف لا يعمل مع مفتاح Gemini الحالي. الرجاء نسخ محتوى المقايسة ولصقه في حقل النص."}]

    def calculate_cost_matrix(self, items, base_prices, overhead=0.15, waste=0.05, profit=0.20):
        """Calculates full cost matrix with overhead, waste, and profit scenarios."""
        full_estimate = []
        total_direct = 0

        for i, item in enumerate(items):
            qty = item.get("quantity", 0)
            base_price = base_prices.get(str(i), 0)

            direct_cost = qty * base_price
            total_direct += direct_cost

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
