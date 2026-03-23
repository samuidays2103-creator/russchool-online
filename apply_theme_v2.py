"""
apply_theme_v2.py
Apply UI Redesign v2 to Moodle — based on competitor research (Foxford, Умскул, Skysmart, Khan Academy, Duolingo).
Dark navbar, Golos Text font, warm background, cards hover, course sections, CSS Variables system.
Re-run this script to re-apply all CSS/HTML after cache purge or server reset.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = "http://130.12.47.10"
os.makedirs("screenshots", exist_ok=True)
LOGO_URL = "https://easydayssamui.com/images/logo.png"

CSS = """<!-- Google Fonts: Golos Text (главный) + Nunito (заголовки) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
<style>

/* ═══════════════════════════════════════════
   CSS VARIABLES — единая система цветов
═══════════════════════════════════════════ */
:root {
    --color-primary:      #1e3a5f;
    --color-primary-dark: #152d4a;
    --color-accent:       #E87722;
    --color-accent-dark:  #c45e10;
    --color-bg:           #FAFAF9;
    --color-bg-card:      #FFFFFF;
    --color-border:       #E7E5E4;
    --color-text:         #1C1917;
    --color-text-muted:   #57534E;
    --radius-sm:  8px;
    --radius-md:  12px;
    --radius-lg:  16px;
    --shadow-sm:  0 1px 3px rgba(0,0,0,0.05), 0 2px 8px rgba(0,0,0,0.06);
    --shadow-md:  0 4px 12px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.08);
    --shadow-hover: 0 8px 24px rgba(30,58,95,0.15);
}

/* ═══════════════════════════════════════════
   ШРИФТЫ — Golos Text везде
═══════════════════════════════════════════ */
body, .navbar, .card, .btn, input, select, textarea,
.activity-item, p, li, td, th {
    font-family: 'Golos Text', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
    color: var(--color-text) !important;
}
h1, h2, h3, h4, h5, h6,
.coursename, .sectionname, .card-title,
.h1, .h2, .h3, .h4, .h5, .h6 {
    font-family: 'Nunito', 'Golos Text', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
    color: var(--color-primary) !important;
}

/* ═══════════════════════════════════════════
   ГЛОБАЛЬНЫЙ ФОН — тёплый, не холодный белый
═══════════════════════════════════════════ */
body {
    background-color: var(--color-bg) !important;
}
#page, #page-wrapper, #page-content {
    background-color: var(--color-bg) !important;
}

/* ═══════════════════════════════════════════
   NAVBAR — тёмный, брендовый
═══════════════════════════════════════════ */
.navbar.fixed-top, .navbar {
    background-color: var(--color-primary) !important;
    border-bottom: 3px solid var(--color-accent) !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.2) !important;
    min-height: 56px !important;
    padding: 0 16px !important;
}
/* Логотип EasyDays */
.navbar-brand {
    color: transparent !important;
    text-shadow: none !important;
    display: inline-flex !important;
    align-items: center !important;
    padding: 6px 0 !important;
}
.navbar-brand::before {
    content: '';
    display: inline-block;
    width: 36px;
    height: 36px;
    background: url('https://easydayssamui.com/images/logo.png') center / contain no-repeat;
    flex-shrink: 0;
    filter: brightness(0) invert(1);
}
.navbar-brand img.logo {
    max-height: 36px !important;
    width: auto !important;
    display: inline-block !important;
}
/* Ссылки в navbar */
.navbar .nav-link,
#usernavigation .nav-link,
.navbar .nav-item a {
    color: rgba(255,255,255,0.88) !important;
    font-family: 'Golos Text', sans-serif !important;
    font-weight: 500 !important;
    transition: color 0.15s !important;
}
.navbar .nav-link:hover,
#usernavigation .nav-link:hover {
    color: var(--color-accent) !important;
}
/* Иконки в navbar */
#usernavigation .icon,
.navbar .icon {
    color: rgba(255,255,255,0.88) !important;
    fill: rgba(255,255,255,0.88) !important;
}
/* Dropdown меню пользователя */
.usermenu .dropdown-menu {
    border-top: 3px solid var(--color-accent) !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    box-shadow: var(--shadow-md) !important;
}
/* Исправление scroll overlap */
.secondary-navigation {
    position: relative !important;
    z-index: 1 !important;
}
#page-header {
    position: relative !important;
    z-index: 1 !important;
}

