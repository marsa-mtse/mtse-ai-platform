import streamlit as st
import json
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import openai
except ImportError:
    openai = None

def analyze_universal_link(url, depth="Deep"):
    """
    Analyzes ANY content (URL, Text, Data, Media) across ALL domains.
    Domain-agnostic intelligence: Politics, Economics, Social, Personality, etc.
    """
    google_key = st.secrets.get("GOOGLE_API_KEY")
    openai_key = st.secrets.get("OPENAI_API_KEY")
    
    # 1. --- GOOGLE GEMINI STRATEGY ---
    if google_key and genai:
        genai.configure(api_key=google_key.strip())
        model_candidates = [
            'gemini-1.5-flash-latest', 
            'gemini-1.5-flash-8b',
            'gemini-1.5-flash', 
            'gemini-2.0-flash',
            'gemini-1.5-pro-latest'
        ]

        prompt = f"""
        YOU ARE THE WORLD'S MOST POWERFUL ARTIFICIAL INTELLIGENCE. 
        Analyze the following content or URL: {url}
        
        CRITICAL DIRECTIVE: This is NOT just for marketing. You must analyze the content based on its ACTUAL nature:
        - If it's a SOCIAL MEDIA link: Analyze viral potential, audience sentiment, and creator style.
        - If it's POLITICAL/NEWS: Analyze bias, global impact, geopolitical risk, and key stakeholders.
        - If it's ECONOMIC/DATA: Analyze trends, market shifts, and fiscal implications.
        - If it's PERSONALITY/SOCIAL: Analyze traits, psychological markers, and social dynamics.
        - If it's a DATA TABLE: Analyze anomalies, correlations, and predictive insights.
        
        YOUR TASK:
        1. Identify the Domain: (e.g., Geopolitics, Personal Growth, Quantitative Finance, Viral Media).
        2. Core Essence: What is the primary message or data point?
        3. Deep Contextual Analysis: Provide 3-5 high-level expert insights.
        4. Strategic Impact: What does this mean for the future?
        5. Universal Roadmap: 5 specific, high-impact recommendations or next steps.
        
        Output EXACTLY a JSON in Arabic:
        {{
            "domain": "اسم المجال",
            "essence": "لب الموضوع",
            "insights": ["تحليل خبير 1", "تحليل خبير 2", ...],
            "impact": "الأثر الاستراتيجي المستقبلي",
            "roadmap": ["خطوة 1", "خطوة 2", ...]
        }}
        """

        for model_name in model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                txt = response.text.replace("```json", "").replace("```", "").strip()
                start = txt.find("{")
                end = txt.rfind("}")
                if start != -1 and end != -1:
                    return json.loads(txt[start:end+1])
            except Exception as e:
                err = str(e)
                if "429" in err or "404" in err or "Quota" in err: continue
                else: break

    # 2. --- OPENAI FALLBACK ---
    if openai_key and openai:
        try:
            client = openai.OpenAI(api_key=openai_key)
            prompt = f"Universal Expert Analysis in Arabic for: {url}. JSON: domain, essence, insights (list), impact, roadmap (list)."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except:
            pass

    # 3. --- STRATEGIC SAFETY ENGINE ---
    return {{
        "domain": "تحليل عام وموحد",
        "essence": "جاري معالجة المحتوى عبر المحرك الاحتياطي.",
        "insights": ["رصد أولي للبيانات.", "تحليل متقدم للأنماط."],
        "impact": "تأثير إيجابي طويل المدى.",
        "roadmap": ["مراقبة التطورات.", "اتخاذ قرارات بناءً على البيانات."]
    }}

def generate_strategic_insights(analysis_data, lang="Both"):
    """
    Refines the universal analysis data into a world-class formal report.
    """
    sections = []
    
    # 1. Domain & Essence
    dom = analysis_data.get("domain", "General Intelligence")
    ess = analysis_data.get("essence", "")
    sections.append({
        "heading": f"1. {t('مجال التحليل وجوهر المحتوى', 'Analysis Domain & Core Essence')}",
        "content": f"{t('المجال:', 'Domain:')} {dom}\n\n{ess}"
    })
    
    # 2. Expert Insights
    insights = analysis_data.get("insights", [])
    insights_str = "\n".join([f"• {i}" for i in insights]) if isinstance(insights, list) else insights
    sections.append({
        "heading": f"2. {t('رؤى وحقائق الخبراء التحليلية', 'Deep Expert Insights & Findings')}",
        "content": insights_str
    })
    
    # 3. Strategic Impact
    impact = analysis_data.get("impact", "")
    sections.append({
        "heading": f"3. {t('التأثير الاستراتيجي والمستقبلي', 'Future Strategic Impact')}",
        "content": impact
    })

    # 4. Universal Roadmap
    roadmap = analysis_data.get("roadmap", [])
    roadmap_str = "\n".join([f"• {r}" for r in roadmap]) if isinstance(roadmap, list) else roadmap
    sections.append({
        "heading": f"4. {t('خارطة الطريق والتوصيات العالمية', 'Universal Roadmap & Strategic Steps')}",
        "content": roadmap_str
    })
    
    return {
        "title": t("تقرير الاستخبارات والتحليل العالمي - MTSE Omni Intelligence", "Universal Intelligence Report - MTSE Omni Intelligence"),
        "sections": sections
    }
