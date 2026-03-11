# ==========================================
# MTSE Enterprise Verification - RBAC & Projects
# ==========================================
import sys
import os
import json

# Ensure project root is in path
sys.path.append('.')

from database import init_database, create_project, get_projects, add_project_asset, get_project_assets, is_admin, update_user_role, get_connection

def run_enterprise_verification():
    print("="*60)
    print("   ENTERPRISE SYSTEM VERIFICATION")
    print("="*60)
    
    init_database()
    test_company = "Apex Agency"
    admin_user = "admin_apex"
    editor_user = "editor_apex"
    
    # 1. Setup Test Environment
    print("\n[STEP 1] Setting up Enterprise users & roles...")
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO users (username, password, company, role, created_at) VALUES (?, ?, ?, ?, ?)", 
                 (admin_user, "pass", test_company, "Admin", "now"))
    conn.execute("INSERT OR IGNORE INTO users (username, password, company, role, created_at) VALUES (?, ?, ?, ?, ?)", 
                 (editor_user, "pass", test_company, "Editor", "now"))
    conn.commit()
    
    # 2. Verify RBAC
    print(f"[STEP 2] Verifying Roles...")
    if is_admin(admin_user) and not is_admin(editor_user):
        print("   SUCCESS - RBAC Logic: PASS")
    else:
        print("   FAILURE - RBAC Logic: FAIL")

    # 3. Project Creation
    print(f"[STEP 3] Creating Enterprise Project...")
    create_project("Q3 Strategy", admin_user, test_company, "Main strategy for Q3 2026")
    projects = get_projects(test_company)
    if any(p['name'] == "Q3 Strategy" for p in projects):
        project_id = [p['id'] for p in projects if p['name'] == "Q3 Strategy"][0]
        print(f"   SUCCESS - Project Creation: PASS (ID: {project_id})")
    else:
        print("   FAILURE - Project Creation: FAIL")
        return

    # 4. Asset Integration
    print(f"[STEP 4] Linking AI Assets to Project...")
    mock_asset = {"strategy": "Aggressive Growth", "channels": ["IG", "FB"]}
    add_project_asset(project_id, "campaign", mock_asset, admin_user)
    
    assets = get_project_assets(project_id)
    if assets and assets[0]['asset_type'] == "campaign":
        print(f"   SUCCESS - Asset Linking: PASS")
    else:
        print("   FAILURE - Asset Linking: FAIL")

    print("\n" + "="*60)
    print("   ENTERPRISE ARCHITECTURE VERIFIED")
    print("="*60)

if __name__ == "__main__":
    run_enterprise_verification()
