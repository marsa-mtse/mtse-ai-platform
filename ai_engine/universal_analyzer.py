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

def t(ar, en):
    """Local translation helper for universal analyzer."""
    import streamlit as st
    return ar if st.session_state.get("lang") == "AR" else en

def analyze_universal_link(url, depth="Deep"):
    """
    ELITE OMNI-INTELLIGENCE ENGINE.
    Analyzes ANY content across ALL domains with 10x depth.
    """
    google_key = st.secrets.get("GOOGLE_API_KEY")
    openai_key = st.secrets.get("OPENAI_API_KEY")
    
    # 1. --- GOOGLE GEMINI ELITE STRATEGY ---
    if google_key and genai:
        genai.configure(api_key=google_key.strip())
        model_candidates = [
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash-latest', 
            'gemini-1.5-flash-002',
            'gemini-1.5-flash', 
            'gemini-2.0-flash'
        ]

        prompt = f"""
        ACT AS THE WORLD'S HIGHEST-RANKED UNIVERSAL STRATEGIC ANALYST & MULTI-DOMAIN EXPERT.
        Your mission is to perform an EXTREME DEEP DIVE on this input: {url}
        
        CRITICAL REASONING GUIDELINES:
        1. Identify the EXPLICIT DOMAIN (Politics, Economics, Social, Tech, Personality, etc.).
        2. Conduct a 'PESTEL' or 'Porter' style analysis if applicable.
        3. Reveal hidden patterns, psychological markers, and non-obvious correlations.
        4. Forecast the 1-year and 5-year impact of this data.
        
        REQUIRED OUTPUT SECTIONS:
        - Domain: Precise classification.
        - Essence: A high-level philosophical and practical distillation.
        - Deep Analysis: 5-7 paragraphs of granular, technical, and strategic findings.
        - Strategic Matrix: A list of 4 key vectors (Variable vs Impact).
        - Risk Assessment: Identify 3 critical vulnerabilities or threats.
        - Long-term Forecast: Predicted trajectory.
        - The Roadmap: 7 actionable, high-impact steps.
        
        Output EXACTLY a JSON in professional Arabic:
        {{
            "domain": "المجال الدقيق",
            "essence": "جوهر وفلسفة المحتوى",
            "deep_analysis": "تحليل معمق وشامل (أكثر من 500 كلمة)",
            "strategic_matrix": ["متجه 1: شرح", "متجه 2: شرح", ...],
            "risk_assessment": ["خطر 1: تحليل", "خطر 2: تحليل", ...],
            "forecast": "التوقعات المستقبلية والمسار المتوقع",
            "roadmap": ["خطوة استراتيجية 1", "خطوة استراتيجية 2", ...]
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

    # 2. --- OPENAI ELITE FALLBACK ---
    if openai_key and openai:
        try:
            client = openai.OpenAI(api_key=openai_key)
            prompt = f"Elite Universal Intelligence Analysis (10x Depth) in Arabic for: {url}. Output JSON with keys: domain, essence, deep_analysis, strategic_matrix (list), risk_assessment (list), forecast, roadmap (list)."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except:
            pass

    # 3. --- ELITE SAFETY ENGINE ---
    return {
        "domain": "الاستخبارات الرقمية العامة",
        "essence": "تحليل أولي عبر المحرك الاحتياطي العميق.",
        "deep_analysis": "النظام حالياً يقوم برصد البيانات الأساسية. يرجى التأكد من تفعيل مفاتيح ה-API للحصول على التحليل النخبوي الكامل الذي يتجاوز 1000 كلمة.",
        "strategic_matrix": ["الانتشار: مرصود", "التفاعل: متوسط"],
        "risk_assessment": ["نقص البيانات اللحظية"],
        "forecast": "نمو مستقر مع حاجة لتحديث الرؤى.",
        "roadmap": ["تفعيل الربط المتقدم", "تحليل المنافسين"]
    }

def generate_strategic_insights(analysis_data, lang="Both"):
    """
    Refines the elite universal analysis data into a formal, world-class report.
    """
    sections = []
    
    # 1. Domain & Essence
    dom = analysis_data.get("domain", "General Intelligence")
    ess = analysis_data.get("essence", "")
    sections.append({
        "heading": f"1. {t('مجال الاستخبارات وجوهر الرؤية', 'Intelligence Domain & Vision Essence')}",
        "content": f"{t('المجال النخبوي:', 'Elite Domain:')} {dom}\n\n{ess}"
    })
    
    # 2. Deep Analysis (The Core)
    analysis = analysis_data.get("deep_analysis", "")
    sections.append({
        "heading": f"2. {t('التحليل الاستراتيجي المعمق (10x Depth)', 'Elite Strategic Deep Dive')}",
        "content": analysis
    })
    
    # 3. Strategic Matrix
    matrix = analysis_data.get("strategic_matrix", [])
    matrix_str = "\n".join([f"◈ {m}" for m in matrix]) if isinstance(matrix, list) else matrix
    sections.append({
        "heading": f"3. {t('مصفوفة المتجهات الاستراتيجية', 'Strategic Vector Matrix')}",
        "content": matrix_str
    })

    # 4. Risk Assessment
    risks = analysis_data.get("risk_assessment", [])
    risks_str = "\n".join([f"⚠ {r}" for r in risks]) if isinstance(risks, list) else risks
    sections.append({
        "heading": f"4. {t('تقييم المخاطر والتهديدات النخبوية', 'Elite Risk & Threat Assessment')}",
        "content": risks_str
    })

    # 5. Long-term Forecast
    forecast = analysis_data.get("forecast", "")
    sections.append({
        "heading": f"5. {t('التوقعات والمسار المستقبلي بعيد المدى', 'Long-term Strategic Forecast')}",
        "content": forecast
    })

    # 6. Elite Roadmap
    roadmap = analysis_data.get("roadmap", [])
    roadmap_str = "\n".join([f"➤ {r}" for r in roadmap]) if isinstance(roadmap, list) else roadmap
    sections.append({
        "heading": f"6. {t('خارطة الطريق التنفيذية العالمية', 'Universal Executive Roadmap')}",
        "content": roadmap_str
    })
    
    return {
        "title": t("تقرير الاستخبارات والتحليل العالمي النخبوي - MTSE OMNI ELITE", "Elite Universal Intelligence Report - MTSE OMNI ELITE"),
        "sections": sections
    }
