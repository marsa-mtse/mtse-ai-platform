import google.generativeai as genai
import os
import streamlit as st

def list_gemini_models():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        print("No API Key found")
        return
    genai.configure(api_key=api_key.strip())
    try:
        models = genai.list_models()
        for m in models:
            print(f"Name: {m.name}, Methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_gemini_models()
