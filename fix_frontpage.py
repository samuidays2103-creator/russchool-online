"""Fix Moodle front page via direct POST request (bypass sortable list JS)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright
import requests
import time

BASE = "http://130.12.47.10"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.set_default_timeout(60000)

    page.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded")
    page.fill("#username", "admin")
    page.fill("#password", "Admin2026!")
    page.click("#loginbtn")
    page.wait_for_url(lambda url: "/login" not in url, timeout=30000)
    print("Logged in")

    # Get sesskey and cookies from browser
    sesskey = page.evaluate("M.cfg.sesskey")
    print("sesskey:", sesskey)

    raw_cookies = ctx.cookies()
    session_cookies = {c["name"]: c["value"] for c in raw_cookies}
    print("Cookies:", list(session_cookies.keys()))

    browser.close()

# Now use requests to POST directly
session = requests.Session()
session.cookies.update(session_cookies)

# POST to frontpagesettings with correct data
# frontpage: '5' = categories (for guests)
# frontpageloggedin: '2' = enrolled courses (for logged-in)
post_data = {
    "sesskey": sesskey,
    "pageurl": f"{BASE}/admin/settings.php?section=frontpagesettings",
    "context": "2",
    "section": "frontpagesettings",
    "action": "save-settings",
    "return": "",
    "s__fullname": "Онлайн-школа",
    "s__shortname": "Школа",
    "s__summary": "",
    "s__maxcategorydepth": "2",
    "s__frontpagecourselimit": "200",
    "s__numsections": "1",
    "s__newsitems": "3",
    "s__commentsperpage": "15",
    "s__defaultfrontpageroleid": "8",
}

# frontpage[] - first = 5 (categories), rest = none
post_data_list = list(post_data.items())
post_data_list.append(("s__frontpage[]", "5"))
post_data_list.append(("s__frontpage[]", "none"))
post_data_list.append(("s__frontpage[]", "none"))
post_data_list.append(("s__frontpage[]", "none"))
post_data_list.append(("s__frontpage[]", "none"))

# frontpageloggedin[] - first = 2 (enrolled), rest = none
post_data_list.append(("s__frontpageloggedin[]", "2"))
post_data_list.append(("s__frontpageloggedin[]", "none"))
post_data_list.append(("s__frontpageloggedin[]", "none"))
post_data_list.append(("s__frontpageloggedin[]", "none"))
post_data_list.append(("s__frontpageloggedin[]", "none"))
post_data_list.append(("s__frontpageloggedin[]", "none"))

resp = session.post(
    f"{BASE}/admin/settings.php",
    data=post_data_list,
    headers={"Referer": f"{BASE}/admin/settings.php?section=frontpagesettings"},
    allow_redirects=True
)
print(f"POST response: {resp.status_code} URL: {resp.url}")
if "changes" in resp.text.lower() or "saved" in resp.text.lower():
    print("Changes saved indicator found")
elif "Settings saved" in resp.text or "Настройки сохранены" in resp.text:
    print("Settings saved!")

# Purge cache via POST
purge_resp = session.post(
    f"{BASE}/admin/purgecaches.php",
    data={"sesskey": sesskey, "confirm": "1"},
    allow_redirects=True
)
print(f"Cache purge: {purge_resp.status_code}")

print("\nNow check http://130.12.47.10/ in browser - should show categories")
print("DONE")
