# ==========================================================
# MTSE Marketing Engine - AI Campaign Generator
# ==========================================================

import random
from utils import t

def generate_campaign_ideas(product_name, target_audience, platform="Meta (Facebook/Instagram)"):
    """
    Generate ad copy ideas based on the platform.
    If OpenAI is available in st.secrets, this would be an API call.
    For simulation, we use a smart fallback engine.
    """
    
    # Advanced fallback logic mimicking an AI response
    platforms_styles = {
        "Meta (Facebook/Instagram)": {
            "hooks": [
                f"هل تعبت من البحث عن الحل المثالي لـ {target_audience}؟",
                f"اكتشف السر وراء نجاح أقوى الـ {target_audience} اليوم!",
                f"توقف عن التفكير وابدأ التنفيذ مع {product_name}!"
            ],
            "body": [
                f"نقدم لك الحل الشامل المصمم خصيصاً ليناسب احتياجاتك. {product_name} يجمع بين السرعة والكفاءة.",
                f"آلاف المستخدمين يثقون في {product_name}. احصل على النتائج التي تستحقها وبدون مجهود.",
            ],
            "cta": ["اطلب الآن واحصل على خصم 20%!", "اضغط هنا لمعرفة المزيد 👇"],
        },
        "TikTok": {
            "hooks": [
                f"لن تصدق ما يمكن أن يفعله {product_name}! 🤯",
                f"التريند الجديد اللي كسر الدنيا للـ {target_audience} 🔥",
                f"جربت {product_name} وكانت النتيجة صدمة! شاهد للنهاية 👀"
            ],
            "body": [
                "بصراحة، أسهل وأسرع حل شفته في حياتي. جربه ومش هتندم!",
                "شوف بنفسك الفرق قبل وبعد استخدام هذا السحر ✨.",
            ],
            "cta": ["الرابط في البايو 🔗", "اطلب نسختك الآن قبل نفاذ الكمية 🏃‍♂️"],
        },
        "Google Search": {
            "hooks": [
                f"{product_name} - الأفضل للـ {target_audience}",
                f"حلول متكاملة وسريعة مع {product_name}",
                f"اكتشف أقوى عروض {product_name} اليوم"
            ],
            "body": [
                "وفر وقتك ومجهودك مع المنصة الأقوى. أسعار تنافسية وجودة مضمونة. احجز الآن.",
                "نقدم لك الدعم الأفضل والنتائج الأسرع. تواصل معنا اليوم لاستشارة مجانية.",
            ],
            "cta": ["احجز الآن", "تواصل معنا مباشرة"],
        }
    }
    
    selected = platforms_styles.get(platform, platforms_styles["Meta (Facebook/Instagram)"])
    
    # Generate 3 variations
    variations = []
    for i in range(3):
        variations.append({
            "headline": random.choice(selected["hooks"]),
            "primary_text": random.choice(selected["body"]),
            "cta": random.choice(selected["cta"])
        })
        
    return variations
