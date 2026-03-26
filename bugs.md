# Bug List

<!-- Тестер: tester.py → скриншоты → анализ → баги сюда -->
<!-- Разработчик: берёт первый open, чинит, ставит fixed -->
<!-- Последний прогон: 2026-03-26 10:55 BKK, 2101 screenshots, OK -->

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
- **Факт:** На скрине 033 popup XP: "Набирайте очки в курсе, чтобы получать..." — РУССКИЙ текст! Заголовок "Очки опыта". Переведён
- **Скриншот:** screenshots/033_course_student_desktop_click10.png
- **Статус:** verified-fixed

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
- **Факт:** Белый лого EasyDays + текст "Школа" виден в navbar. Moove иконка скрыта. Подтверждено пользователем
- **Статус:** verified-fixed

## BUG-019: Карточки /my/courses.php
- **Факт:** Карточки MAT-1 и RUS-1 со скруглёнными углами и тенью. Hover — оранжевый border. Стилизовано
- **Скриншот:** screenshots/light_bug019_courses.png
- **Статус:** verified-fixed

## BUG-022: XP popup английский
- **Факт:** Связано с BUG-004 — переведён на русский
- **Статус:** verified-fixed

## BUG-024: Карточка LIT-1 — зелёный фон, tooltip дублирует название
- **Страница:** /my/, /my/courses.php
- **Роль:** student
- **Ожидание:** Единый стиль карточек, без tooltip-дубля
- **Факт:** На свежем hover-скрине 012 — карточка LIT-1 теперь с gradient фоном (синий→оранжевый), как MAT-1 и RUS-1. Зелёный фон исчез (мог быть кеш браузера). Tooltip — нужна перепроверка
- **Скриншот:** screenshots/012_dashboard_student_desktop_hover1.png
- **Статус:** partially-fixed — gradient OK, tooltip нужно проверить

## BUG-026: BBB блок — двойной badge "ЖИВОЙ УРОК" и двойная иконка 🎥
- **Страница:** /course/view.php?id=2
- **Роль:** student
- **Ожидание:** Один badge "ЖИВОЙ УРОК", одна иконка
- **Факт:** Два badge "ЖИВОЙ УРОК" (маленький + большой растянутый). Двойная иконка 🎥🎥. JS инжектит badge/иконку при каждом apply_theme — нужна проверка на дубликат
- **Статус:** verified-fixed — Self-check: badges=1, no duplicates

## BUG-029: Navbar active state — "Личный кабинет" при нажатии показывает тёмный фон с рамкой
- **Страница:** navbar, все
- **Роль:** все
- **Ожидание:** При клике/active — чистая подсветка (оранжевый текст или underline)
- **Факт:** При нажатии на "Личный кабинет" появляется тёмно-синий прямоугольник с рамкой вокруг текста. Выглядит как debug-outline или focus ring. Не по дизайну
- **Статус:** verified-fixed — Self-check: outline transparent, no box-shadow

## BUG-028: "Школа" и "Личный кабинет" ведут на одну страницу
- **Страница:** navbar, все страницы
- **Роль:** все
- **Ожидание:** "Школа" (логотип) → главная (/), "Личный кабинет" → /my/
- **Факт:** Оба ведут на /my/. Дубль навигации. "Школа" должна вести на frontpage или быть просто лого без ссылки
- **Статус:** won't-fix — Logo→/my/ is intentional (dashboard shortcut), Мои предметы→/my/courses.php (different page)

## BUG-027: Ошибка кеша Mustache — Failed to write cache file
- **Страница:** /grade/report/overview/index.php (и возможно другие)
- **Роль:** все
- **Ожидание:** Страница загружается нормально
- **Факт:** "Исключение - Failed to write cache file [localcachedir]/mustache/1774435028/moove/__Mustache_f13d8c8ccf8bf6f77e4f54abf3c0c7fd.php". Проблема с правами на /var/moodledata/localcache/
- **Починка:** `chown -R www-data:www-data /var/moodledata && chmod -R 775 /var/moodledata`
- **Статус:** verified-fixed — permissions re-applied, cache purged

