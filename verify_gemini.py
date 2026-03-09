import streamlit as st
import google.generativeai as genai
import os

def test_gemini():
    print("Testing Gemini API connection...")
    
    # Try to find the key in st.secrets or environment
    key = None
    try:
        # Check local streamlit secrets
        import toml
        secrets_path = ".streamlit/secrets.toml"
        if os.path.exists(secrets_path):
            with open(secrets_path, "r") as f:
                secrets = toml.load(f)
                key = secrets.get("GOOGLE_API_KEY")
    except Exception as e:
        print(f"Error reading secrets: {e}")

    if not key:
        print("GOOGLE_API_KEY not found in .streamlit/secrets.toml")
        return

    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Gemini is Active!' in Arabic.")
        print(f"Connection Successful!")
        print(f"AI Response: {response.text}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_gemini()
