# ==========================================================
# MTSE Social Media Sniper - Multi-Platform Audit
# ==========================================================

import streamlit as st
import json
import google.generativeai as genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict

class SWOTModel(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class RoadmapStepModel(BaseModel):
    phase: str
    action: str
    expected_impact: str

class AuditReportModel(BaseModel):
    audit_summary: str
    swot: SWOTModel
    content_roadmap: List[RoadmapStepModel]
    cta_optimization: str
    viral_potential: str

@st.cache_data(ttl=3600, show_spinner=False)
def perform_audit_cached(url: str, available_models: List[str], context: str = "") -> dict:
    prompt = f"""
    Act as an Elite Social Media Auditor and Strategic Growth Consultant.
    Perform a comprehensive audit on this link: {url}
    
    {"[CONTEXT PROVIDED BY USER]: " + context if context else "[NO ADDITIONAL CONTEXT]"}

    CRITICAL INSTRUCTIONS:
    1. DO NOT GUESS location, industry, or specific details if they are not explicitly present in the URL or the context provided above.
    2. If the URL is generic (e.g. '@marsatouch') and no context is provided, focus on the 'Name' itself but state 'Insufficient data for geographic/industry profiling' if you are unsure.
    3. DO NOT confuse phonetic similarities (e.g., 'Marsa' with 'Marsa Alam') unless confirmed.
    4. Provide analysis based on marketing patterns visible in the branding of the name/url.
    
    Output EXACTLY a JSON in Arabic matching this exact schema:
    {{
        "audit_summary": "ملخص شامل للأداء الحالي",
        "swot": {{
            "strengths": ["نقطة 1", ...],
            "weaknesses": ["نقطة 1", ...],
            "opportunities": ["نقطة 1", ...],
            "threats": ["نقطة 1", ...]
        }},
        "content_roadmap": [
            {{"phase": "المرحلة 1", "action": "الإجراء", "expected_impact": "الأثر المتوقع"}},
            ...
        ],
        "cta_optimization": "كيفية تحسين دعوات اتخاذ الإجراء (CTA)",
        "viral_potential": "مدى إمكانية الانتشار الفيروسي"
    }}
    """
    last_errs = []
    for model_name in available_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            txt = response.text.replace("```json", "").replace("```", "").strip()
            
            # Robust extraction
            start = txt.find("{")
            end = txt.rfind("}")
            if start != -1 and end != -1:
                raw_dict = json.loads(txt[start:end+1])
            else:
                raw_dict = json.loads(txt)
                
            # Strict Pydantic validation
            validated_obj = AuditReportModel(**raw_dict)
            return validated_obj.model_dump()
            
        except ValidationError as ve:
             last_errs.append(f"{model_name} (Validation Error): {str(ve)}")
        except Exception as e:
            last_errs.append(f"{model_name}: {str(e)}")
            continue
    return {"error": f"Social Sniper failed after rotation: {' | '.join(last_errs)}"}


class SocialSniper:
    """
    Analyzes social media profiles/links for performance and strategy.
    """
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        
        # Discover accessible models dynamically
        self.available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    self.available_models.append(m.name.replace("models/", ""))
        except:
             self.available_models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash']
        
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def audit_profile(self, url, context=""):
        """Perform a 360-degree audit with model rotation."""
        return perform_audit_cached(url, tuple(self.available_models), context=context)

def get_social_sniper():
    return SocialSniper()
