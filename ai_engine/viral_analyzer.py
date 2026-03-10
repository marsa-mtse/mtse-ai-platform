# ==========================================================
# MTSE Marketing Engine - Viral Analyzer
# ==========================================================

import random
import streamlit as st
import json
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from utils import t, format_arabic

def analyze_virality(content_text, has_media=False, target_audience="General"):
    """
    Analyzes content to predict its virality score.
    Returns score (0-100) and specific feedback points.
    """
    
    score = 40 # Base score
    feedback = []
    modifiers = []
    
    # Analyze text length
    words = len(content_text.split())
    if 10 < words < 50:
        score += 15
        feedback.append("✨ طول النص مثالي وسهل القراءة السريعة.")
    elif words > 100:
        score -= 10
        feedback.append("⚠️ النص طويل جداً، قد يقلل من تفاعل الجمهور في بعض المنصات.")
    else:
        feedback.append("📝 طول النص مقبول.")

    # Check for emotional triggers or strong words
    power_words = ["حصري", "سر", "مجاناً", "عاجل", "صدمة", "مفاجأة", "جديد", "اليوم"]
    found_power_words = [w for w in power_words if w in content_text]
    
    if found_power_words:
        score += len(found_power_words) * 5
        feedback.append(f"🔥 استخدام جيد للكلمات القوية المحفزة ({', '.join(found_power_words)}).")
    else:
        feedback.append("💡 أضف بعض الكلمات المحفزة (مثل: حصري، سر، مجاناً) لزيادة الجذب.")
        
    # Check for media
    if has_media:
        score += 20
        feedback.append("📸 المحتوى المرئي يضاعف فرص الانتشار بنسبة كبيرة.")
    else:
        feedback.append("🖼️ إضافة صورة أو فيديو سيزيد من التفاعل بشكل ملحوظ.")
        
    # Check for hashtags
    hashtag_count = content_text.count("#")
    if 1 <= hashtag_count <= 5:
        score += 10
        feedback.append("🏷️ عدد الهاشتاجات مناسب ويساعد على الاكتشاف.")
    elif hashtag_count > 5:
        score -= 5
        feedback.append("⚠️ استخدام هاشتاجات كثيرة قد يبدو كـ Spam.")
    else:
        feedback.append("🔍 أضف 2-3 هاشتاجات متعلقة بالموضوع.")

    # Cap score
    score = min(score, 99)
    
    # Audience specific analysis
    if target_audience != "General":
        feedback.append(f"🎯 تم تقييم المحتوى بناءً على اهتمامات جمهورك: {target_audience}")

    return {
        "score": score,
        "feedback": feedback,
        "is_viral_candidate": score >= 80
    }


def rewrite_for_virality(content_text, tone="Viral"):
    """
    Rewrites content for virality using Gemini, OpenAI, or simulation.
    """
    # 1. Google Gemini (Free Tier)
    google_key = st.secrets.get("GOOGLE_API_KEY")
    if google_key and genai:
        try:
            genai.configure(api_key=google_key.strip())
            success_model = None
            response = None
            for model_name in ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-latest']:
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = f"Rewrite this for social media virality. Tone: {tone}. Content: {content_text}. Output 3 variations in Arabic. No extra text."
                    response = model.generate_content(prompt)
                    if response.text:
                        success_model = model_name
                        break
                except Exception:
                    continue

            if not response:
                raise Exception("Could not connect to any Gemini model")

            choices = response.text.split("\n")
            variations = [c.strip() for c in choices if len(c.strip()) > 15]
            if variations: return variations[:3]
        except Exception as e:
            st.warning(f"Gemini AI Error: {e}")

    # 2. OpenAI
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key and openai:
        try:
            client = openai.OpenAI(api_key=api_key)
            prompt = f"Rewrite this for social media virality. Tone: {tone}. Content: {content_text}. Output 3 variations in Arabic."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            choices = response.choices[0].message.content.split("\n")
            variations = [c.strip() for c in choices if len(c.strip()) > 15]
            if variations: return variations[:3]
        except Exception as e:
            st.error(f"OpenAI AI Error: {e}")

    # 3. Fallback Simulation
    prefixes = [
        "🔥 السر اللي الكل بيدور عليه: ",
        "🚀 أخيراً، الحل النهائي لـ: ",
        "✨ مش هتصدق النتيجة لما تجرب: ",
        "💡 نصيحة من خبير: ",
        "⚡ عاجل وحصري: "
    ]
    
    suffixes = [
        "\n\n👇 اضغط الرابط في البايو للتفاصيل",
        "\n\n🔥 شير عشان الكل يستفيد",
        "\n\n📝 منشن صاحبك اللي محتاج يشوف ده",
        "\n\n✨ عرض خاص لفترة محدودة جداً",
        "\n\n🚀 انضم لأقوى مجتمع ماركتينج الآن"
    ]
    
    hashtags = " #تسويق #بيزنس #نمو #MTSE #AI #viral"
    
    variations = []
    import random
    
    for i in range(3):
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        # Simple transformation logic
        words = content_text.split()
        if len(words) > 10:
            core_content = " ".join(words[:10]) + "..."
        else:
            core_content = content_text
            
        variations.append(f"{prefix}{core_content}{suffix}{hashtags}")
        
    return variations
