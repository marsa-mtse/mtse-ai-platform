# ==========================================================
# MTSE Marketing Engine - Authentication Module
# ==========================================================

import hashlib
import secrets
import datetime
import streamlit as st
from database import get_user, create_user, reset_login_attempts, increment_login_attempts, lock_account, is_account_locked
from config import ADMIN_DEFAULT_USERNAME, ADMIN_DEFAULT_PASSWORD, MAX_LOGIN_ATTEMPTS, LOGIN_LOCKOUT_MINUTES


# ==============================
# PASSWORD HASHING (Salted SHA256)
# ==============================

def hash_password(password, salt=None):
    """Hash password with a random salt for security."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(password, stored_hash):
    """Verify a password against the stored salted hash."""
    if "$" not in stored_hash:
        # Legacy: plain SHA256 without salt (backward compatibility)
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    salt, hashed = stored_hash.split("$", 1)
    return hash_password(password, salt) == stored_hash


# ==============================
# SESSION MANAGEMENT
# ==============================

def init_session():
    """Initialize session state for auth."""
    defaults = {
        "logged_in": False,
        "username": None,
        "role": None,
        "plan": "Starter",  # Default free plan on new session
        "lang": "AR"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(username, password):
    """
    Attempt to log in a user.
    Returns: (success: bool, message: str)
    """
    if not username or not password:
        return False, "يرجى إدخال اسم المستخدم وكلمة المرور" if st.session_state.lang == "AR" else "Please enter username and password"

    # Check if account is locked
    if is_account_locked(username):
        return False, f"الحساب مقفل. حاول بعد {LOGIN_LOCKOUT_MINUTES} دقيقة" if st.session_state.lang == "AR" else f"Account locked. Try again after {LOGIN_LOCKOUT_MINUTES} minutes"

    user = get_user(username)

    if user and verify_password(password, user["password"]):
        # Successful login
        st.session_state.logged_in = True
        st.session_state.username = user["username"]
        st.session_state.role = user["role"]
        
        # Map legacy plan names to new tiers
        plan_map = {
            "Explorer": "Starter", "Starter": "Starter",
            "Strategist": "Pro",   "Pro": "Pro",
            "Business": "Command", "Command": "Command"
        }
        db_plan = user.get("plan", "Starter")
        st.session_state.plan = plan_map.get(db_plan, "Starter")
        reset_login_attempts(username)
        return True, "تم تسجيل الدخول بنجاح" if st.session_state.lang == "AR" else "Login Successful"
    else:
        # Failed login
        if user:
            increment_login_attempts(username)
            attempts = (user.get("login_attempts") or 0) + 1
            if attempts >= MAX_LOGIN_ATTEMPTS:
                lock_account(username, LOGIN_LOCKOUT_MINUTES)
                return False, "تم قفل الحساب بسبب محاولات كثيرة" if st.session_state.lang == "AR" else "Account locked due to too many attempts"
        return False, "بيانات الدخول غير صحيحة" if st.session_state.lang == "AR" else "Invalid Credentials"


def logout_user():
    """Log out the current user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.plan = None


def create_default_admin():
    """Create default admin user if it doesn't exist."""
    user = get_user(ADMIN_DEFAULT_USERNAME)
    if not user:
        create_user(
            ADMIN_DEFAULT_USERNAME,
            hash_password(ADMIN_DEFAULT_PASSWORD),
            "admin",
            "Command"  # Admin always gets enterprise
        )


def is_admin():
    """Check if current user is admin."""
    return st.session_state.get("role") == "admin"
