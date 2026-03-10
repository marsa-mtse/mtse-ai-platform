# ==========================================================
# MTSE Social Media Sniper - Multi-Platform Audit
# ==========================================================

import streamlit as st
import json
import google.generativeai as genai

class SocialSniper:
    """
    Analyzes social media profiles/links for performance and strategy.
    """
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def audit_profile(self, url):
        """Perform a 360-degree audit on a social media link."""
        prompt = f"""
        Act as an Elite Social Media Auditor and Strategic Growth Consultant.
        Perform a comprehensive audit on this link: {url}
        
        Required focus areas:
        1. Content Identity & Branding.
        2. Engagement Patterns (Simulated based on visible markers).
        3. Strategic Gaps & Missed Opportunities.
        4. Competitor Comparison.
        
        Output EXACTLY a JSON in Arabic:
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
        try:
            response = self.model.generate_content(prompt)
            txt = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(txt)
        except Exception as e:
            return {{"error": str(e)}}

def get_social_sniper():
    return SocialSniper()
