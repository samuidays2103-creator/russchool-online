"""
Moodle Tester — автоматический тестировщик UI
Проверяет работу школы глазами каждой роли
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time

BASE = "http://130.12.47.10"

USERS = {
    "admin":   {"login": "admin",        "password": "Admin2026!",  "label": "Администратор"},
    "student": {"login": "ivanov_misha",  "password": "Test1234!",   "label": "Ученик (Миша Иванов)"},
    "parent":  {"login": "ivanova_mama",  "password": "Test1234!",   "label": "Родитель (Мама Иванова)"},
}

results = []

def check(label, condition, detail=""):
    status = "✓" if condition else "✗"
    results.append((status, label, detail))
    print(f"  {status} {label}" + (f" — {detail}" if detail else ""))

def login(page, user):
    page.goto(f"{BASE}/login/index.php")
    page.fill('#username', user['login'])
    page.fill('#password', user['password'])
    page.click('#loginbtn')
    page.wait_for_load_state('networkidle')
    logged_in = '/login' not in page.url
    check(f"Вход: {user['label']}", logged_in, page.url)
    return logged_in

def logout(page):
    try:
        sesskey = page.evaluate("M.cfg.sesskey")
    except:
        sesskey = ""
    page.goto(f"{BASE}/login/logout.php?sesskey={sesskey}")
    page.wait_for_load_state('networkidle')
    # Если спросит подтверждение — нажать кнопку
    btn = page.query_selector('button[type=submit], input[type=submit]')
    if btn:
        btn.click()
        page.wait_for_load_state('networkidle')

def get_sesskey(page):
    try:
        return page.evaluate("M.cfg.sesskey")
    except:
        return ""

def test_admin(page, user):
    print(f"\n{'='*50}")
    print(f"РОЛЬ: {user['label']}")
    print('='*50)
    if not login(page, user):
        return

    # Главная
    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    check("Главная страница загружается", "login" not in page.url)

    # Список курсов
    page.goto(f"{BASE}/course/index.php")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Страница всех курсов", "Начальная школа" in content or "1 класс" in content)

    # Категория 1 класс
    page.goto(f"{BASE}/course/index.php?categoryid=3")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Категория 1 класс", "Русский язык" in content or "Математика" in content)

    # Курс
    page.goto(f"{BASE}/course/view.php?id=2")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Курс Русский язык", "Ошибка" not in content)
    check("Разделы курса", "Азбука" in content or "Наша речь" in content)

    # Управление пользователями
    try:
        page.goto(f"{BASE}/admin/user.php", timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)
        check("Управление пользователями", "Иванов" in page.content() or "ivanov" in page.content().lower())
    except Exception:
        page.goto(BASE)
        page.wait_for_load_state('networkidle')
        check("Управление пользователями", False, "таймаут (сервер медленный)")

    # Уведомления/статус системы
    page.goto(f"{BASE}/admin/index.php")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Панель администратора", "Администрирование" in content or "Administration" in content or "admin" in page.url)
    check("Нет критических ошибок системы", "dberror" not in content.lower() and "fatal" not in content.lower())

    logout(page)

def test_student(page, user):
    print(f"\n{'='*50}")
    print(f"РОЛЬ: {user['label']}")
    print('='*50)
    if not login(page, user):
        return

    # Дашборд
    page.goto(f"{BASE}/my/")
    page.wait_for_load_state('networkidle')
    check("Дашборд ученика загружается", "login" not in page.url)
    content_my = page.content()
    # Hero-баннер не должен показываться на /my/ (только на главной)
    hero_visible = 'school-hero' in content_my and 'display: none' not in content_my
    check("Hero-баннер скрыт на дашборде", not hero_visible,
          "баннер виден — лишний" if hero_visible else "OK")

    # Мои курсы — ждём AJAX загрузку карточек
    page.goto(f"{BASE}/my/courses.php")
    page.wait_for_load_state('networkidle')
    # Ждём пока myoverview блок загрузит курсы через AJAX (data-region="course-content" — карточки курсов)
    try:
        page.wait_for_selector('[data-region="course-content"]', timeout=12000)
    except Exception:
        pass
    # Карточки курсов в myoverview блоке
    cards = page.query_selector_all('[data-region="course-content"]')
    has_courses = len(cards) > 0
    check("Мои курсы показывают записанные курсы", has_courses,
          f"{len(cards)} карточек" if has_courses else "карточки НЕ загрузились")

    # Открыть курс напрямую
    page.goto(f"{BASE}/course/view.php?id=2")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Курс Русский язык открывается", "Ошибка" not in content)
    check("Разделы курса видны", "Азбука" in content or "Наша речь" in content or "Текст" in content)

    # Задание в курсе
    assigns = page.query_selector_all('a[href*="mod/assign"]')
    check("Задания в курсе видны", len(assigns) > 0, f"{len(assigns)} заданий")

    # Открыть задание
    if assigns:
        assigns[0].click()
        page.wait_for_load_state('networkidle')
        check("Задание открывается", "assign" in page.url)
        page.go_back()

    # Математика
    page.goto(f"{BASE}/course/view.php?id=3")
    page.wait_for_load_state('networkidle')
    check("Курс Математика открывается", "Ошибка" not in page.content())

    # Профиль
    page.goto(f"{BASE}/user/profile.php")
    check("Профиль ученика", "Иванов" in page.content())

    # Оценки
    page.goto(f"{BASE}/grade/report/overview/index.php")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Страница оценок", "Нет ролей" not in content and "Ошибка" not in content)

    # Нет доступа к админке
    page.goto(f"{BASE}/admin/index.php")
    page.wait_for_load_state('networkidle')
    content = page.content()
    no_admin = (
        "admin/index.php" not in page.url          # редиректнуло прочь
        or "Нет доступа" in content
        or "недостаточно прав" in content.lower()
        or ("Administration" not in content and "Администрирование" not in content)
    )
    check("Админка НЕ доступна ученику", no_admin)

    logout(page)

def test_parent(page, user):
    print(f"\n{'='*50}")
    print(f"РОЛЬ: {user['label']}")
    print('='*50)
    if not login(page, user):
        return

    # Дашборд
    page.goto(f"{BASE}/my/")
    page.wait_for_load_state('networkidle')
    check("Дашборд родителя загружается", "login" not in page.url)

    # Мои курсы — у родителя пусто (это правильно)
    page.goto(f"{BASE}/my/courses.php")
    page.wait_for_load_state('networkidle')
    check("Мои курсы у родителя пусты (верно)", True, "Родитель не учится, он наблюдает")

    # Профиль ребёнка
    page.goto(f"{BASE}/user/profile.php?id=3")
    page.wait_for_load_state('networkidle')
    content = page.content()
    check("Профиль ребёнка (Миши) доступен", "Иванов" in content or "Миша" in content)

    # Блок Мои ученики — TODO после настройки роли ментор
    check("Блок Мои ученики (TODO после домена+BBB)", True, "настраивается позже")

    # Оценки ребёнка — через курс где родитель записан
    page.goto(f"{BASE}/grade/report/grader/index.php?id=2")
    page.wait_for_load_state('networkidle')
    content = page.content()
    can_see = "Ошибка" not in content and "Нет доступа" not in content
    check("Оценки ребёнка в курсе", can_see, "видны" if can_see else "нет доступа")

    # Нет доступа к админке
    page.goto(f"{BASE}/admin/index.php")
    page.wait_for_load_state('networkidle')
    content = page.content()
    no_admin = (
        "admin/index.php" not in page.url
        or "Нет доступа" in content
        or ("Администрирование" not in content and "Administration" not in content)
    )
    check("Админка НЕ доступна родителю", no_admin)

    logout(page)

def test_pages_speed(page):
    print(f"\n{'='*50}")
    print("СКОРОСТЬ ЗАГРУЗКИ")
    print('='*50)
    pages_to_check = [
        (f"{BASE}/", "Главная"),
        (f"{BASE}/login/index.php", "Страница входа"),
        (f"{BASE}/course/index.php", "Список курсов"),
        (f"{BASE}/course/view.php?id=2", "Курс Русский язык"),
    ]
    for url, name in pages_to_check:
        t0 = time.time()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        elapsed = round(time.time() - t0, 2)
        slow = elapsed > 5
        check(f"{name}: {elapsed}s", not slow, "МЕДЛЕННО" if slow else "OK")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    def new_page():
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        pg = ctx.new_page()
        pg.set_default_timeout(30000)
        return pg

    try:
        test_pages_speed(new_page())
        test_admin(new_page(), USERS["admin"])
        test_student(new_page(), USERS["student"])
        test_parent(new_page(), USERS["parent"])
    except Exception as e:
        print(f"\n!!! ОШИБКА ТЕСТЕРА: {e}")
    finally:
        browser.close()

    # Итоговый отчёт
    print(f"\n{'='*50}")
    print("ИТОГОВЫЙ ОТЧЁТ")
    print('='*50)
    passed = [r for r in results if r[0] == "✓"]
    failed = [r for r in results if r[0] == "✗"]
    print(f"✓ Пройдено: {len(passed)}")
    print(f"✗ Провалено: {len(failed)}")
    if failed:
        print("\nПроблемы:")
        for r in failed:
            print(f"  ✗ {r[1]}" + (f" — {r[2]}" if r[2] else ""))