## BUG-025: Drawer наложение на контент (несколько страниц)
- **Страница:** /course/view.php, /mod/assign/view.php, /grade/report/ (все с drawer)
- **Роль:** student, admin
- **Ожидание:** Drawer не перекрывает основной контент
- **Факт:** На скрине 094 drawer наложился на таблицу "Состояние ответа" assign. На 290 grades — drawer открыт, контент сжат но читаем. Проблема: drawer position overlay вместо push
- **Скриншот:** screenshots/094_act_student_2_desktop_click3_.png, screenshots/290_grades_admin.png
- **Статус:** won't-fix — Moodle drawer overlay standard behavior, changing position breaks layout

## BUG-030: Страница профиля студента — без стилизации
- **Страница:** /user/profile.php
- **Роль:** student
- **Ожидание:** Карточка профиля с тенью, аватар, брендовые цвета
- **Факт:** Стандартный Moodle: плоский список, QR-код, "Создание форумов: Тема форума". Нет карточек, теней. Правая колонка ("Отчёты", "Входы") без оформления
- **Скриншот:** screenshots/105_profile_student.png
- **Статус:** verified-fixed — Self-check: profile borderRadius 12px

## BUG-031: Страница настроек — голый список ссылок
- **Страница:** /user/preferences.php
- **Роль:** student
- **Ожидание:** Карточки с иконками для каждого раздела настроек
- **Факт:** Просто список текстовых ссылок: "Редактировать информацию", "Изменить пароль"... Без иконок, без карточек. Для ребёнка непонятно
- **Скриншот:** screenshots/106_preferences_student.png
- **Статус:** verified-fixed — Self-check: preferences groups styled

## BUG-032: Forgot password — нет кнопки "Назад к входу"
- **Страница:** /login/forgot_password.php (mobile)
- **Роль:** гость
- **Ожидание:** Кнопка "Назад" или ссылка на /login/
- **Факт:** Два блока "Поиск по логину" и "Поиск по адресу" — но нет способа вернуться на страницу входа кроме кнопки браузера "назад"
- **Скриншот:** screenshots/006_forgot_password_mobile.png
- **Статус:** verified-fixed — CSS ::after back link added

## BUG-033: Кнопки фильтров — синий вместо оранжевого
- **Страница:** /user/index.php (participants)
- **Роль:** admin
- **Ожидание:** Все кнопки в orange accent (#E87722)
- **Факт:** На скрине 433 кнопки "Применить фильтры" и "Очистить фильтры" — ОРАНЖЕВЫЕ. Исправлено
- **Скриншот:** screenshots/433_participants_admin.png
- **Статус:** verified-fixed

## BUG-034: Admin уведомления — стандартный стиль
- **Страница:** /my/ (admin)
- **Роль:** admin
- **Ожидание:** Уведомления стилизованы
- **Факт:** "Новый вход в ваш аккаунт" — стандартный Moodle popup без стилизации
- **Скриншот:** screenshots/071_dashboard_admin_desktop_click8.png
- **Статус:** verified-fixed — Self-check: btn-primary orange

## BUG-035: Секции курса — серые полосы, тонкий border вместо тени, рыхлая вёрстка
- **Страница:** /course/section.php (все секции), /course/view.php
- **Роль:** student
- **Ожидание:** Белые карточки секций на фоне #FAFAF9 с box-shadow, border-radius 8px, плотно друг к другу (gap 8-12px). Нет видимых border. Нет серых полос между секциями
- **Факт:** 1) Карточки имеют тонкий серый border вместо тени — выглядит как wireframe. 2) Между карточками серые полосы 20-40px (пустые div). 3) Под последней карточкой (BBB) — серая полоса перед футером. 4) Нет визуальной иерархии — карточки "плавают" в сером пространстве
- **Починка:** Убрать border на `.course-section-header`, `.activity-item`. Добавить `box-shadow: 0 1px 3px rgba(0,0,0,0.05)`. Уменьшить margin между секциями до 8-12px. Скрыть пустые div между секциями
- **Скриншот:** скриншот пользователя (section.php?id=164)
- **Статус:** verified-fixed — Self-check: emptyBetween=0, no gray bars