/* ═══════════════════════════════════════════
   КАРТОЧКИ КУРСОВ — dashboard /my/ и /my/courses.php
═══════════════════════════════════════════ */
.block_myoverview .card.course-card,
.card-grid .card.course-card,
[data-region="course-content"] .card {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--color-border) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s !important;
    overflow: hidden !important;
    background: var(--color-bg-card) !important;
}
.block_myoverview .card.course-card:hover,
.card-grid .card.course-card:hover,
[data-region="course-content"] .card:hover {
    transform: translateY(-4px) !important;
    box-shadow: var(--shadow-hover) !important;
    border-color: var(--color-accent) !important;
}
.card.course-card .card-img-top {
    height: 130px !important;
    object-fit: cover !important;
    background-size: cover !important;
    background-position: center !important;
}
.card.course-card .coursename.aalink,
.card.course-card .card-title a {
    color: var(--color-primary) !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 16px !important;
    text-decoration: none !important;
}
.card.course-card .coursename.aalink:hover,
.card.course-card .card-title a:hover {
    color: var(--color-accent) !important;
}
/* Прогресс-бар курса */
.progress { background: #e9ecef !important; border-radius: 99px !important; }
.progress-bar { background-color: var(--color-accent) !important; border-radius: 99px !important; }

/* ═══════════════════════════════════════════
   СТРАНИЦА КУРСА — секции и активности
═══════════════════════════════════════════ */
.course-content .course-section {
    background: var(--color-bg-card) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 12px !important;
    overflow: hidden !important;
}
.course-content .course-section-header {
    background: linear-gradient(135deg, #f0f4f8 0%, #e8edf2 100%) !important;
    border-bottom: 2px solid var(--color-primary) !important;
    padding: 12px 16px !important;
}
.course-content .course-section-header .sectionname,
.course-content .course-section-header h3 {
    color: var(--color-primary) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    margin: 0 !important;
}
.activity-item {
    border-bottom: 1px solid #f0f0f0 !important;
    transition: background 0.15s !important;
    border-radius: 0 !important;
}
.activity-item:last-child { border-bottom: none !important; }
.activity-item:hover { background: #f8f9fa !important; }
.activity-item .activity-name-area a {
    color: var(--color-primary) !important;
    font-weight: 500 !important;
    text-decoration: none !important;
}
.activity-item .activity-name-area a:hover { color: var(--color-accent) !important; }
/* Иконки активностей */
.activityiconcontainer.assessment { background-color: var(--color-accent) !important; }
.activityiconcontainer.content    { background-color: var(--color-primary) !important; }
.activityiconcontainer.communication { background-color: #10B981 !important; }

/* ═══════════════════════════════════════════
   БОКОВАЯ НАВИГАЦИЯ (Course Index Drawer)
═══════════════════════════════════════════ */
#courseindex {
    background: #f8fafc !important;
    border-right: 3px solid var(--color-primary) !important;
}
.courseindex .courseindex-section-title {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: var(--color-primary) !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.courseindex .courseindex-link { color: var(--color-primary) !important; }
.courseindex .courseindex-link:hover {
    color: var(--color-accent) !important;
    background: rgba(232,119,34,0.06) !important;
}
.courseindex .courseindex-item.active,
.courseindex .courseindex-section.active {
    background: rgba(30,58,95,0.07) !important;
    border-left: 3px solid var(--color-accent) !important;
}

/* ═══════════════════════════════════════════
   КНОПКИ — оранжевый везде
═══════════════════════════════════════════ */
.btn-primary, .btn-primary:not(:disabled) {
    background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent-dark) 100%) !important;
    border-color: var(--color-accent) !important;
    color: #fff !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Golos Text', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 2px 8px rgba(232,119,34,0.3) !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
}
.btn-primary:hover:not(:disabled) {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(232,119,34,0.4) !important;
}
.btn-secondary, .btn-outline-primary {
    border-color: var(--color-primary) !important;
    color: var(--color-primary) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Golos Text', sans-serif !important;
    font-weight: 500 !important;
}
.btn-secondary:hover, .btn-outline-primary:hover {
    background: var(--color-primary) !important;
    color: #fff !important;
}

/* ═══════════════════════════════════════════
   ФОРМЫ — скруглённые, оранжевый фокус
═══════════════════════════════════════════ */
.form-control, .form-select {
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid var(--color-border) !important;
    font-family: 'Golos Text', sans-serif !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.form-control:focus, .form-select:focus {
    border-color: var(--color-accent) !important;
    box-shadow: 0 0 0 3px rgba(232,119,34,0.18) !important;
    outline: none !important;
}

/* ═══════════════════════════════════════════
   СТРАНИЦА ВХОДА — полный редизайн
═══════════════════════════════════════════ */
body.pagelayout-login {
    background: linear-gradient(160deg, #1e3a5f 0%, #E87722 100%) !important;
    min-height: 100vh;
}
body.pagelayout-login #page-wrapper,
body.pagelayout-login #page,
body.pagelayout-login #page-content {
    background: transparent !important;
}
body.pagelayout-login .navbar,
body.pagelayout-login #page-header,
body.pagelayout-login footer,
body.pagelayout-login .footer-popover-container {
    display: none !important;
}
body.pagelayout-login #school-login-header {
    display: flex !important;
}
body.pagelayout-login .login-wrapper {
    max-width: 460px !important;
    margin: 0 auto !important;
    padding: 0 16px 60px !important;
}
body.pagelayout-login .login-container {
    background: white !important;
    border-radius: 20px !important;
    box-shadow: 0 30px 60px rgba(0,0,0,0.3) !important;
    overflow: hidden !important;
    padding: 36px 40px 40px !important;
}
body.pagelayout-login .login-container::before {
    content: '';
    display: block;
    height: 5px;
    background: linear-gradient(90deg, #E87722, #c45e10);
    margin: -36px -40px 32px;
    border-radius: 20px 20px 0 0;
}
body.pagelayout-login .loginform {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    padding: 0 !important;
    margin: 0 !important;
}
body.pagelayout-login .loginform .col {
    flex: 0 0 100% !important;
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
}
body.pagelayout-login .login-heading { display: none !important; }
body.pagelayout-login .loginform::before {
    content: 'Войдите в личный кабинет';
    display: block;
    flex: 0 0 100%;
    font-size: 1.45em;
    font-weight: 700;
    color: #1e3a5f;
    margin-bottom: 24px;
    text-align: center;
    line-height: 1.3;
    font-family: 'Nunito', sans-serif;
}
body.pagelayout-login .form-control {
    border-radius: 8px !important;
    border: 1.5px solid #dde1e7 !important;
    padding: 10px 14px !important;
    font-size: 1em !important;
    width: 100% !important;
}
body.pagelayout-login .form-control:focus {
    border-color: #E87722 !important;
    box-shadow: 0 0 0 3px rgba(232,119,34,0.18) !important;
}
body.pagelayout-login #loginbtn {
    background: linear-gradient(135deg, #E87722 0%, #c45e10 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 1.05em !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}
body.pagelayout-login #loginbtn:hover { opacity: 0.88 !important; }
body.pagelayout-login a { color: #E87722 !important; }
body.pagelayout-login .login-languagemenu,
body.pagelayout-login .login-divider ~ .d-flex,
body.pagelayout-login .lang-chooser-container {
    display: none !important;
}

/* ═══════════════════════════════════════════
   HERO / LOGIN HEADER
═══════════════════════════════════════════ */
#school-hero { display: none !important; }
#school-login-header { display: none !important; }
body.pagelayout-frontpage #school-hero { display: block !important; }

/* ═══════════════════════════════════════════
   СКРЫТЬ НЕНУЖНОЕ
═══════════════════════════════════════════ */
.copyright { display: none !important; }
.footer-content-debugging { display: none; }
.moove-container-fluid { display: none !important; }
.btn-footer-popover { display: none !important; }
a[href*="categoryid=2"] { display: none !important; }
li:has(a[href*="categoryid=2"]) { display: none !important; }

/* ═══════════════════════════════════════════
   DASHBOARD — страница /my/
═══════════════════════════════════════════ */
/* Приветственный блок */
.block_myoverview .block-header,
[data-block="myoverview"] .card-header {
    background: var(--color-primary) !important;
    color: white !important;
    border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
}
/* Навигация внутри блока "Мои курсы" */
.block_myoverview .nav-link.active {
    background: var(--color-accent) !important;
    color: #fff !important;
    border-radius: var(--radius-sm) !important;
}
/* Пустое состояние */
.block_myoverview .empty-placeholder {
    color: var(--color-text-muted) !important;
    font-style: italic !important;
}

/* ═══════════════════════════════════════════
   ОЦЕНКИ — таблица журнала
═══════════════════════════════════════════ */
.gradeparent table,
.generaltable {
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    border: 1px solid var(--color-border) !important;
    box-shadow: var(--shadow-sm) !important;
}
.gradeparent table thead th,
.generaltable thead th {
    background: var(--color-primary) !important;
    color: white !important;
    font-family: 'Golos Text', sans-serif !important;
    font-weight: 600 !important;
}
.generaltable tbody tr:hover { background: #f8f9fa !important; }

/* ═══════════════════════════════════════════
   МОБИЛЬНАЯ АДАПТАЦИЯ
═══════════════════════════════════════════ */
@media (max-width: 575.98px) {
    body { font-size: 14px !important; }
    .card-grid .col {
        flex: 0 0 100% !important;
        max-width: 100% !important;
    }
    .card.course-card .card-img-top { height: 90px !important; }
    #page { overflow-x: hidden !important; }

    body.pagelayout-login #school-login-header {
        padding: 28px 16px 20px !important;
    }
    body.pagelayout-login .login-container {
        padding: 28px 24px 32px !important;
    }
    body.pagelayout-login .login-container::before {
        margin: -28px -24px 24px;
    }
    body.pagelayout-login .loginform::before {
        font-size: 1.25em !important;
    }
    #school-hero h1 { font-size: 1.7em !important; }
    #school-hero { padding: 36px 16px 30px !important; }
}

@media (min-width: 576px) and (max-width: 991.98px) {
    .card-grid .col {
        flex: 0 0 50% !important;
        max-width: 50% !important;
    }
}

/* ═══════════════════════════════════════════
   ОБЩЕЕ
═══════════════════════════════════════════ */
.logininfo a { color: var(--color-accent) !important; font-weight: 600 !important; }
.dashboard-card .card-title a,
.coursebox .coursename a {
    color: var(--color-primary) !important;
    font-weight: 600 !important;
}
.section-title a { color: var(--color-primary) !important; font-weight: 700 !important; }
a { color: var(--color-primary) !important; }
a:hover { color: var(--color-accent) !important; }

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

print("Applying UI Redesign v2 (based on competitor research)...")
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
    purged = False
    for sel in ['input[type=submit]', 'button[type=submit]']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=3000):
                btn.click()
                page.wait_for_load_state('networkidle')
                print("✓ Caches purged")
                purged = True
                break
        except:
            pass
    if not purged:
        time.sleep(5)
        try:
            page.reload(wait_until="networkidle")
            btn = page.locator('input[type=submit]').first
            if btn.is_visible(timeout=3000):
                btn.click()
                page.wait_for_load_state('networkidle')
                print("✓ Caches purged (retry)")
        except Exception as e:
            print(f"  ! Cache purge skipped: {e}")

    time.sleep(3)
    print("\nScreenshots...")

    def shot(name, url, user=None, mobile=False, scroll_y=0):
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
            if scroll_y:
                pg.evaluate(f"window.scrollTo(0, {scroll_y})")
                time.sleep(0.5)
            pg.screenshot(path=f"screenshots/{name}.png", full_page=(scroll_y == 0))
            print(f"  ✓ {name}.png")
        except Exception as e:
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
        finally:
            c.close()

    shot("login_desktop",   f"{BASE}/login/index.php")
    shot("login_mobile",    f"{BASE}/login/index.php", mobile=True)
    shot("dashboard",       f"{BASE}/my/",                  user=("ivanov_misha", "Test1234!"))
    shot("course",          f"{BASE}/course/view.php?id=2", user=("ivanov_misha", "Test1234!"))
    shot("navbar_scroll",   f"{BASE}/my/courses.php",       user=("ivanov_misha", "Test1234!"), scroll_y=300)
    shot("course_mobile",   f"{BASE}/course/view.php?id=2", user=("ivanov_misha", "Test1234!"), mobile=True)

    browser.close()
print("✓ Done!")
