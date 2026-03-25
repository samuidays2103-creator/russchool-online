"""
tester_light.py — Быстрая проверка текущих open багов.
~2 минуты, ключевые страницы для всех open багов.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = "http://130.12.47.10"
os.makedirs("screenshots", exist_ok=True)


def login(pg, user, pw):
    pg.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded", timeout=30000)
    time.sleep(1)
    pg.evaluate("""() => {
        let el = document.querySelector('#username');
        while (el) { el.style.setProperty('display','block','important'); el.style.setProperty('visibility','visible','important'); el = el.parentElement; }
        ['#password','#loginbtn'].forEach(s => { let e = document.querySelector(s); if(e) { e.style.setProperty('display','block','important'); e.style.setProperty('visibility','visible','important'); }});
    }""")
    time.sleep(0.3)
    pg.fill("#username", user, timeout=10000)
    pg.fill("#password", pw, timeout=10000)
    pg.click("#loginbtn", timeout=10000)
    pg.wait_for_url(lambda u: "/login" not in u, timeout=20000)


print("tester_light.py — current open bugs check")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # === STUDENT DESKTOP ===
    print("\n=== Student Desktop ===")
    try:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.set_default_timeout(25000)
        login(pg, "ivanov_misha", "Test1234!")

        # Dashboard — BUG-026,028,029,039,041,042,051
        pg.goto(f"{BASE}/my/", wait_until="networkidle")
        time.sleep(3)
        pg.screenshot(path="screenshots/light_dashboard_desktop.png", full_page=True)
        pg.screenshot(path="screenshots/light_navbar_desktop.png", clip={"x": 0, "y": 0, "width": 1440, "height": 70})
        print("  dashboard + navbar OK")

        # Course view — BUG-025,035,036,037,038,052,054
        pg.goto(f"{BASE}/course/view.php?id=4", wait_until="networkidle")
        time.sleep(3)
        pg.screenshot(path="screenshots/light_course_desktop.png", full_page=True)
        print("  course view OK")

        # Section page — BUG-035,036,037,038,053
        pg.goto(f"{BASE}/course/section.php?id=21", wait_until="networkidle")
        time.sleep(3)
        pg.screenshot(path="screenshots/light_section_desktop.png", full_page=True)
        print("  section OK")

        # BBB page — BUG-049,050
        pg.goto(f"{BASE}/mod/bigbluebuttonbn/view.php?id=84", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_bbb_desktop.png", full_page=True)
        print("  BBB OK")

        # Grades — BUG-042,051
        pg.goto(f"{BASE}/grade/report/overview/index.php", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_grades_desktop.png", full_page=True)
        print("  grades OK")

        # Profile — BUG-030
        pg.goto(f"{BASE}/user/profile.php", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_profile_desktop.png", full_page=True)
        print("  profile OK")

        # Preferences — BUG-031
        pg.goto(f"{BASE}/user/preferences.php", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_preferences_desktop.png", full_page=True)
        print("  preferences OK")

        ctx.close()
    except Exception as e:
        print(f"  FAIL: {e}")

    # === STUDENT MOBILE ===
    print("\n=== Student Mobile ===")
    try:
        ctx = browser.new_context(viewport={"width": 375, "height": 812}, is_mobile=True)
        pg = ctx.new_page()
        pg.set_default_timeout(25000)
        login(pg, "ivanov_misha", "Test1234!")

        # Dashboard mobile — BUG-040,043,045
        pg.goto(f"{BASE}/my/", wait_until="networkidle")
        time.sleep(3)
        pg.screenshot(path="screenshots/light_dashboard_mobile.png", full_page=True)
        print("  dashboard mobile OK")

        # Course mobile — BUG-046
        pg.goto(f"{BASE}/course/view.php?id=4", wait_until="networkidle")
        time.sleep(3)
        pg.screenshot(path="screenshots/light_course_mobile.png", full_page=True)
        print("  course mobile OK")

        # Forgot password — BUG-032
        pg.goto(f"{BASE}/login/forgot_password.php", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_forgot_mobile.png", full_page=True)
        print("  forgot password mobile OK")

        ctx.close()
    except Exception as e:
        print(f"  FAIL: {e}")

    # === ADMIN ===
    print("\n=== Admin ===")
    try:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.set_default_timeout(25000)
        login(pg, "admin", "Admin2026!")

        # BBB admin — BUG-027
        pg.goto(f"{BASE}/mod/bigbluebuttonbn/view.php?id=84", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_bbb_admin.png", full_page=True)
        print("  BBB admin OK")

        # Navbar on different page — BUG-041
        pg.goto(f"{BASE}/grade/report/grader/index.php?id=2", wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_grades_admin_navbar.png", clip={"x": 0, "y": 0, "width": 1440, "height": 70})
        print("  admin navbar OK")

        ctx.close()
    except Exception as e:
        print(f"  FAIL: {e}")

    # === GUEST ===
    print("\n=== Guest ===")
    try:
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.set_default_timeout(15000)

        # Frontpage — BUG-044
        pg.goto(BASE, wait_until="networkidle")
        time.sleep(2)
        pg.screenshot(path="screenshots/light_frontpage_guest.png", full_page=True)
        pg.screenshot(path="screenshots/light_frontpage_navbar.png", clip={"x": 0, "y": 0, "width": 1440, "height": 70})
        print("  frontpage + navbar OK")

        ctx.close()
    except Exception as e:
        print(f"  FAIL: {e}")

    browser.close()

print("\nDONE — 14 screenshots")
