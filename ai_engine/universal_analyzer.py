import streamlit as st
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

def get_gemini_model():
    """Get the first available working Gemini model."""
    google_key = st.secrets.get("GOOGLE_API_KEY")
    if not google_key or not genai:
        return None
    
    genai.configure(api_key=google_key.strip())
    for model_name in ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            return model
        except Exception:
            continue
    return None

def analyze_universal_link(url, depth="Deep"):
    """
    Analyzes any URL using Gemini's multimodal/web capabilities.
    Returns a structured analysis object.
    """
    model = get_gemini_model()
    if not model:
        return {"error": "AI Engine not configured."}

    prompt = f"""
    Perform a {depth} marketing and strategic analysis of this URL: {url}
    
    Analyze the following aspects:
    1. Content Summary: What is this about?
    2. Target Audience: Who is this for?
    3. Sentiment & Tone: Brand voice and user reaction.
    4. Strategic SWOT: Strengths, Weaknesses, Opportunities, Threats.
    5. Actionable Advice: 3-5 concrete steps for improvement or expansion.
    
    Output the result in a structured JSON format with these keys: 
    'summary', 'audience', 'sentiment', 'swot', 'recommendations'.
    Language: Support both Arabic and English if possible.
    """

    try:
        response = model.generate_content(prompt)
        txt = response.text.replace("```json", "").replace("```", "").strip()
        # JSON extraction cleanup
        start = txt.find("{")
        end = txt.rfind("}")
        if start != -1 and end != -1:
            txt = txt[start:end+1]
        
        return json.loads(txt)
    except Exception as e:
        return {"error": str(e)}

def generate_strategic_insights(analysis_data, lang="Both"):
    """
    Refines the analysis data into a formal report structure.
    """
    # This prepares the data for the structure
    report = {
        "title": "Universal Strategic Analysis / تحليل استراتيجي شامل",
        "sections": [
            {"heading": "Summary / الملخص", "content": analysis_data.get("summary", "")},
            {"heading": "Target Audience / الجمهور المستهدف", "content": analysis_data.get("audience", "")},
            {"heading": "Sentiment / الانطباع العام", "content": analysis_data.get("sentiment", "")},
            {"heading": "SWOT Analysis / تحليل نقاط القوة والضعف", "content": analysis_data.get("swot", "")},
            {"heading": "Recommendations / التوصيات", "content": analysis_data.get("recommendations", "")}
        ]
    }
    return report