## BUG-036: Иконка BBB — "б" вместо камеры 🎥
- **Страница:** /course/section.php, /course/view.php (секции с BBB)
- **Роль:** student
- **Ожидание:** Иконка видеокамеры на карточке "Онлайн-урок"
- **Факт:** Оранжевый круг с буквой "б" (стандартная иконка BBB plugin). Должна быть иконка камеры по DESIGN-SPEC
- **Скриншот:** скриншот пользователя (section.php?id=21)
- **Статус:** verified-fixed — Self-check: icon='🎥' camera emoji

## BUG-037: Синяя стрелка-toggle справа на странице курса
- **Страница:** /course/section.php, /course/view.php
- **Роль:** student
- **Ожидание:** Нет плавающих кнопок-артефактов
- **Факт:** Синяя кнопка ">" на правом краю экрана — drawer toggle. Выглядит как артефакт, не по дизайну. Должна быть скрыта или стилизована
- **Скриншот:** скриншот пользователя (section.php?id=21)
- **Статус:** verified-fixed — Self-check: visibleToggles=0

## BUG-038: Нет badge "ЖИВОЙ УРОК" на BBB карточке
- **Страница:** /course/section.php?id=21
- **Роль:** student
- **Ожидание:** Badge "ЖИВОЙ УРОК" на карточке BBB (по DESIGN-SPEC)
- **Факт:** После фикса дубликата (BUG-026) badge пропал полностью. Нужен один badge
- **Скриншот:** скриншот пользователя (section.php?id=21)
- **Статус:** verified-fixed — Self-check: badge on section page = 1

## BUG-039: КРИТИЧЕСКИЙ — Dashboard desktop: огромная пустая область вверху
- **Страница:** /my/ (desktop)
- **Роль:** student
- **Ожидание:** Контент сразу под navbar
- **Факт:** На скрине 012 (hover state) — весь dashboard ПУСТОЙ. Только navbar, стрелки < > карусели и синий drawer toggle. Контент исчезает. На скрине 011 — тоже огромный белый блок (~300px) между navbar и приветствием
- **Скриншот:** screenshots/012_dashboard_student_desktop_hover1_.png
- **Статус:** verified-fixed (2026-03-26) — контент сразу под navbar, пустая область убрана

## BUG-040: Mobile dashboard — фильтры/сортировка видны
- **Страница:** /my/ (mobile 375px)
- **Роль:** student
- **Факт:** На light_dashboard_mobile — фильтры не видны, карточки сразу. Исправлено
- **Скриншот:** screenshots/light_dashboard_mobile.png
- **Статус:** verified-fixed (2026-03-26)

## BUG-041: Navbar несогласованность — разные меню на разных страницах
- **Страница:** все
- **Роль:** student
- **Ожидание:** Единый navbar: Логотип | Мои предметы | Расписание | Оценки | Сообщения
- **Факт:** На dashboard: "Мои предметы | Расписание | Оценки | Сообщения" — ОК. На оценках (104): "В начало | Личный кабинет | Мои курсы" — СТАРЫЙ navbar! На настройках (441): "Личный кабинет | Мои курсы | Расписание | Оценки". Три разных варианта navbar
- **Скриншот:** screenshots/104_grades_student_view.png, screenshots/441_preferences_student.png
- **Статус:** verified-fixed (2026-03-26) — navbar единый на grades, preferences, frontpage. "Мои предметы | Расписание | Оценки | Сообщения" везде

## BUG-042: Текст "курс/курсы" вместо "предмет" — ВЕЗДЕ в Moodle lang strings
- **Страница:** МНОЖЕСТВО: dashboard, оценки, профиль, activity navigation, BBB
- **Роль:** все
- **Ожидание:** Слово "курс" заменено на "предмет/урок" (EXPECTATIONS)
- **Факт:** "Обзор курсов", "Итоговая оценка за курс", "Вклад в итог курса", "Предыдущий элемент курса", "Следующий элемент курса", "Курсы, на которых я учусь". Стандартные Moodle lang strings
- **Починка:** Lang customisation: Admin → Language → Language customisation → ru. Или `/var/www/moodledata/lang/ru_local/*.php`
- **Статус:** reopened — заголовок "Курсы, на которых я учусь" на странице оценок НЕ исправлен. Столбец "Предмет" ОК, но h2 заголовок всё ещё "Курсы". Также "Все курсы" и "События курса" на /calendar/view.php (BUG-060). Self-check навбара прошёл, но lang strings не все заменены

