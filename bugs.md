# Bug List

<!-- Тестер: tester.py → скриншоты → анализ → баги сюда -->
<!-- Разработчик: берёт первый open, чинит, ставит fixed -->
<!-- Последний прогон: 2026-03-25 17:00 BKK. BUG-011,014,019 verified-fixed. Осталось: BUG-016 (логотип) -->

## BUG-001–003: Dashboard виджеты и layout — verified-fixed
## BUG-005: Teacher panel — verified-fixed
## BUG-006–008: Футер, tours, grid — verified-fixed
## BUG-009: Assign таблица — verified-fixed
## BUG-012–013: Admin enrolled, frontpage — verified-fixed
## BUG-015: Toggle темы — verified-fixed
## BUG-017–018: Messaging, admin язык — verified-fixed
## BUG-020–021: Mobile секции и приветствие — verified-fixed
## BUG-023: Navbar "Дополнительно" — verified-fixed

## BUG-004: Level Up! XP — текст на английском
- **Страница:** /my/ → правый sidebar
- **Ожидание:** "Участвуйте в курсе, чтобы получать очки опыта!" через CSS ::after
- **Факт:** Заголовок "Очки опыта" на русском. Описание — не удалось прочитать мелкий текст на скрине 007. Нужен крупный скрин sidebar
- **Скриншот:** screenshots/007_dashboard_student_desktop.png
- **Статус:** partially-fixed (нужна перепроверка крупным планом)

## BUG-010: BBB страница ожидания
- **Страница:** /mod/bigbluebuttonbn/view.php
- **Факт:** Карточка с тенью и border-radius. "Ожидание подключения руководителя." Навигация внизу
- **Скриншот:** screenshots/062_activity_student_0_desktop.png
- **Статус:** partially-fixed (нет иконки/анимации, но визуально ОК)

## BUG-011: BBB admin warning banner
- **Факт:** Warning в оранжевой карточке с border-radius и тёплым фоном
- **Скриншот:** screenshots/light_bug011_bbb_admin.png
- **Статус:** verified-fixed

## BUG-014: Quiz попытки
- **Факт:** "Ваши попытки" — Попытка 1 и 2 в карточках с border-radius и тенью. Кнопка оранжевая
- **Скриншот:** screenshots/light_bug014_quiz_direct.png
- **Статус:** verified-fixed

## BUG-016: Логотип в navbar
- **Страница:** все
- **Ожидание:** Белый логотип EasyDays, иконка Moove скрыта
- **Факт:** Headless скриншот подтверждает: белый EasyDays лого виден (40x40, /pix/school-logo.png). Moove иконки нет. Возможно кэш браузера тестера
- **Скриншот:** screenshots/debug_logo_close.png (verified), screenshots/fix9_login_logo.png
- **Статус:** fixed — лого работает, нужна перепроверка с очисткой кэша

## BUG-019: Карточки /my/courses.php
- **Факт:** Карточки MAT-1 и RUS-1 со скруглёнными углами и тенью. Hover — оранжевый border. Стилизовано
- **Скриншот:** screenshots/light_bug019_courses.png
- **Статус:** verified-fixed

## BUG-022: XP popup английский
- **Факт:** Связано с BUG-004
- **Статус:** partially-fixed
