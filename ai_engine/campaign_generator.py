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
        h = random.choice(selected["hooks"])
        b = random.choice(selected["body"])
        c = random.choice(selected["cta"])
        
        variations.append({
            "headline": h,
            "primary_text": b,
            "cta": c,
            "platform": platform
        })
        
    return variations

def get_social_preview_css():
    """Returns CSS for a modern social media post preview."""
    return """
    <style>
    .social-preview-card {
        background: white;
        color: #1c1e21;
        border-radius: 8px;
        max-width: 400px;
        margin: 20px auto;
        font-family: Arial, sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        overflow: hidden;
        border: 1px solid #dddfe2;
    }
    .social-header {
        padding: 12px;
        display: flex;
        align-items: center;
    }
    .profile-pic {
        width: 40px;
        height: 40px;
        background: #6366f1;
        border-radius: 50%;
        margin-right: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    .profile-info {
        flex-grow: 1;
    }
    .profile-name {
        font-weight: bold;
        font-size: 14px;
        color: #1c1e21;
    }
    .post-time {
        font-size: 12px;
        color: #606770;
    }
    .post-content {
        padding: 12px;
        font-size: 14px;
        line-height: 1.4;
    }
    .post-headline {
        font-weight: bold;
        padding: 10px 12px;
        background: #f0f2f5;
        border-top: 1px solid #dddfe2;
        font-size: 16px;
    }
    .post-cta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 12px;
        background: #f0f2f5;
        border-top: 1px solid #dddfe2;
    }
    .cta-button {
        background: #e4e6eb;
        color: #050505;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
    }
    .social-media-placeholder {
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255,255,255,0.8);
        font-size: 1.5rem;
    }
    </style>
    """

def render_preview_html(variation, username="MTSE"):
    """Generates the HTML for the social media preview."""
    return f"""
    <div class="social-preview-card">
        <div class="social-header">
            <div class="profile-pic">{username[0]}</div>
            <div class="profile-info">
                <div class="profile-name">{username}</div>
                <div class="post-time">Sponsored · 🌐</div>
            </div>
        </div>
        <div class="post-content">
            {variation['primary_text']}
        </div>
        <div class="social-media-placeholder">
            🖼️ Media Visual
        </div>
        <div class="post-headline">
            {variation['headline']}
        </div>
        <div class="post-cta">
            <span style="color:#606770; font-size:12px;">WWW.MTSE.COM</span>
            <div class="cta-button">{variation['cta']}</div>
        </div>
    </div>
    """
