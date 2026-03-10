# ==========================================================
# MTSE Cost Engine - Industrial Estimation Layer
# ==========================================================

import streamlit as st
import json
import google.generativeai as genai

class CostEngine:
    """
    Handles BOQ extraction and complex project cost estimation.
    """
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        self.model = genai.GenerativeModel("gemini-1.5-flash")

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
        candidates = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        last_err = "Unknown"
        
        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                txt = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(txt)
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
                "item": item.get("item"),
                "qty": qty,
                "unit": item.get("unit"),
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
