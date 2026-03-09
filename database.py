# ==========================================================
# MTSE Marketing Engine - Database Module
# ==========================================================

import sqlite3
import datetime
import streamlit as st


@st.cache_resource
def get_connection():
    """Create a cached database connection."""
    conn = sqlite3.connect("mtse_saas.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize all database tables."""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Viewer',
            plan TEXT NOT NULL DEFAULT 'Starter',
            reports_used INTEGER DEFAULT 0,
            uploads_used INTEGER DEFAULT 0,
            login_attempts INTEGER DEFAULT 0,
            locked_until TEXT,
            company TEXT,
            billing_status TEXT DEFAULT 'Active',
            expiry_date TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Reports archive
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            file_name TEXT,
            created_at TEXT,
            summary TEXT,
            pdf_data BLOB,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    # Activity log
    c.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    # Teams table
    c.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            owner TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (owner) REFERENCES users(username)
        )
    """)

    # CRM Leads table
    c.execute("""
        CREATE TABLE IF NOT EXISTS crm_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            company TEXT,
            status TEXT DEFAULT 'New',
            created_at TEXT
        )
    """)

    conn.commit()


# ==============================
# HELPER FUNCTIONS
# ==============================

def log_activity(username, action):
    """Log a user activity."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO activity_log (username, action, timestamp) VALUES (?, ?, ?)",
        (username, action, datetime.datetime.now().isoformat())
    )
    conn.commit()


def get_user(username):
    """Get a user by username."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    return dict(row) if row else None


def get_all_users():
    """Get all users."""
    conn = get_connection()
    rows = conn.execute("SELECT username, role, plan, company, billing_status FROM users").fetchall()
    return [dict(r) for r in rows]


def create_user(username, hashed_password, role, plan):
    """Create a new user. Returns True on success, False if user exists."""
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO users (username, password, role, plan, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (username, hashed_password, role, plan, datetime.datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def update_password(username, hashed_password):
    """Update a user's password."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hashed_password, username)
    )
    conn.commit()


def update_plan(username, new_plan):
    """Update a user's plan."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET plan=?, billing_status='Active', expiry_date=? WHERE username=?",
        (new_plan, (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(), username)
    )
    conn.commit()


def get_usage(username):
    """Get usage stats for a user."""
    conn = get_connection()
    row = conn.execute(
        "SELECT reports_used, uploads_used FROM users WHERE username=?",
        (username,)
    ).fetchone()
    return dict(row) if row else {"reports_used": 0, "uploads_used": 0}


def increment_uploads(username):
    """Increment upload counter."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET uploads_used = uploads_used + 1 WHERE username=?",
        (username,)
    )
    conn.commit()


def increment_reports(username):
    """Increment report counter."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET reports_used = reports_used + 1 WHERE username=?",
        (username,)
    )
    conn.commit()


def save_report(username, file_name, summary, pdf_data):
    """Save a report to the archive."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO reports (username, file_name, created_at, summary, pdf_data)
           VALUES (?, ?, ?, ?, ?)""",
        (username, file_name, datetime.datetime.now().isoformat(), summary, pdf_data)
    )
    conn.commit()


def get_user_reports(username):
    """Get all reports for a user."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, file_name, created_at, summary FROM reports WHERE username=? ORDER BY created_at DESC",
        (username,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_report_pdf(report_id):
    """Get PDF data for a specific report."""
    conn = get_connection()
    row = conn.execute(
        "SELECT pdf_data FROM reports WHERE id=?", (report_id,)
    ).fetchone()
    return row["pdf_data"] if row else None


def get_activity_log(limit=50):
    """Get recent activity logs."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT username, action, timestamp FROM activity_log ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def reset_usage_if_new_month(username):
    """Reset usage counters if it's a new billing month."""
    conn = get_connection()
    row = conn.execute(
        "SELECT created_at FROM users WHERE username=?", (username,)
    ).fetchone()

    if row:
        created_date = datetime.datetime.fromisoformat(row["created_at"])
        now = datetime.datetime.now()

        if created_date.month != now.month or created_date.year != now.year:
            conn.execute(
                """UPDATE users SET reports_used=0, uploads_used=0, created_at=?
                   WHERE username=?""",
                (now.isoformat(), username)
            )
            conn.commit()


def increment_login_attempts(username):
    """Increment failed login attempts."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET login_attempts = login_attempts + 1 WHERE username=?",
        (username,)
    )
    conn.commit()


def reset_login_attempts(username):
    """Reset login attempts on successful login."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE username=?",
        (username,)
    )
    conn.commit()


def lock_account(username, minutes=15):
    """Lock account for specified minutes."""
    conn = get_connection()
    lock_until = (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).isoformat()
    conn.execute(
        "UPDATE users SET locked_until=? WHERE username=?",
        (lock_until, username)
    )
    conn.commit()


def is_account_locked(username):
    """Check if account is locked."""
    user = get_user(username)
    if user and user.get("locked_until"):
        lock_time = datetime.datetime.fromisoformat(user["locked_until"])
        if datetime.datetime.now() < lock_time:
            return True
        else:
            reset_login_attempts(username)
    return False


# ==============================
# CRM HELPERS
# ==============================

def add_lead(name, email, company):
    """Add a CRM lead."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO crm_leads (name, email, company, status, created_at)
           VALUES (?, ?, ?, 'New', ?)""",
        (name, email, company, datetime.datetime.now().isoformat())
    )
    conn.commit()


def get_all_leads():
    """Get all CRM leads."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, email, company, status, created_at FROM crm_leads ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def update_lead_status(lead_id, status):
    """Update CRM lead status."""
    conn = get_connection()
    conn.execute(
        "UPDATE crm_leads SET status=? WHERE id=?",
        (status, lead_id)
    )
    conn.commit()


# ==============================
# TEAM HELPERS
# ==============================

def create_team(company, owner):
    """Create a team."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO teams (company, owner, created_at) VALUES (?, ?, ?)",
        (company, owner, datetime.datetime.now().isoformat())
    )
    conn.commit()


def assign_user_to_company(username, company):
    """Assign a user to a company."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET company=? WHERE username=?",
        (company, username)
    )
    conn.commit()


def get_user_company(username):
    """Get the company a user belongs to."""
    user = get_user(username)
    return user.get("company") if user else None
