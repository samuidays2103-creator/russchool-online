# Bug List

<!-- Тестер: tester.py → 103 скриншота → анализ → баги сюда -->
<!-- Разработчик: берёт первый open, чинит, ставит fixed -->
<!-- Тестер перезапустит tester.py и проверит -->

## BUG-001: Dashboard — приветственный виджет не появляется
- **Страница:** /my/
- **Роль:** student, admin
- **Ожидание:** Вверху dashboard блок "Доброе утро, Миша!" с gradient-фоном и badge "Скоро урок"
- **Факт:** Виджет #school-dashboard-header не инжектится. JS из footer видимо не находит #region-main или .block_myoverview в нужный момент (DOM ещё не готов, или структура Moodle 4.5 изменилась)
- **Скриншот:** screenshots/011_dashboard_student_desktop.png
- **Статус:** open

## BUG-002: Dashboard — sidebar "Ближайшие уроки" не появляется
- **Страница:** /my/
- **Роль:** student, admin
- **Ожидание:** Справа sticky-sidebar с расписанием и курсами
- **Факт:** Sidebar #school-sidebar не создаётся. JS ищет .block_myoverview но возможно этот блок отсутствует или имеет другой селектор в Moodle 4.5
- **Скриншот:** screenshots/011_dashboard_student_desktop.png
- **Статус:** open

## BUG-003: Dashboard — "Шкала времени" вместо карточек курсов
- **Страница:** /my/
- **Роль:** student
- **Ожидание:** Блок "Мои курсы" с карточками (card-grid) как основной контент
- **Факт:** Главный блок — "Шкала времени" (Timeline) с фильтрами и пустым "Нет элементов курса". Карточки курсов показываются только через "Обзор курсов" popup (скрин 015). Настройка Dashboard page в Moodle выставлена на Timeline, а не Course overview
- **Скриншот:** screenshots/011_dashboard_student_desktop.png, screenshots/015_dashboard_student_usermenu_desktop.png
- **Статус:** open — myoverview теперь вверху (weight=-2), но Moodle Layout Manager определяет порядок по regions

## BUG-004: Level Up! виджет — текст на английском
- **Страница:** /my/, /course/view.php?id=2
- **Роль:** student
- **Ожидание:** Виджет Level Up! XP на русском или полностью скрыт
- **Факт:** Показывает "Level up!", "Participate in the course to gain experience points and...", "Начинающий" (частично русский). Англ. текст не переведён
- **Скриншот:** screenshots/043_course_student_desktop_sections_toggled.png
- **Статус:** open

## BUG-005: Teacher panel не появляется на странице курса
- **Страница:** /course/view.php?id=2
- **Роль:** admin (teacher)
- **Ожидание:** Панель #school-teacher-panel с кнопками: Журнал оценок, Список учеников, Задания, Начать урок
- **Факт:** Панель не инжектится. JS проверяет isTeacher через `.editing-mode-toggle-on, [data-action="toggle-editing"], .editing-mode-toggle` — в Moodle 4.5 кнопка "Режим редактирования" имеет другие атрибуты
- **Скриншот:** screenshots/063_course_admin_desktop.png
- **Статус:** open

## BUG-006: Футер "На платформе Moodle" виден на всех мобильных страницах
- **Страница:** /my/, /course/view.php?id=2, /mod/bigbluebuttonbn/, все активности (mobile)
- **Роль:** student
- **Ожидание:** Футер скрыт или ребрендирован ("Онлайн-школа EasyDays")
- **Факт:** Видна надпись "На платформе Moodle" с оранжевой ссылкой. CSS-правило `.moove-container-fluid { display: none }` не покрывает этот элемент
- **Скриншот:** screenshots/003_frontpage_mobile.png, screenshots/046_activity_student_0_mobile.png
- **Статус:** fixed — добавлены CSS-селекторы для скрытия footer/powered-by/moodle.org ссылок

## BUG-007: Журнал оценок — user tour popup перекрывает таблицу
- **Страница:** /grade/report/grader/index.php?id=2
- **Роль:** admin
- **Ожидание:** Таблица оценок видна сразу без popup
- **Факт:** Popup "Лёгкий поиск студентов" (Далее 1/3, Пропустить тур) перекрывает таблицу при первом визите. Нужно отключить user tours через Admin → Appearance → User tours
- **Скриншот:** screenshots/101_grades_admin.png (после dismiss_tours — без popup)
- **Статус:** fixed — все 5 user tours отключены через UPDATE mdl_tool_usertours_tours SET enabled=0

## BUG-008: Dashboard grid layout не работает
- **Страница:** /my/
- **Роль:** student, admin
- **Ожидание:** CSS grid `1fr 320px` — основной контент + sidebar
- **Факт:** Layout однколоночный. CSS `body.pagelayout-mydashboard #region-main { grid-template-columns: 1fr 320px }` не даёт эффекта т.к. нет второго элемента в grid (sidebar не инжектится → BUG-002). Moodle размещает блоки своим layout
- **Скриншот:** screenshots/011_dashboard_student_desktop.png
- **Статус:** open (зависит от BUG-002)

