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
    # Try to find a list first
    start = txt.find("[")
    end = txt.rfind("]")
    if start != -1 and end != -1:
        return json.loads(txt[start:end+1])
    # Try to find an object
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1:
        return json.loads(txt[start:end+1])
    return json.loads(txt)


class CostEngine:
    """
    Handles BOQ extraction and complex project cost estimation.
    Tries Groq first (reliable for this user), then Gemini as fallback.
    """
    def __init__(self):
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if google_key and genai:
            genai.configure(api_key=google_key.strip())

    def normalize_boq_data(self, data):
        """Normalizes keys from AI output (handles Arabic/English/vague keys)."""
        # If input is a dict (Groq wraps lists in objects), unwrap it first
        if isinstance(data, dict):
            for key in ["items", "boq", "line_items", "data", "بنود", "المقايسة", "list"]:
                if key in data and isinstance(data[key], list):
                    data = data[key]
                    break
            else:
                # If still a dict, can't normalize
                return [{"error": f"شكل البيانات غير متوقع: {list(data.keys())}"}]

        if not isinstance(data, list):
            return [{"error": f"البيانات المُعادة ليست قائمة: {type(data)}"}]

        mapping = {
            "item": ["item", "البند", "بند", "الوصف", "description", "name", "الاسم", "وصف_البند", "item_description"],
            "unit": ["unit", "الوحدة", "وحدة", "measurement", "وحدة_القياس"],
            "quantity": ["quantity", "الكمية", "كمية", "qty", "count", "العدد", "الكميه"]
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

        if not normalized:
            return [{"error": "لم يتم العثور على بنود في الاستجابة. حاول مرة أخرى أو تحقق من البيانات."}]
        return normalized

    def _call_groq(self, prompt_text):
        """Call Groq API for text BOQ extraction. Returns raw parsed data or None."""
        groq_key = st.secrets.get("GROQ_API_KEY")
        if not groq_key:
            return None, "لا يوجد GROQ_API_KEY"
        if not groq_lib:
            return None, "مكتبة groq غير مثبتة"

        last_err = "Unknown"
        try:
            client = groq_lib.Groq(api_key=groq_key.strip())
            for model_name in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt_text}],
                        max_tokens=4096,
                        temperature=0.1,
                    )
                    raw_text = response.choices[0].message.content
                    parsed = _parse_json_list(raw_text)
                    return parsed, None
                except Exception as e:
                    last_err = str(e)
                    if "429" in last_err or "decommissioned" in last_err or "model" in last_err.lower():
                        continue
                    break
        except Exception as e:
            return None, f"Groq error: {str(e)}"
        return None, f"Groq فشل في كل النماذج: {last_err}"

    def _call_gemini_text(self, prompt_text):
        """Call Gemini API for text BOQ extraction."""
        if not genai:
            return None, "google-generativeai غير مثبتة"
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if not google_key:
            return None, "لا يوجد GOOGLE_API_KEY"

        last_err = "Unknown"
        for model_name in ["gemini-2.0-flash", "gemini-1.5-flash"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt_text)
                parsed = _parse_json_list(response.text)
                return parsed, None
            except Exception as e:
                last_err = str(e)
                if "404" in last_err or "429" in last_err:
                    continue
                break
        return None, f"Gemini فشل: {last_err}"

    def extract_boq_items(self, content):
        """Extracts BOQ items from pasted text — tries Groq first, then Gemini."""
        prompt = f"""You are a Professional Quantity Surveyor.
Extract all line items from this Bill of Quantities (BOQ) text.

Content:
{content[:5000]}

Return a JSON array of objects. Each object must have:
- "item": string (item/work description)
- "unit": string (unit of measurement: m2, m3, kg, etc.)  
- "quantity": number

Example output:
[
  {{"item": "Concrete C25", "unit": "m3", "quantity": 50.5}},
  {{"item": "Reinforcement steel", "unit": "ton", "quantity": 3.2}}
]

Return ONLY the JSON array, no other text.
"""
        errors = []

        # 1. Try Groq first
        result, err = self._call_groq(prompt)
        if result is not None:
            normalized = self.normalize_boq_data(result)
            if normalized and "error" not in normalized[0]:
                return normalized
            errors.append(f"Groq normalization: {normalized[0].get('error', '')}")
        else:
            errors.append(f"Groq: {err}")

        # 2. Try Gemini as fallback
        result, err = self._call_gemini_text(prompt)
        if result is not None:
            normalized = self.normalize_boq_data(result)
            if normalized and "error" not in normalized[0]:
                return normalized
            errors.append(f"Gemini normalization: {normalized[0].get('error', '')}")
        else:
            errors.append(f"Gemini: {err}")

        return [{"error": " | ".join(errors)}]

    def _file_to_text(self, file_bytes, file_type):
        """Convert uploaded file to plain text for Groq processing."""
        import io

        # --- Excel ---
        if "excel" in file_type.lower() or "spreadsheet" in file_type.lower() or "xlsx" in file_type.lower():
            try:
                import openpyxl
                wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
                lines = []
                for sheet in wb.worksheets:
                    lines.append(f"=== Sheet: {sheet.title} ===")
                    for row in sheet.iter_rows(values_only=True):
                        row_str = "\t".join([str(c) if c is not None else "" for c in row])
                        if row_str.strip():
                            lines.append(row_str)
                return "\n".join(lines)
            except Exception as e:
                return None, f"خطأ في قراءة Excel: {str(e)}"

        # --- PDF ---
        if "pdf" in file_type.lower():
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                pages = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)
                extracted = "\n".join(pages)
                if not extracted.strip():
                    return None, "لم يتم استخراج نص من PDF. قد يكون الملف صورة ممسوحة ضوئياً."
                return extracted, None
            except Exception as e:
                return None, f"خطأ في قراءة PDF: {str(e)}"

        return None, f"نوع الملف غير مدعوم: {file_type}"

    def extract_boq_from_file(self, file_bytes, file_type):
        """Extracts BOQ from uploaded files by converting to text, then using Groq."""
        # Step 1: Convert file to text
        result = self._file_to_text(file_bytes, file_type)
        if isinstance(result, tuple):
            text_content, err = result
        else:
            text_content, err = result, None

        if not text_content:
            return [{"error": err or "فشل تحويل الملف إلى نص."}]

        # Step 2: Extract BOQ from text using Groq
        return self.extract_boq_items(text_content)


    def calculate_cost_matrix(self, items, base_prices, overhead=0.15, waste=0.05, profit=0.20):
        """Calculates full cost matrix with overhead, waste, and profit scenarios."""
        full_estimate = []
        total_direct = 0

        for i, item in enumerate(items):
            qty = float(item.get("quantity", 0) or 0)
            base_price = float(base_prices.get(str(i), 0) or 0)

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
