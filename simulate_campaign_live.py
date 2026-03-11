# ==========================================
# MTSE Campaign Simulation - High Fidelity Demo
# ==========================================
import sys
import os
import json
import time

# Ensure project root is in path
sys.path.append('.')

def run_simulation():
    print("="*60)
    print("   MTSE CAMPAIGN ORCHESTRATOR - STRATEGIC DEMO")
    print("="*60)
    
    product = "Eco-Smart Zen Bottle (Sustainability + Tracking Tech)"
    audience = "Urban Professionals & Health Enthusiasts"
    goal = "Global Market Launch"
    budget = "$5,000 / Month"

    print(f"\n[STEP 1] Initializing Strategic Engine...")
    time.sleep(1)
    print(f"        -> Engine: Gemini 1.5 Pro (Strategic Mode)")
    
    print(f"\n[STEP 2] Planning Cross-Platform Strategy for: {product}")
    print(f"        -> Audience: {audience}")
    print("\n[AI ANALYZING...] Identifying market gaps, retention hooks, and visual language...")
    
    # Simulate AI processing time
    for i in range(3):
        print("          . . . processing . . .")
        time.sleep(1)

    # Simulated high-quality output matching our Pydantic schema
    result = {
        "campaign_name": "Zen Hydration: The Future of Sustainable Wellness",
        "target_audience": "Healthy urban professionals valuing tech-connected sustainability.",
        "funnel_strategy": {
            "awareness": "Awareness Campaign on Reels/TikTok highlighting plastic impact and tracking features.",
            "consideration": "Instagram 'Zen Secrets' series focusing on build quality and app integration.",
            "conversion": "Exclusive Early Bird offer and Lifetime Warranty to ensure brand loyalty."
        },
        "platform_content": [
            {
                "platform": "Instagram",
                "headline": "Elevate Your Health with Zen Bottle",
                "body": "One bottle, eternal impact. Track your hydration in real-time and save the planet.",
                "call_to_action": "Shop Now - 20% OFF"
            },
            {
                "platform": "TikTok",
                "headline": "The Bottle That Talks to Your Thirst!",
                "body": "The 30-Day Hydration Challenge starts here. Are you ready to level up?",
                "call_to_action": "Join the Challenge"
            }
        ],
        "visual_prompts": [
            {
                "platform": "Midjourney/DALL-E",
                "concept": "Abstract nature + technology hybrid",
                "prompt": "Cinematic shot of a sleek matte green smart water bottle on a clean wooden desk, morning sunlight streaming through green leaves, tech-hologram representation of water levels floating around it, 8k, hyper-realistic, peaceful zen atmosphere."
            }
        ],
        "suggested_budget_allocation": {
            "Instagram Ads": "35%",
            "TikTok Ads": "45%",
            "Google SEO/SEM": "20%"
        },
        "overall_roadmap": "Week 1: Awareness Launch. Week 2: Influencer Activation. Week 3-4: Retargeting for Conversions."
    }

    print("\n" + "*" * 40)
    print(f"  CAMPAIGN: {result['campaign_name']}")
    print("*" * 40)
    
    print(f"\n[1. TARGET AUDIENCE ANALYSIS]")
    print(result['target_audience'])
    
    print(f"\n[2. SALES FUNNEL STRATEGY]")
    print(f"Awareness: {result['funnel_strategy']['awareness']}")
    print(f"Consideration: {result['funnel_strategy']['consideration']}")
    print(f"Conversion: {result['funnel_strategy']['conversion']}")
    
    print(f"\n[3. SAMPLE PLATFORM CONTENT]")
    for post in result['platform_content']:
        print(f"--- Platform: {post['platform']} ---")
        print(f"Headline: {post['headline']}")
        print(f"Body: {post['body']}")
        print(f"CTA: {post['call_to_action']}")
    
    print(f"\n[4. CREATIVE DIRECTIVES (AI Prompting)]")
    for art in result['visual_prompts']:
        print(f"Concept: {art['concept']}")
        print(f"Prompt (Copy-Paste to Midjourney): {art['prompt']}")
        
    print(f"\n[5. BUDGET ALLOCATION]")
    for plat, alloc in result['suggested_budget_allocation'].items():
        print(f"- {plat}: {alloc}")
        
    print(f"\n[6. STRATEGIC ROADMAP]")
    print(result['overall_roadmap'])
    
    print("\n" + "="*60)
    print("   [SUCCESS] SIMULATION COMPLETED: ALL SYSTEMS READY")
    print("="*60)

if __name__ == "__main__":
    run_simulation()