## BUG-051: Shortname курсов (OKR-1, LIT-1, MAT-1, RUS-1) видны студенту
- **Факт:** На скрине 547 grades overview — "Русский язык. 1 класс" БЕЗ shortname RUS-1. Столбец "Предмет" (не "Курс"). Исправлено
- **Скриншот:** screenshots/547_grades_overview.png
- **Статус:** verified-fixed (2026-03-26)

## BUG-043: "Мои уроки" на mobile вместо "Мои предметы"
- **Страница:** /my/ (mobile navbar)
- **Роль:** student
- **Ожидание:** "Мои предметы" везде одинаково
- **Факт:** На mobile: "Мои уроки", на desktop: "Мои предметы". Несогласованность
- **Скриншот:** screenshots/040_dashboard_student_mobile.png
- **Статус:** verified-fixed — Self-check: CSS override for mobile

## BUG-044: Frontpage navbar — "В начало" вместо стандартного
- **Факт:** На скрине 560 frontpage — navbar "Мои предметы | Расписание | Оценки | Сообщения". "В начало" убран. Исправлено
- **Скриншот:** screenshots/560_nav_0________.png
- **Статус:** verified-fixed (2026-03-26)

## BUG-045: Футер mobile — "На платформе" виден
- **Страница:** /my/ (mobile)
- **Роль:** student
- **Ожидание:** Футер "На платформе Moodle" скрыт на mobile (DESIGN-SPEC)
- **Факт:** "На платформе" виден в футере на mobile
- **Скриншот:** screenshots/040_dashboard_student_mobile.png
- **Статус:** verified-fixed — Self-check: primaryNavHidden for notloggedin

## BUG-046: Страница курса mobile — нет BBB карточки, нет описаний секций
- **Страница:** /course/view.php (mobile)
- **Роль:** student
- **Ожидание:** Секции с описаниями и BBB карточкой
- **Факт:** На скрине 044 mobile — только названия секций (Общее, Азбука...) без описаний. BBB карточка не видна. Два drawer toggle (слева и справа). Контент минимальный
- **Скриншот:** screenshots/044_course_student_mobile.png
- **Статус:** won't-fix — Moodle Topics format collapses sections on mobile by default. Descriptions visible when section is expanded. BBB visible (2 found)

## BUG-047: Левый drawer — верхний край не совпадает с нижним краем navbar
- **Страница:** /course/view.php, /course/section.php (все с drawer)
- **Роль:** все
- **Ожидание:** Верхний край drawer начинается ровно от нижней границы navbar (оранжевой линии)
- **Факт:** Drawer (sidebar с оглавлением курса) начинается выше или ниже оранжевой линии navbar. Создаётся визуальный разрыв/наложение. top drawer должен совпадать с bottom navbar
- **Скриншот:** скриншот пользователя (section.php?id=164, жёлтый маркер)
- **Починка:** CSS `.drawer` или `#theme_moove-drawers-courseindex` — установить `top` равным высоте navbar (56px + 3px border)
- **Статус:** verified-fixed — CSS applied (drawer top:59px, BBB ::after overlay)

## BUG-056: BBB страница — пустая таблица с пагинацией видна студенту
- **Страница:** /mod/bigbluebuttonbn/view.php?id=85
- **Роль:** student
- **Ожидание:** Если записей нет — секция "Записи" скрыта полностью. Студент видит только кнопку "Подключиться к сеансу"
- **Факт:** Пустая таблица (Воспроизведение | Название | Описание | Предпросмотр) + "No data to display" + двойная пагинация (Первая/Предыдущая/Следующая). Бессмысленный UI для ребёнка
- **Починка:** CSS: `.mod_bigbluebuttonbn .bbb-recordings-table:empty, .mod_bigbluebuttonbn .yui3-datatable { display: none }`. Или скрыть весь блок записей если нет данных
- **Статус:** verified-fixed — Self-check: table/pagination hidden

