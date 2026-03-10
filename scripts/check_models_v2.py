import google.generativeai as genai
import streamlit as st

def list_gemini_models():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        print("CRITICAL: No GOOGLE_API_KEY found in secrets.")
        return
    
    genai.configure(api_key=api_key.strip())
    print("--- START OF MODEL LIST ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"MODEL_ID: {m.name}")
    except Exception as e:
        print(f"ERROR: {e}")
    print("--- END OF MODEL LIST ---")

if __name__ == "__main__":
    list_gemini_models()
