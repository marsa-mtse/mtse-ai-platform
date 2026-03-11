# ==========================================================
# MTSE Marketing Engine - Database Module
# ==========================================================

import sqlite3
import datetime
import streamlit as st
import threading
import json

try:
    import psycopg2
    from psycopg2.extras import DictCursor
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


class DBWrapper:
    """Wrapper to support both SQLite and PostgreSQL natively without ORM rewrites."""
    
    def __init__(self):
        # Allow passing connection string via st.secrets
        self.db_url = None
        try:
            self.db_url = st.secrets.get("DATABASE_URL")
        except Exception:
            pass
        self.is_postgres = bool(self.db_url and HAS_PSYCOPG2 and self.db_url.startswith("postgres"))
        
        if self.is_postgres:
            self.conn = psycopg2.connect(self.db_url)
        else:
            self.conn = sqlite3.connect("mtse_saas.db", check_same_thread=False)
            self.conn.row_factory = sqlite3.Row

    def execute(self, sql, params=()):
        if self.is_postgres:
            # Adapt SQLite syntax to Postgres automatically
            sql = sql.replace("?", "%s")
            sql = sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            sql = sql.replace("BLOB", "BYTEA")
            
            cursor = self.conn.cursor(cursor_factory=DictCursor)
            try:
                cursor.execute(sql, params)
            except Exception as e:
                self.conn.rollback()
                raise e
            return cursor
        else:
            return self.conn.execute(sql, params)

    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()


# Store a thread-local connection for the request lifecycle, or use Streamlit's cache
_local = threading.local()

def get_connection():
    """Create or retrieve a database connection."""
    if not hasattr(_local, "db_conn") or getattr(_local, "db_conn") is None:
        _local.db_conn = DBWrapper()
    return _local.db_conn


def init_database():
    """Initialize all database tables."""
    conn = get_connection()

    # Users table
    conn.execute("""
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
            brand_name TEXT,
            brand_logo_base64 TEXT,
            brand_color TEXT DEFAULT '#1a73e8',
            stripe_customer_id TEXT,
            subscription_id TEXT,
            subscription_status TEXT DEFAULT 'Inactive',
            plan_expiry TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Reports archive
    conn.execute("""
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    # Teams table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            owner TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (owner) REFERENCES users(username)
        )
    """)

    # CRM Leads table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS crm_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            company TEXT,
            status TEXT DEFAULT 'New',
            created_at TEXT
        )
    """)

    # --- ENTERPRISE EXTENSIONS ---
    
    # Projects table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            owner TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (owner) REFERENCES users (username)
        )
    """)
    
    # Project assets table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS project_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            asset_type TEXT NOT NULL,
            asset_data TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
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
    except Exception:
        # Catch both sqlite3.IntegrityError and psycopg2.IntegrityError
        conn.conn.rollback() # Important for Postgres
        return False


def update_password(username, hashed_password):
    """Update a user's password."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hashed_password, username)
    )
    conn.commit()


def update_plan(username, new_plan, stripe_sub_id=None, stripe_cus_id=None, status='Active'):
    """Update a user's plan and subscription details."""
    conn = get_connection()
    expiry = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
    conn.execute(
        """UPDATE users SET 
           plan=?, 
           billing_status=?, 
           expiry_date=?, 
           subscription_id=?, 
           stripe_customer_id=?, 
           subscription_status=?
           WHERE username=?""",
        (new_plan, status, expiry, stripe_sub_id, stripe_cus_id, status, username)
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


def update_user_branding(username, brand_name, logo_base64, brand_color):
    """Update user branding settings."""
    conn = get_connection()
    conn.execute(
        "UPDATE users SET brand_name=?, brand_logo_base64=?, brand_color=? WHERE username=?",
        (brand_name, logo_base64, brand_color, username)
    )
    conn.commit()


def get_user_branding(username):
    """Get user branding settings with defaults."""
    user = get_user(username)
    if user:
        return {
            "name": user.get("brand_name") or "MTSE AI Platform",
            "logo": user.get("brand_logo_base64"),
            "color": user.get("brand_color") or "#1a73e8"
        }
# ==============================
# PROJECT & TEAM HELPERS (ENTERPRISE)
# ==============================

def create_project(name, owner, company, description=""):
    """Create a new enterprise project."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO projects (name, owner, company, description, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, owner, company, description, datetime.datetime.now().isoformat())
    )
    conn.commit()

def get_projects(company):
    """Retrieve all projects for a company."""
    conn = get_connection()
    return conn.execute("SELECT * FROM projects WHERE company = ? ORDER BY created_at DESC", (company,)).fetchall()

def add_project_asset(project_id, asset_type, asset_data, created_by):
    """Link an AI report or strategy to a project."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO project_assets (project_id, asset_type, asset_data, created_by, created_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, asset_type, json.dumps(asset_data), created_by, datetime.datetime.now().isoformat())
    )
    conn.commit()

def get_project_assets(project_id):
    """Retrieve all assets for a project."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM project_assets WHERE project_id = ? ORDER BY created_at DESC", (project_id,)).fetchall()
    assets = []
    for row in rows:
        d = dict(row)
        try:
            d['asset_data'] = json.loads(d['asset_data'])
        except:
            pass
        assets.append(d)
    return assets

def get_company_members(company):
    """List all users belonging to the same company."""
    conn = get_connection()
    return conn.execute("SELECT username, role, plan FROM users WHERE company = ?", (company,)).fetchall()

def update_user_role(username, role):
    """Update a user's RBAC role."""
    conn = get_connection()
    conn.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
    conn.commit()

def is_admin(username):
    """Check if user has Admin privileges."""
    user = get_user(username)
    return user.get("role") == "Admin" if user else False