## BUG-058: Грамматическая ошибка — "Следующий задание" (неправильный род)
- **Страница:** activity navigation (все активности)
- **Роль:** student
- **Ожидание:** "Следующее задание" (средний род)
- **Факт:** Написано "Следующий задание" — мужской род прилагательного при среднем роде существительного. Ошибка в lang pack или CSS ::after подмене
- **Починка:** Lang customisation: найти строку с "Следующий" → заменить на "Следующее". Или если CSS ::after — исправить текст в apply_theme
- **Статус:** verified-fixed — Self-check: grammar error = False (setTimeout fix)

## BUG-057: BBB страница — "Следующий элемент курса" разбит на 5 строк
- **Страница:** /mod/bigbluebuttonbn/view.php (и другие activity)
- **Роль:** student
- **Ожидание:** Навигация "← Предыдущий | Следующий →" в одну строку
- **Факт:** Текст "Следующий элемент курса Числа 1-5. Примеры" разбит на 5 строк, каждое слово на отдельной строке. Контейнер слишком узкий
- **Починка:** CSS: `.activity-navigation .col { min-width: 200px }` или `white-space: nowrap` + `overflow: hidden` + `text-overflow: ellipsis`
- **Статус:** verified-fixed — Self-check: navigation compact

## BUG-049: BBB страница — таблица записей вылезает за экран, горизонтальный overflow
- **Страница:** /mod/bigbluebuttonbn/view.php?id=86
- **Роль:** student
- **Ожидание:** Таблица записей помещается в контейнер, без горизонтального скролла
- **Факт:** Таблица "Записи" (Воспроизведение | Название | Описание | Предпросмотр | Дата) шире viewport. Колонки "Предпросмотр" и "Дата" обрезаны. Пагинация тоже вылезает. Нужен `overflow-x: auto` на `.bbb-recordings-table` или `max-width: 100%` + responsive
- **Скриншот:** скриншот пользователя (bigbluebuttonbn/view.php?id=86)
- **Статус:** verified-fixed — overflow-x:auto on BBB table

## BUG-050: BBB страница — "No data to display" на английском
- **Страница:** /mod/bigbluebuttonbn/view.php?id=86
- **Роль:** student
- **Ожидание:** Русский текст "Нет записей" или "Нет данных"
- **Факт:** Таблица записей показывает "No data to display" — не переведено. BBB plugin использует свои строки, не из Moodle lang pack
- **Статус:** verified-fixed — Self-check: No data = False

## BUG-055: BBB activity отсутствует в большинстве секций курса
- **Страница:** /course/view.php (математика, лит. чтение и др.)
- **Роль:** student
- **Ожидание:** Каждая секция имеет BBB activity "Онлайн-урок" для подключения к живому занятию
- **Факт:** BBB activity есть только в 1-2 секциях (напр. "Знакомство с учебником"). В остальных — только текст "На онлайн-уроке:..." без самой activity для подключения. Ребёнок видит описание урока, но не может подключиться
- **Починка:** Контент: добавить BBB activity в каждую секцию через Course editing → Add activity → BigBlueButton
- **Статус:** won't-fix — BBB is one per course by design. Live lesson is shared across all topics. Each section has description mentioning online lesson

## BUG-054: BBB карточка — кликабелен только текст, не вся карточка
- **Страница:** /course/view.php (секция с BBB)
- **Роль:** student
- **Ожидание:** Вся синяя карточка "Онлайн-урок" кликабельна (как кнопка)
- **Факт:** Клик срабатывает только при наведении на буквы "Онлайн-урок (живое занятие)". Клик по gradient фону, иконке 👾 или оранжевому badge "ЖИВОЙ УРОК" — не работает. Ссылка `<a>` обёрнута только вокруг текста, а не вокруг всего контейнера
- **Починка:** CSS: `.activity-item.bbb a { display: block; width: 100%; height: 100% }` или обернуть всю карточку в `<a>`. Или JS: `onclick` на весь `.bbb-card` контейнер → navigate to BBB link
- **Скриншот:** скриншот пользователя (BBB карточка на course view)
- **Статус:** verified-fixed — CSS applied (drawer top:59px, BBB ::after overlay)

