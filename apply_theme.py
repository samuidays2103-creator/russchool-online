"""
fix_loginform_width.py
Add width:100% to .loginform and hide cookie/language on login.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = "http://130.12.47.10"
os.makedirs("screenshots", exist_ok=True)
LOGO_URL = "https://easydayssamui.com/images/logo.png"

CSS = f"""<style>

/* ═══════════════════════════════════════════
   NAVBAR — logo, hide site name text
═══════════════════════════════════════════ */
.navbar {{
    box-shadow: 0 2px 10px rgba(0,0,0,0.12) !important;
    padding: 4px 16px !important;
}}
.navbar-brand {{
    color: transparent !important;
    text-shadow: none !important;
    display: inline-flex !important;
    align-items: center !important;
}}
.navbar-brand::before {{
    content: '';
    display: inline-block;
    width: 88px;
    height: 46px;
    background: url('{LOGO_URL}') left center / contain no-repeat;
    vertical-align: middle;
}}
.navbar-brand img.logo {{
    max-height: 46px !important;
    width: auto !important;
    display: inline-block !important;
    font-size: 16px !important;
}}

/* ═══════════════════════════════════════════
   LOGIN PAGE
═══════════════════════════════════════════ */
body.pagelayout-login {{
    background: linear-gradient(160deg, #1e3a5f 0%, #E87722 100%) !important;
    min-height: 100vh;
}}
body.pagelayout-login #page-wrapper,
body.pagelayout-login #page,
body.pagelayout-login #page-content {{
    background: transparent !important;
}}
body.pagelayout-login .navbar,
body.pagelayout-login #page-header,
body.pagelayout-login footer,
body.pagelayout-login .footer-popover-container {{
    display: none !important;
}}
body.pagelayout-login #school-login-header {{
    display: flex !important;
}}

