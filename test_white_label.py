import sys
sys.path.append('.')
import base64
from database import init_database, update_user_branding, get_user_branding
from utils import generate_branded_pdf

# 1. Initialize DB to ensure columns exist
print("--- Initializing DB ---")
init_database()

# 2. Mock User Data
username = "test_user_white_label"
from database import get_connection
conn = get_connection()
conn.execute("INSERT OR IGNORE INTO users (username, password, created_at) VALUES (?, ?, ?)", (username, "pass", "now"))
conn.commit()

brand_name = "Golden Marketing Agency"
brand_color = "#FFD700" # Gold
# Small transparent PNG pixel in base64 as mock logo
logo_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

print(f"--- Setting Branding for {username} ---")
update_user_branding(username, brand_name, logo_b64, brand_color)

# 3. Retrieve and Verify
brand = get_user_branding(username)
print(f"Retrieved Brand: {brand}")
assert brand['name'] == brand_name
assert brand['color'] == brand_color
assert brand['logo'] == logo_b64

# 4. Target PDF Generation
print("--- Generating Branded PDF ---")
report_data = {
    "title": "Verification Report",
    "sections": [
        {"heading": "Testing Section", "content": "This is a branded test content."}
    ]
}

pdf_bytes = generate_branded_pdf(report_data, brand_data=brand)
if pdf_bytes:
    with open("test_branded_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("PDF Generated successfully: test_branded_report.pdf")
else:
    print("PDF Generation failed.")