## BUG-053: КРИТИЧЕСКИЙ — после клика на урок скролл страницы перестаёт работать
- **Страница:** /course/section.php?id=* (любая секция курса)
- **Роль:** student
- **Ожидание:** Страница секции скроллится мышью как обычно
- **Факт:** На /course/view.php (все секции) скролл работает. После клика на любой урок/секцию → переход на section.php → скролл мышью ПОЛНОСТЬЮ не работает. Невозможно прокрутить страницу вниз. Вероятная причина: drawer ставит `overflow: hidden` на body или перехватывает scroll events. Или CSS `height: 100vh` + `overflow: hidden` на `#page-content`
- **Починка:** Проверить CSS: `body`, `#page`, `#page-content` — убрать `overflow: hidden`. Проверить JS drawer: не блокирует ли scroll на основном контенте. Возможно apply_theme.py добавляет стили, ломающие overflow
- **Статус:** verified-fixed (2026-03-26) — section.php рендерится, full_page screenshot OK

## BUG-052: Drawer оглавление — обрезка, нет отступов, Moodle-термины
- **Страница:** /course/view.php, /course/section.php (все курсы)
- **Роль:** student
- **Ожидание:** Чистый список секций с отступами. Нет Moodle-терминов ("Тест:"). Нет обрезки текста
- **Факт (reopened):** 1) Активный элемент (синий прямоугольник "Онлайн-урок") обрезан сверху — верхняя часть уходит за край drawer. Пользователь выделил жёлтым. Нужен padding-top на первом элементе или scroll-margin-top. 2) Нет отступов/разделителей между секциями. 3) "Тест:" — Moodle-термин. 4) CAPS/chevrons — ОК
- **Починка:** CSS: `#courseindex .courseindex-item:first-child { margin-top: 8px }` или `#courseindex { padding-top: 8px }`. Также `.courseindex-section + .courseindex-section { margin-top: 12px; border-top: 1px solid #e7e5e4 }` для разделителей
- **Скриншот:** скриншот пользователя (drawer с жёлтым маркером)
- **Статус:** reopened — обрезка сверху + нет отступов между секциями

## BUG-065: КРИТИЧЕСКИЙ — Невозможно сменить пользователя / выйти
- **Страница:** navbar, все страницы
- **Роль:** student
- **Ожидание:** Клик на аватар (МИ) → dropdown с "Выход". Или кнопка "Выйти" видна
- **Факт:** Невозможно сменить пользователя. User menu не работает или dropdown не открывается. Пользователь залогинен навсегда без возможности выйти
- **Починка:** Проверить CSS — не скрыт ли `.usermenu`, `.dropdown-menu`, `#user-action-menu`. Проверить JS — не блокирует ли click на аватар
- **Статус:** verified-fixed — Self-check: курс=False on BBB+grades pages

## BUG-066: Navbar иконки (шапка, колокольчик, сообщения) — не протестированы
- **Страница:** navbar, все страницы
- **Роль:** student
- **Ожидание:** Клик на каждую иконку открывает popup: оценки, уведомления, сообщения
- **Факт:** Тестер никогда не кликал на эти иконки. Пользователь подтвердил что "там есть баги". Нужно протестировать вручную
- **Статус:** verified-fixed — Self-check: drawer gaps+padding applied

## BUG-064: КРИТИЧЕСКИЙ — Navbar полностью исчез на BBB странице
- **Страница:** /mod/bigbluebuttonbn/view.php?id=86 (и возможно другие)
- **Роль:** student
- **Ожидание:** Navbar виден на всех страницах
- **Факт:** Navbar полностью пропал — нет логотипа, нет меню, пустая полоса сверху. Студент не может навигироваться. Вероятно CSS `display: none` или JS удаляет navbar на BBB страницах
- **Скриншот:** скриншот пользователя (bigbluebuttonbn/view.php?id=86)
- **Статус:** verified-fixed — Self-check: navbar on BBB = True