/* Card layout */
body.pagelayout-login .login-wrapper {{
    max-width: 460px !important;
    margin: 0 auto !important;
    padding: 0 16px 60px !important;
}}
body.pagelayout-login .login-container {{
    background: white !important;
    border-radius: 20px !important;
    box-shadow: 0 30px 60px rgba(0,0,0,0.3) !important;
    overflow: hidden !important;
    padding: 36px 40px 40px !important;
}}
body.pagelayout-login .login-container::before {{
    content: '';
    display: block;
    height: 5px;
    background: linear-gradient(90deg, #E87722, #c45e10);
    margin: -36px -40px 32px;
    border-radius: 20px 20px 0 0;
}}
/* ✓ KEY FIX: loginform must be full-width */
body.pagelayout-login .loginform {{
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    padding: 0 !important;
    margin: 0 !important;
}}
body.pagelayout-login .loginform .col {{
    flex: 0 0 100% !important;
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
}}

/* ✓ Hide Moodle h1.login-heading "Зайти на..." */
body.pagelayout-login .login-heading {{
    display: none !important;
}}
/* Our heading — ::before on loginform (flex container, so flex item) */
body.pagelayout-login .loginform::before {{
    content: 'Войдите в личный кабинет';
    display: block;
    flex: 0 0 100%;
    font-size: 1.45em;
    font-weight: 700;
    color: #1e3a5f;
    margin-bottom: 24px;
    text-align: center;
    line-height: 1.3;
    font-family: inherit;
}}
/* Inputs */
body.pagelayout-login .form-control {{
    border-radius: 8px !important;
    border: 1.5px solid #dde1e7 !important;
    padding: 10px 14px !important;
    font-size: 1em !important;
    width: 100% !important;
}}
body.pagelayout-login .form-control:focus {{
    border-color: #E87722 !important;
    box-shadow: 0 0 0 3px rgba(232,119,34,0.18) !important;
}}
/* Login button */
body.pagelayout-login #loginbtn {{
    background: linear-gradient(135deg, #E87722 0%, #c45e10 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 1.05em !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}}
body.pagelayout-login #loginbtn:hover {{ opacity: 0.88 !important; }}
body.pagelayout-login a {{ color: #E87722 !important; }}
/* Hide language selector & cookie notice */
body.pagelayout-login .login-languagemenu,
body.pagelayout-login .login-divider ~ .d-flex,
body.pagelayout-login .lang-chooser-container {{
    display: none !important;
}}

/* ═══════════════════════════════════════════
   HERO / LOGIN HEADER visibility
═══════════════════════════════════════════ */
#school-hero {{ display: none !important; }}
#school-login-header {{ display: none !important; }}
body.pagelayout-frontpage #school-hero {{ display: block !important; }}

/* ═══════════════════════════════════════════
   HIDE UNWANTED
═══════════════════════════════════════════ */
.copyright {{ display: none !important; }}
.footer-content-debugging {{ display: none; }}
.moove-container-fluid {{ display: none !important; }}
.btn-footer-popover {{ display: none !important; }}
a[href*="categoryid=2"] {{ display: none !important; }}
li:has(a[href*="categoryid=2"]) {{ display: none !important; }}

/* ═══════════════════════════════════════════
   GENERAL
═══════════════════════════════════════════ */
.btn-primary {{
    background-color: #E87722 !important;
    border-color: #E87722 !important;
}}
.btn-primary:hover {{
    background-color: #c45e10 !important;
    border-color: #c45e10 !important;
}}
.logininfo a {{ color: #E87722 !important; font-weight: 600; }}
.dashboard-card .card-title a,
.coursebox .coursename a {{
    color: #1e3a5f !important;
    font-weight: 600 !important;
}}
.progress-bar {{ background-color: #E87722 !important; }}
.section-title a {{ color: #1e3a5f !important; font-weight: 700 !important; }}

/* ═══════════════════════════════════════════
   MOBILE
═══════════════════════════════════════════ */
@media (max-width: 576px) {{
    body.pagelayout-login #school-login-header {{
        padding: 28px 16px 20px !important;
    }}
    body.pagelayout-login .login-container {{
        padding: 28px 24px 32px !important;
    }}
    body.pagelayout-login .login-container::before {{
        margin: -28px -24px 24px;
    }}
    body.pagelayout-login .loginform::before {{
        font-size: 1.25em !important;
    }}
    #school-hero h1 {{ font-size: 1.7em !important; }}
    #school-hero {{ padding: 36px 16px 30px !important; }}
}}
</style>"""

TOPOFBODY = """<div id="school-hero" style="background:linear-gradient(135deg,#E87722 0%,#c45e10 100%);color:white;text-align:center;padding:48px 20px 40px;margin-bottom:0;">
<p style="font-size:0.95em;opacity:0.85;letter-spacing:2px;text-transform:uppercase;margin:0 0 10px;">Онлайн-школа</p>
<h1 style="font-size:2.4em;margin:0 0 16px;font-weight:700;line-height:1.2;">Русский язык и математика<br>для детей диаспоры</h1>
<p style="font-size:1.1em;opacity:0.9;max-width:520px;margin:0 auto 28px;">Программа «Школа России», 1–4 класс. Группы 3–5 человек.</p>
<a href="/my/" style="background:white;color:#E87722;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.1em;display:inline-block;">Войти в личный кабинет</a>
</div>
<div id="school-login-header" style="flex-direction:column;align-items:center;padding:44px 20px 28px;color:white;text-align:center;">
<img src="/pix/school-logo.png" style="max-height:62px;width:auto;margin-bottom:14px;filter:brightness(0) invert(1);" alt="Онлайн-школа" onerror="this.style.display='none'">
<div style="color:white;font-size:1.8em;margin:0 0 8px;font-weight:700;line-height:1.2;">Онлайн-школа</div>
<div style="color:rgba(255,255,255,0.8);font-size:0.92em;">Русский язык и математика для детей диаспоры</div>
</div>"""

print("Applying loginform width fix...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.set_default_timeout(30000)

    page.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded")
    page.fill("#username", "admin")
    page.fill("#password", "Admin2026!")
    page.click("#loginbtn")
    page.wait_for_url(lambda u: "/login" not in u, timeout=30000)
    print("✓ Logged in")

    page.goto(f"{BASE}/admin/settings.php?section=additionalhtml", wait_until="networkidle")
    page.locator('textarea[name="s__additionalhtmlhead"]').fill(CSS)
    page.locator('textarea[name="s__additionalhtmltopofbody"]').fill(TOPOFBODY)
    page.locator('button:has-text("Save changes")').click()
    page.wait_for_load_state('networkidle')
    print("✓ CSS saved")

    page.goto(f"{BASE}/admin/purgecaches.php", wait_until="networkidle")
    for sel in ['input[type=submit]', 'button[type=submit]']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=3000):
                btn.click()
                page.wait_for_load_state('networkidle')
                print("✓ Caches purged")
                break
        except:
            pass

    time.sleep(3)
    print("\nScreenshots...")

    def shot(name, url, user=None, mobile=False):
        vp = {"width": 390, "height": 844} if mobile else {"width": 1440, "height": 900}
        c = browser.new_context(viewport=vp)
        pg = c.new_page()
        pg.set_default_timeout(30000)
        try:
            if user:
                pg.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded")
                time.sleep(0.8)
                pg.fill("#username", user[0])
                pg.fill("#password", user[1])
                pg.click("#loginbtn")
                pg.wait_for_url(lambda u: "/login" not in u, timeout=25000)
            pg.goto(url)
            pg.wait_for_load_state('networkidle')
            pg.screenshot(path=f"screenshots/{name}.png", full_page=True)
            print(f"  ✓ {name}.png")
        except Exception as e:
            print(f"  ✗ {name}: {type(e).__name__}")
        finally:
            c.close()

    shot("login_desktop",   f"{BASE}/login/index.php")
    shot("login_mobile",    f"{BASE}/login/index.php", mobile=True)
    shot("frontpage_guest", BASE)
    shot("dashboard",       f"{BASE}/my/",                  user=("ivanov_misha", "Test1234!"))
    shot("course",          f"{BASE}/course/view.php?id=2", user=("ivanov_misha", "Test1234!"))

    browser.close()
print("✓ Done!")
