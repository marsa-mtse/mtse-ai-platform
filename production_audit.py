# ==========================================
# MTSE Production Audit - Final Check
# ==========================================
import sys
import os

# Ensure project root is in path
sys.path.append('.')

def audit_production():
    print("="*60)
    print("   MTSE v2.0 PRODUCTION READINESS AUDIT")
    print("="*60)
    
    stages = [
        ("Core Dependencies", ["streamlit", "pandas", "numpy", "PIL", "reportlab"]),
        ("AI Engines", ["ai_engine.campaign_orchestrator", "ai_engine.video_analyzer", "ai_engine.cost_engine"]),
        ("Database Logic", ["database"]),
        ("View Modules", ["views.workspace_page", "views.campaign_page", "views.settings_page", "views.video_intel_page"])
    ]
    
    overall_pass = True
    
    for stage_name, imports in stages:
        print(f"\n[AUDIT] {stage_name}...")
        for imp in imports:
            try:
                __import__(imp)
                print(f"   PASS: {imp}")
            except ImportError as e:
                print(f"   FAIL: {imp} ({str(e)})")
                overall_pass = False
    
    print("\n" + "="*60)
    if overall_pass:
        print("   STATUS: GLOBAL LAUNCH READY")
    else:
        print("   STATUS: BLOCKED - CHECK LOGS")
    print("="*60)

if __name__ == "__main__":
    audit_production()
