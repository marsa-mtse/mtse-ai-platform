# ==========================================
# AI Campaign Orchestrator - Enterprise Core
# ==========================================
import streamlit as st
import json
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Dict

class VisualPromptModel(BaseModel):
    platform: str
    prompt: str
    concept: str

class PlatformContentModel(BaseModel):
    platform: str
    headline: str
    body: str
    call_to_action: str

class CampaignFunnelModel(BaseModel):
    awareness: str
    consideration: str
    conversion: str

class CampaignStrategyModel(BaseModel):
    campaign_name: str
    target_audience: str
    funnel_strategy: CampaignFunnelModel
    platform_content: List[PlatformContentModel]
    visual_prompts: List[VisualPromptModel]
    suggested_budget_allocation: Dict[str, str]
    overall_roadmap: str

class CampaignOrchestrator:
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        
        # Discover available models
        self.available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    self.available_models.append(m.name.replace("models/", ""))
        except:
            self.available_models = ["gemini-1.5-pro", "gemini-2.0-flash", "gemini-1.5-flash"]
        
        self.groq_api_key = st.secrets.get("GROQ_API_KEY")

    def _call_groq(self, prompt):
        """Fallback to Groq if Gemini fails."""
        try:
            from groq import Groq
            client = Groq(api_key=self.groq_api_key)
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq Fallback Failed: {str(e)}")

    def orchestrate(self, product_description, target_audience, primary_goal, budget_limit=None):
        """Generates a complete multichannel marketing campaign."""
        
        prompt = f"""
        Act as a Chief Marketing Officer (CMO) and Strategic Growth Hacker.
        Orchestrate a complete marketing campaign for the following:
        
        PRODUCT: {product_description}
        TARGET AUDIENCE: {target_audience}
        PRIMARY GOAL: {primary_goal}
        BUDGET LIMIT: {budget_limit if budget_limit else "Not specified"}
        
        CRITICAL RELIABILITY RULES:
        1. DO NOT invent local branches, specific office addresses, or regional details unless they are explicitly mentioned in the PRODUCT description.
        2. If the product is digital or global, keep the strategy global. 
        3. DO NOT hallucinate partners or specific media outlets not requested.
        4. Focus on the core value proposition provided.
        
        Provide the strategy in ARABIC (except for technical terms) in a clean JSON format:
        {{
            "campaign_name": "اسم الحملة الإبداعي",
            "target_audience": "تحليل دقيق للجمهور المستهدف",
            "funnel_strategy": {{
                "awareness": "استراتيجية التوعية",
                "consideration": "استراتيجية الاهتمام",
                "conversion": "استراتيجية التحويل"
            }},
            "platform_content": [
                {{
                    "platform": "Instagram/TikTok/Facebook/Google",
                    "headline": "العنوان الجذاب",
                    "body": "نص الإعلان",
                    "call_to_action": "زر اتخاذ الإجراء"
                }}
            ],
            "visual_prompts": [
                {{
                    "platform": "Platform Name",
                    "prompt": "Highly detailed AI image generation prompt (in English)",
                    "concept": "شرح فكرة التصميم"
                }}
            ],
            "suggested_budget_allocation": {{
                "Instagram": "20%",
                "TikTok": "40%",
                "Google Ads": "40%"
            }},
            "overall_roadmap": "خطة العمل الزمنية (Roadmap)"
        }}
        """
        
        last_error = ""
        # 1. Try Gemini Rotation
        for model_name in self.available_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                txt = response.text.replace("```json", "").replace("```", "").strip()
                
                # Extract JSON block
                import json
                start = txt.find("{")
                end = txt.rfind("}")
                raw_data = json.loads(txt[start:end+1])
                
                # Validate with Pydantic
                validated = CampaignStrategyModel(**raw_data)
                return validated.model_dump()
            except Exception as e:
                last_error = str(e)
                continue

        # 2. Try Groq Fallback
        if self.groq_api_key:
            try:
                txt = self._call_groq(prompt)
                import json
                start = txt.find("{")
                end = txt.rfind("}")
                raw_data = json.loads(txt[start:end+1])
                validated = CampaignStrategyModel(**raw_data)
                return validated.model_dump()
            except Exception as e:
                last_error = f"{last_error} | Groq Error: {str(e)}"

        return {"error": f"All AI engines failed: {last_error}"}

def get_orchestrator():
    return CampaignOrchestrator()
