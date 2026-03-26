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

try:
    import groq
except ImportError:
    groq = None

from ai_engine.classifier import classify_content

def t(ar, en):
    """Local translation helper for universal analyzer."""
    import streamlit as st
    return ar if st.session_state.get("lang") == "AR" else en

def format_expert_content(data):
    """
    Recursively formats complex AI response structures (dicts/lists) 
    into a world-class, human-readable string.
    """
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        items = []
        for i in data:
            formatted = format_expert_content(i)
            items.append(f"• {formatted}")
        return "\n".join(items)
    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            key_label = k.replace("_", " ").title()
            if isinstance(v, (dict, list)):
                lines.append(f"**{key_label}:**\n{format_expert_content(v)}")
            else:
                lines.append(f"**{key_label}:** {v}")
        return "\n".join(lines)
    return str(data)

def get_api_status():
    """Returns the status of AI backends."""
    google_key = st.secrets.get("GOOGLE_API_KEY")
    openai_key = st.secrets.get("OPENAI_API_KEY")
    groq_key = st.secrets.get("GROQ_API_KEY")
    return {
        "google": bool(google_key and genai),
        "openai": bool(openai_key and openai),
        "groq": bool(groq_key and groq)
    }

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
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-flash',
        ]

        # Phase 10: AI Domain Detection
        detected_domain = classify_content(url)
        
        industry_prompts = {
            "Engineering": "Act as a Lead Project Engineer and Senior Estimator.",
            "Financial": "Act as a Chief Financial Officer and Market Risk Analyst.",
            "Legal": "Act as a Senior Legal Counsel and Regulatory Expert.",
            "Marketing": "Act as a Global Marketing Strategist and Growth Hacker.",
            "Admin": "Act as an Operations Director and Management Consultant.",
            "Mixed": "Act as a Multi-Disciplinary Industrial Consultant."
        }
        
        system_role = industry_prompts.get(detected_domain, "Act as a World-Class Strategic Analyst.")

        prompt = f"""
        {system_role}
        Perform an EXTREME DEEP DIVE on this input: {url}
        
        Detected Industry: {detected_domain}
        
        CRITICAL REASONING GUIDELINES:
        1. Tailor all insights to the requirements of the {detected_domain} industry.
        2. Identify the EXPLICIT DOMAIN (Politics, Economics, Social, Tech, Personality, etc.).
        3. Conduct a granular, technical analysis based on industry standards.
        4. Forecast the 1-year and 5-year impact of this data.
        
        REQUIRED OUTPUT SECTIONS:
        - Domain: Precise classification.
        - Essence: A high-level distillation.
        - Deep Analysis: 5-7 paragraphs of granular finds.
        - Strategic Matrix: 4 key vectors (Variable vs Impact).
        - Risk Assessment: 3 critical vulnerabilities.
        - Long-term Forecast: Predicted trajectory.
        - The Roadmap: 7 actionable steps.
        
        Output EXACTLY a JSON where ALL keys and ALL values are in professional Arabic:
        {{
            "domain": "المجال الدقيق (بناءً على تصنيف {detected_domain})",
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
                st.session_state.last_ai_error = f"Gemini ({model_name}): {str(e)}"
                err = str(e)
                if "429" in err or "404" in err or "Quota" in err: continue
                else: break

    # 2. --- OPENAI ELITE FALLBACK ---
    if openai_key and openai:
        try:
            client = openai.OpenAI(api_key=openai_key)
            prompt = f"Elite Universal Intelligence Analysis (10x Depth) for: {url}. YOU MUST OUTPUT THE CONTENT ENTIRELY IN ARABIC. Output JSON with keys: domain, essence, deep_analysis, strategic_matrix (list), risk_assessment (list), forecast, roadmap (list)."
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            st.session_state.last_ai_error = f"OpenAI: {str(e)}"
            pass

    # 3. --- GROQ ELITE BACKUP (LLAMA-3 FREE) ---
    groq_key = st.secrets.get("GROQ_API_KEY")
    if groq_key:
        if not groq:
            st.session_state.last_ai_error = "Groq library not installed. Please wait for the server to update requirements.txt."
        else:
            try:
                client = groq.Groq(api_key=groq_key.strip())
                prompt = f"Elite Universal Intelligence Analysis (10x Depth) in Arabic for: {url}. Output JSON with keys: domain, essence, deep_analysis, strategic_matrix (list), risk_assessment (list), forecast, roadmap (list). IMPORTANT: ALL CONTENT MUST BE IN ARABIC."
                
                # Model rotation for Groq
                for groq_model in ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]:
                    try:
                        response = client.chat.completions.create(
                            model=groq_model,
                            messages=[{"role": "user", "content": prompt}],
                            response_format={ "type": "json_object" }
                        )
                        return json.loads(response.choices[0].message.content)
                    except Exception as e:
                        if "429" in str(e) or "model_decommissioned" in str(e):
                            continue
                        raise e
            except Exception as e:
                st.session_state.last_ai_error = f"Groq (Llama-3): {str(e)}"
                pass

    # 4. --- ELITE SAFETY ENGINE ---
    error_msg = st.session_state.get("last_ai_error", "All AI providers failed or no API keys are provided.")
    if not any([google_key, openai_key, groq_key]):
        error_msg = "Missing API Keys: Please set GOOGLE_API_KEY, GROQ_API_KEY or OPENAI_API_KEY in Streamlit secrets."
        
    return {
        "error": t(
            f"فشل التحليل الذكي بسبب: {error_msg}", 
            f"Smart analysis failed due to: {error_msg}"
        )
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
        "content": f"{t('المجال النخبوي:', 'Elite Domain:')} {format_expert_content(dom)}\n\n{format_expert_content(ess)}"
    })
    
    # 2. Deep Analysis (The Core)
    analysis = analysis_data.get("deep_analysis", "")
    sections.append({
        "heading": f"2. {t('التحليل الاستراتيجي المعمق (10x Depth)', 'Elite Strategic Deep Dive')}",
        "content": format_expert_content(analysis)
    })
    
    # 3. Strategic Matrix
    matrix = analysis_data.get("strategic_matrix", [])
    sections.append({
        "heading": f"3. {t('مصفوفة المتجهات الاستراتيجية', 'Strategic Vector Matrix')}",
        "content": format_expert_content(matrix)
    })

    # 4. Risk Assessment
    risks = analysis_data.get("risk_assessment", [])
    sections.append({
        "heading": f"4. {t('تقييم المخاطر والتهديدات النخبوية', 'Elite Risk & Threat Assessment')}",
        "content": format_expert_content(risks)
    })

    # 5. Long-term Forecast
    forecast = analysis_data.get("forecast", "")
    sections.append({
        "heading": f"5. {t('التوقعات والمسار المستقبلي بعيد المدى', 'Long-term Strategic Forecast')}",
        "content": format_expert_content(forecast)
    })

    # 6. Elite Roadmap
    roadmap = analysis_data.get("roadmap", [])
    sections.append({
        "heading": f"6. {t('خارطة الطريق التنفيذية العالمية', 'Universal Executive Roadmap')}",
        "content": format_expert_content(roadmap)
    })
    
    return {
        "title": t("تقرير الاستخبارات والتحليل العالمي النخبوي - MTSE OMNI ELITE", "Elite Universal Intelligence Report - MTSE OMNI ELITE"),
        "sections": sections
    }
