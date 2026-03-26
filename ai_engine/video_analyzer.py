# ==============================
# AI Video Intelligence Engine
# ==============================
import streamlit as st
import time
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

class VideoSceneModel(BaseModel):
    timestamp: str
    visual_description: str
    marketing_insight: str
    suggestion: str

class VideoAuditModel(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    hook_effectiveness: str
    visual_pacing: str
    script_quality: str
    retention_risk_points: List[str]
    scenes_analysis: List[VideoSceneModel]
    final_recommendation: str

class VideoAnalyzer:
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
            self.available_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"]
        
        self.groq_api_key = st.secrets.get("GROQ_API_KEY")

    def analyze_video(self, video_file_path):
        """Processes video and returns structured marketing intelligence."""
        
        # Uploading to Gemini Files API (Required for video > a few MB/seconds)
        try:
            with st.spinner("📤 Uploading video to AI Cloud..."):
                video_file = genai.upload_file(path=video_file_path)
                
                # Wait for processing
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name == "FAILED":
                    raise Exception("AI Video processing failed.")

            prompt = """
            Act as a Strategic Video Marketing Expert and Viral Growth Consultant.
            Analyze this video for its marketing effectiveness.
            
            CRITICAL RELIABILITY RULES:
            1. DO NOT guess speaker names, specific company departments, or locations if they are not visible/audible in the video.
            2. If branding is unclear, describe it generically rather than assuming a brand name.
            3. Focus on objective visual pacing and marketing psychology markers.
            4. If the video is purely abstract, state 'Abstract visual style - analysis based on artistic impact' instead of guessing specific hooks.

            Provide a deep audit in Arabic with the following structure (JSON):
            {
                "overall_score": 85,
                "hook_effectiveness": "تحليل أول 3 ثواني",
                "visual_pacing": "تحليل سرعة التنقل بين المشاهد",
                "script_quality": "تقييم النصوص أو الكلام المنطوق",
                "retention_risk_points": ["نقطة 1", "نقطة 2"],
                "scenes_analysis": [
                    {"timestamp": "00:05", "visual_description": "وصف المشهد", "marketing_insight": "لماذا هذا المشهد مهم؟", "suggestion": "تطوير مقترح"}
                ],
                "final_recommendation": "الخلاصة للنجاح"
            }
            """
            
            last_error = ""
            for model_name in self.available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content([video_file, prompt])
                    txt = response.text.replace("```json", "").replace("```", "").strip()
                    import json
                    start = txt.find("{")
                    end = txt.rfind("}")
                    raw_data = json.loads(txt[start:end+1])
                    validated = VideoAuditModel(**raw_data)
                    
                    try: genai.delete_file(video_file.name)
                    except: pass
                    
                    return validated.model_dump()
                except Exception as e:
                    last_error = str(e)
                    continue

            try: genai.delete_file(video_file.name)
            except: pass
            return {"error": f"Video AI failed: {last_error}"}

        except Exception as e:
            return {"error": str(e)}

def get_video_analyzer():
    return VideoAnalyzer()