## BUG-009: Страницы активностей (assign) — "Состояние ответа" без стилизации
- **Страница:** /mod/assign/view.php?id=* (все задания)
- **Роль:** student
- **Ожидание:** Карточка задания стилизована: скруглённые углы, тёплый фон, брендовые цвета
- **Факт:** Таблица "Состояние ответа" выглядит стандартно Moodle — нет border-radius, нет тени, заголовок "Номер попытки / Состояние ответа / Баллы" не стилизован. Страница визуально "голая"
- **Скриншот:** screenshots/029_activity_student_1_desktop.png — screenshots/041_activity_student_7_desktop.png
- **Статус:** open

## BUG-010: BBB страница — "Ожидание подключения руководителя" без стилизации
- **Страница:** /mod/bigbluebuttonbn/view.php?id=*
- **Роль:** student
- **Ожидание:** Красивая страница ожидания с анимацией или понятным сообщением
- **Факт:** Просто текст "Ожидание подключения руководителя." на белом фоне. Навигация "Перейти на..." внизу. Пустое пространство. Нет кнопки, нет прогресса, нет информации когда будет урок
- **Скриншот:** screenshots/027_activity_student_0_desktop.png, screenshots/046_activity_student_0_mobile.png
- **Статус:** open

## BUG-011: BBB admin — warning banner не стилизован
- **Страница:** /mod/bigbluebuttonbn/view.php?id=* (admin)
- **Роль:** admin
- **Ожидание:** Warning красиво вписан в стиль или скрыт
- **Факт:** Красный alert-banner "Срок действия учётных данных BigBlueButton по умолчанию скоро истечёт..." — стандартный Bootstrap alert, не вписывается в дизайн
- **Скриншот:** screenshots/065_activity_admin_0_desktop.png
- **Статус:** open

## BUG-012: Обзорный отчёт — admin не записан на курс
- **Страница:** /grade/report/overview/index.php?id=2
- **Роль:** admin
- **Ожидание:** Admin видит оценки всех студентов
- **Факт:** Сообщение "Сейчас Вы не записаны ни на один курс." — admin не enrolled, поэтому overview пустой. Это не UI-баг, но влияет на UX учителя
- **Скриншот:** screenshots/103_grades_overview.png
- **Статус:** open

## BUG-013: Frontpage — "Категории курсов" показывает все классы неавторизованным
- **Страница:** / (главная)
- **Роль:** гость (без логина)
- **Ожидание:** Гость видит только hero + кнопку входа, без деталей курсов
- **Факт:** Под hero виден блок "Категории курсов" со списком "1 класс (4), 2 класс (4), 3 класс (4), 4 класс (4)". Раскрывает внутреннюю структуру школы
- **Скриншот:** screenshots/001_frontpage_desktop.png, screenshots/003_frontpage_mobile.png
- **Статус:** fixed — CSS body.notloggedin скрывает все блоки курсов для гостя

## BUG-014: Тест (quiz) — кнопка "Пройти тест заново" стилизована, но попытка не стилизована
- **Страница:** /mod/quiz/view.php?id=*
- **Роль:** student
- **Ожидание:** Карточка попытки стилизована, детали читаемы
- **Факт:** Кнопка "Пройти тест заново" оранжевая (OK), но блок "Ваши попытки → Попытка 1" — стандартный список без карточки, без визуального выделения. На мобильном мелкий шрифт дат
- **Скриншот:** screenshots/039_activity_student_6_desktop.png, screenshots/058_activity_student_6_mobile.png
- **Статус:** open

## BUG-015: Navbar — переключатель темы (toggle) виден, но не нужен
- **Страница:** все страницы
- **Роль:** все
- **Ожидание:** Нет toggle светлая/тёмная тема, т.к. тёмная тема не поддержана
- **Факт:** В navbar виден toggle-переключатель (серый кружок). Если кликнуть — может сломать стили, т.к. CSS заточен под светлую тему
- **Скриншот:** screenshots/011_dashboard_student_desktop.png (рядом с иконками справа)
- **Статус:** fixed — CSS display:none на .custom-switch, .moove-darkmode-toggle и другие

## BUG-016: Логотип в navbar — CSS ::before не совпадает с Moodle-логотипом
- **Страница:** все страницы
- **Роль:** все
- **Ожидание:** Один чёткий логотип "Онлайн-школа EasyDays"
- **Факт:** Navbar показывает маленькую иконку Moodle-темы (сова/звезда), а CSS пытается подставить лого через ::before с внешнего URL easydayssamui.com. Результат — два конкурирующих элемента, ни один не выглядит как полноценный логотип
- **Скриншот:** screenshots/011_dashboard_student_desktop.png
- **Статус:** open
