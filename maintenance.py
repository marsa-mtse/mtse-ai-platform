import subprocess
import os
import datetime
import sys

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def perform_maintenance():
    print("="*50)
    print(f"   MTSE v11 AUTO-MAINTENANCE [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print("="*50)

    # 1. Run System Health Check
    print("\n[1/3] Running System Health Check...")
    success, stdout, stderr = run_command("python system_health_check.py")
    if not success:
        print("[FAIL] System Health Check FAILED.")
        print(stderr)
        return False
    
    if "FAIL" in stdout or "ERROR" in stdout:
        print("[FAIL] System Audit detected issues:")
        print(stdout)
        return False
    
    print("[PASS] System Health Check: PASSED")

    # 2. Check for Changes
    print("\n[2/3] Checking for Local Changes...")
    _, status_out, _ = run_command("git status --porcelain")
    if not status_out.strip():
        print("[INFO] No changes to sync. System is up to date.")
        return True
    
    print(f"[EDIT] Changes detected:\n{status_out}")

    # 3. Sync to GitHub
    print("\n[3/3] Synchronizing to GitHub...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    steps = [
        "git add .",
        f'git commit -m "Auto-Maintenance Sync: {timestamp}"',
        "git push origin master --force"
    ]

    for step in steps:
        print(f"   Running: {step}")
        success, stdout, stderr = run_command(step)
        if not success:
            if "nothing to commit" in stderr or "nothing to commit" in stdout:
                continue
            print(f"[FAIL] Failed at step: {step}")
            print(stderr)
            return False
    
    print("[PASS] Successfully synced to GitHub.")
    print("="*50)
    print("   MAINTENANCE COMPLETE")
    print("="*50)
    return True

if __name__ == "__main__":
    if perform_maintenance():
        sys.exit(0)
    else:
        sys.exit(1)
