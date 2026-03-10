import streamlit as st
import json
from ai_engine.universal_analyzer import analyze_universal_link, format_expert_content

def analyze_competitor_clash(url1, url2):
    """
    ELITE COMPETITOR BATTLEGROUND.
    Compares two entities to find strategic gaps and advantages.
    """
    prompt = f"""
    ACT AS THE WORLD'S TOP CORPORATE STRATEGIST.
    Perform a COMPETITIVE CLASH analysis between:
    1. {url1}
    2. {url2}
    
    COMPARE THEM ON:
    - Market Dominance
    - Product/Content Quality
    - Strategic Gaps
    - Predicted Winner (1-year horizon)
    
    Output a JSON in Arabic:
    {{
        "entity_1_strengths": ["...", "..."],
        "entity_2_strengths": ["...", "..."],
        "clash_summary": "Deep analysis of the rivalry",
        "strategic_gap": "Where one is winning and the other is failing",
        "battleground_forecast": "Who will dominate in 12 months"
    }}
    """
    # Using Gemini as the primary clash engine
    try:
        import google.generativeai as genai
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if google_key:
            genai.configure(api_key=google_key.strip())
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            txt = response.text.replace("```json", "").replace("```", "").strip()
            start = txt.find("{")
            end = txt.rfind("}")
            return json.loads(txt[start:end+1])
    except:
        pass
        
    return {
        "entity_1_strengths": ["قوة افتراضية 1"],
        "entity_2_strengths": ["قوة افتراضية 2"],
        "clash_summary": "حدث خطأ أثناء الاتصال بالمحرك. يرجى المحاولة لاحقاً.",
        "strategic_gap": "تحليل الفجوة غير متاح حالياً.",
        "battleground_forecast": "التوقعات متوقفة مؤقتاً."
    }

def analyze_sentiment_command(url):
    """
    ELITE SENTIMENT COMMAND CENTER.
    Extracts audience emotions and perception.
    """
    prompt = f"Perform a SENTIMENT COMMAND analysis for {url}. Output JSON in Arabic with keys: overall_mood (Safe/Alert/Doubt), audience_perception (3 points), and emotional_velocity (Rising/Falling)."
    
    try:
        import google.generativeai as genai
        google_key = st.secrets.get("GOOGLE_API_KEY")
        if google_key:
            genai.configure(api_key=google_key.strip())
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            txt = response.text.replace("```json", "").replace("```", "").strip()
            start = txt.find("{")
            end = txt.rfind("}")
            return json.loads(txt[start:end+1])
    except:
        pass
        
    return {"overall_mood": "Unknown", "audience_perception": [], "emotional_velocity": "Static"}
