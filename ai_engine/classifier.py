# ==========================================================
# MTSE AI Content Classifier - Auto-Routing Domain
# ==========================================================

import streamlit as st
import google.generativeai as genai

class AIClassifier:
    """
    Automatically detects the domain of the content to apply specific analysis layers.
    """
    def __init__(self):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key.strip())
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def detect_domain(self, content_sample):
        """
        Returns one of: Engineering, Financial, Legal, Marketing, Admin, Mixed.
        Includes model rotation for stability.
        """
        prompt = f"""
        Analyze the following content sample and classify it into exactly ONE category:
        [Engineering, Financial, Legal, Marketing, Admin, Mixed]
        
        Content Sample: {content_sample[:2000]}
        
        Output only the category name.
        """
        candidates = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash']
        
        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                category = response.text.strip().replace("[", "").replace("]", "")
                valid_categories = ["Engineering", "Financial", "Legal", "Marketing", "Admin", "Mixed"]
                if category in valid_categories:
                    return category
                continue 
            except:
                continue
        return "Marketing"

def classify_content(content):
    classifier = AIClassifier()
    return classifier.detect_domain(content)
