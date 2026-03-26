# ==========================================================
# MTSE Marketing Engine v13 - Resilient AI Gateway
# Handles primary model execution and automatic failover
# ==========================================================

import streamlit as st
from config import FALLBACK_API_KEYS

def get_api_key(provider: str) -> str:
    """Retrieve API key from session, Streamlit secrets, or hardcoded config."""
    # Priority 1: User-entered session keys (AI Secrets Page)
    if "custom_keys" in st.session_state and provider.lower() in st.session_state.custom_keys:
        return st.session_state.custom_keys[provider.lower()]
        
    # Priority 2: Streamlit Secrets
    env_name = f"{provider.upper()}_API_KEY"
    key = st.secrets.get(env_name, None)
    if not key:
        # Priority 3: Fallback from config
        key = FALLBACK_API_KEYS.get(provider.lower(), None)
    return key


def structured_text_generation(system_prompt: str, user_prompt: str, preferred_provider: str = "openai") -> str | None:
    """
    Generate text using the preferred provider, but automatically fall back
    to other providers if the primary one fails (e.g. quota, rate limit, invalid key).
    
    Fallback Order:
    1. Requested Provider (e.g. 'openai')
    2. Anthropic (Claude 3.5 Sonnet)
    3. Groq (Llama 3.3 70B)
    4. Google (Gemini 1.5 Pro)
    5. OpenAI (GPT-4o Mini)
    """
    # Inject Global Brand Voice if available
    if "brand_voice" in st.session_state and st.session_state.brand_voice.get("personality"):
        bv = st.session_state.brand_voice
        brand_context = f"""
[GLOBAL BRAND VOICE ACTIVE]
Personality: {bv.get('personality')}
Core Values: {bv.get('core_values')}
Target Audience: {bv.get('target_audience')}
Forbidden Words: {bv.get('forbidden_words')}
---
"""
        system_prompt = brand_context + system_prompt

    # Priority list starting with preferred
    # Pivoted to Google/Anthropic as primary for v13.6 Stability
    providers_list = ["google", "anthropic", "groq", "openai"]
    if preferred_provider in providers_list:
        providers_list.remove(preferred_provider)
    providers_list.insert(0, preferred_provider) # Put preferred first

    last_error = None

    for provider in providers_list:
        try:
            key = get_api_key(provider)
            if not key:
                continue # Try next provider natively if key missing

            if provider == "openai":
                import openai
                client = openai.OpenAI(api_key=key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif provider == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=key)
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=3000,
                    temperature=0.7,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text

            elif provider == "groq":
                from groq import Groq
                client = Groq(api_key=key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif provider == "google":
                import google.generativeai as genai
                genai.configure(api_key=key)
                model = genai.GenerativeModel("gemini-1.5-pro")
                # Gemini doesn't have a strict system prompt in standard chat natively, 
                # so we combine it clearly for the generation.
                combined_prompt = f"System Instruction: {system_prompt}\n\nUser Request: {user_prompt}"
                response = model.generate_content(combined_prompt)
                return response.text

        except Exception as e:
            last_error = e
            # Log exact error locally for debug, but silently continue to next provider
            print(f"[AI Gateway] {provider} failed: {e}")
            continue

    return None # All providers exhausted or failed

# ==============================
# MULTIMEDIA GENERATION PIPELINES
# ==============================

def generate_image_advanced(prompt: str, provider: str = "openai", width: int = 1024, height: int = 1024) -> str | None:
    """
    Generate high-quality images using OpenAI's DALL-E 3. 
    This provides reliable production-ready images without needing external keys.
    """
    try:
        if provider == "openai":
            key = get_api_key("openai")
            if not key:
                print(f"[AI Gateway] Image provider '{provider}' key not configured.")
                return None
                
            import openai
            client = openai.OpenAI(api_key=key)
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"Cinematic, ultra-quality, professional marketing visualization: {prompt}",
                n=1,
                size="1024x1024"
            )
            return response.data[0].url
            
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"[AI Gateway - Image] {provider} failed: {e}")
        print(error_msg)
    return None


def generate_video(prompt: str, image_url: str = None, provider: str = "runway") -> str | None:
    """
    Placeholder for Video Generation APIs (Requiring Paid Developer Keys).
    """
    print("[AI Gateway] Video Generation requires a dedicated enterprise API key.")
    return None


def generate_audio(prompt: str, provider: str = "suno") -> str | None:
    """
    Placeholder for Audio Generation APIs (Requiring Paid Developer Keys).
    """
    print("[AI Gateway] Audio Generation requires a dedicated enterprise API key.")
    return None