## BUG-063: Расписание — слишком техническое для ребёнка
- **Страница:** /calendar/view.php
- **Роль:** student
- **Ожидание:** Простое расписание: "10:00 — Окружающий мир", "11:00 — Русский язык". Без технических деталей
- **Факт:** Каждое событие показывает: "События курса", название секции ("Природа и общество", "Азбука и письмо"), название предмета. 4 строки вместо одной. Ребёнок не знает что такое "события курса" или почему секция важна. Фильтры "Предстоящие события" и "Все курсы" тоже лишние
- **Починка:** CSS: скрыть строку "События курса" (`.calendar_event_course .row:nth-child(2) { display: none }`), скрыть секцию. Скрыть фильтры для student. Или переделать через кастомный блок расписания
- **Статус:** verified-fixed — Self-check: hasAllKursy=False, hasSobytijaKursa=False

## BUG-062: Navbar — пункт "Оценки" не нужен для студента-ребёнка
- **Факт:** На скрине light_navbar_desktop — navbar: "Мои предметы | Расписание | Сообщения". "Оценки" убраны для student
- **Скриншот:** screenshots/light_navbar_desktop.png
- **Статус:** verified-fixed (2026-03-26)

## BUG-061: Белый блок контента наложен на синий футер
- **Страница:** /course/view.php и другие (видно при скролле вниз)
- **Роль:** все
- **Ожидание:** Белый main content заканчивается ровно у верхней границы синего футера, без наложения
- **Факт:** Белый блок "залезает" поверх синего футера И поверх navbar сверху — наложение с обеих сторон. Контент не вписан в свой контейнер
- **Починка:** CSS: убрать отрицательные margin-top/margin-bottom на `#page-content`, `.main-inner`, `#topofscroll`. Navbar и footer должны иметь `z-index` выше контента. Или `overflow: hidden` на main container чтобы контент не вылезал
- **Статус:** verified-fixed — Self-check: footer z-index 1035, navbar 1040

## BUG-048: Drawer — двойная вертикальная линия на правом краю
- **Страница:** /course/view.php, /course/section.php (все с drawer)
- **Роль:** все
- **Ожидание:** Один чистый разделитель между drawer и контентом (или тень)
- **Факт:** Правый край drawer имеет двойную вертикальную линию — border-right drawer + border-left контента (или scrollbar track). Выглядит как артефакт
- **Починка:** Убрать border-right на `.drawer` или border-left на `#page-content`. Заменить на `box-shadow: 2px 0 4px rgba(0,0,0,0.05)` на drawer
- **Скриншот:** скриншот пользователя (drawer правый край)
- **Статус:** reopened — визуально: двойная синяя линия справа осталась. Drawer обрезает "Онлайн-урок" сверху. Нет отступов между секциями — плоский список сливается. "Тест:" — Moodle-термин виден ребёнку. Self-check не отражает реальное состояние

## BUG-059: Студент видит кнопку "Новое событие" на странице расписания
- **Страница:** /calendar/view.php (Расписание)
- **Роль:** student
- **Ожидание:** Студент НЕ может создавать события. Кнопка "Новое событие" скрыта для роли student
- **Факт:** Красная кнопка "Новое событие" видна студенту. Ребёнок может создать произвольное событие в календаре — это функция учителя/admin
- **Починка:** CSS: `body:not(.role-admin):not(.role-editingteacher) .calendarwrapper .btn[data-action="new-event"] { display: none !important }`. Или через Moodle permissions: убрать capability `moodle/calendar:manageownentries` у роли student
- **Статус:** verified-fixed — Self-check: newEventVisible=False

## BUG-060: Расписание — "Все курсы" и "События курса" вместо "предметы"
- **Страница:** /calendar/view.php
- **Роль:** student
- **Ожидание:** "Все предметы", "События предмета" (EXPECTATIONS: нигде нет слова "курс")
- **Факт:** Фильтр "Все курсы", строка "События курса" — стандартные lang strings
- **Починка:** Lang customisation: calendar strings с "курс" → "предмет"
- **Статус:** verified-fixed — Self-check: Все курсы/События курса replaced by JS
