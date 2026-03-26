"""
apply_theme_v3.py
Platform v3: Dashboard widgets, Teacher panel, BBB styling, JS DOM manipulation.
Full UI redesign with role-based client-side enhancements.
"""
import sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = "http://130.12.47.10"
os.makedirs("screenshots", exist_ok=True)

# ─── CSS: все стили v2 + новые v3 ───────────────────────────────────────────
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
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 0 !important;
}
.navbar-brand:focus, .navbar-brand:active, .navbar-brand:hover {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
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
/* Скрыть ВСЬЮ primary navigation Moodle — наш JS navbar её заменяет */
.primary-navigation {
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    max-height: 0 !important;
    position: absolute !important;
    width: 0 !important;
    opacity: 0 !important;
}
/* Скрыть popover "Мои предметы" ссылку (дублирует наш nav) */
.popover-region-container .see-all-link[href*="courses"],
.navbar .popover-region .see-all-link {
    display: none !important;
}
/* Наша кастомная nav-панель (создаётся JS в footer) */
#school-nav-links {
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
    margin-left: 16px !important;
}
#school-nav-links a {
    color: rgba(255,255,255,0.88) !important;
    padding: 6px 14px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    text-decoration: none !important;
    border-radius: 6px !important;
    transition: all 0.15s !important;
    white-space: nowrap !important;
}
#school-nav-links a:hover {
    color: #E87722 !important;
    background: rgba(255,255,255,0.1) !important;
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
.card.course-card {
    border-radius: 16px !important;
    border: 1px solid #E7E5E4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s !important;
    overflow: hidden !important;
    background: #FFFFFF !important;
}
.card.course-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(30,58,95,0.15) !important;
    border-color: #E87722 !important;
}
/* BUG-024: Единый фон карточек (не зелёный/фиолетовый — единый брендовый) */
.card.course-card .card-img-top {
    height: 130px !important;
    object-fit: cover !important;
    background: linear-gradient(135deg, #1e3a5f 0%, #2a5298 60%, #E87722 100%) !important;
    background-size: cover !important;
    background-position: center !important;
}
/* BUG-025: Drawer не наложится на navbar */
.drawer-left, [data-region="left-hand-drawer"] {
    z-index: 1030 !important;
    top: 56px !important;
}
.drawer.show {
    z-index: 1030 !important;
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
/* Описание секции — красивая карточка */
/* Описание секции — только если есть контент */
.course-content .section-summary:not(:empty),
.course-content .course-section .summary:not(:empty),
.course-content .section .summary:not(:empty) {
    padding: 16px 20px !important;
    font-size: 15px !important;
    color: #57534E !important;
    line-height: 1.6 !important;
    background: #f8fafc !important;
    border-left: 4px solid #E87722 !important;
    margin: 12px 16px !important;
    border-radius: 8px !important;
}
/* Пустые summary — полностью скрыть */
.course-content .section-summary:empty,
.course-content .summary:empty,
.course-content .section_availability:empty {
    display: none !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}
/* Серая полоса сверху секции — скрыть все пустые wrapper'ы */
.course-content .course-section > .content > div:empty,
.course-content .sectionhead,
[data-for="page-activity-header"] {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Скрыть пустые блоки в секциях */
.activity-header,
[data-for="page-activity-header"],
.course-section .activity-header {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Убрать синюю рамку на активной секции в sidebar */
#courseindex .courseindex-item.active,
#courseindex .courseindex-section.active,
.courseindex [aria-current="true"],
.courseindex .active {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
    background: rgba(30,58,95,0.08) !important;
}
/* Course index sidebar — убрать ВСЕ рамки/outline */
#courseindex a:focus,
#courseindex a:focus-visible,
#courseindex a:active,
#courseindex button:focus,
#courseindex button:focus-visible,
.courseindex a:focus,
.courseindex a:focus-visible,
.courseindex *:focus,
.courseindex *:focus-visible,
#courseindex .courseindex-link:focus,
#courseindex .courseindex-link:focus-visible {
    outline: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
}
/* Глобально убрать ВСЕ focus rings */
*:focus, *:focus-visible, *:focus-within {
    outline: 2px solid transparent !important;
    outline-offset: 0 !important;
    box-shadow: none !important;
}
/* Course index — активная секция: оранжевый фон вместо синей рамки */
.courseindex .courseindex-section.highlight,
.courseindex .courseindex-item.current,
#courseindex [aria-expanded="true"],
#courseindex .active,
.courseindex-section-title[aria-current] {
    background: rgba(30,58,95,0.08) !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
/* Серая полоса — course-section-header на section page */
.course-section-header,
[data-for="page-activity-header"],
.activity-header {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* Контейнер контента — белый фон, не голубой */
.course-content,
.course-content .course-section,
#region-main .course-content {
    background: white !important;
}
.activity-item {
    border-bottom: 1px solid #f0f0f0 !important;
    transition: background 0.15s !important;
    border-radius: 0 !important;
    padding: 12px 16px !important;
}
.activity-item:last-child { border-bottom: none !important; }
/* Section page — убрать лишнее пустое пространство */
body.path-course-view #region-main,
body[class*="path-course-section"] #region-main {
    min-height: auto !important;
}
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
    border: none !important;
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
/* Скрыть фильтры/сортировку/поиск — ученику не нужно при 4 предметах */
.block_myoverview [data-region="filter"],
.block_myoverview [data-region="courses-view-dropdown"],
.block_myoverview .dropdown,
.block_myoverview .block-header,
.block_myoverview .card-header,
.block_myoverview input[type="search"],
.block_myoverview .header-action,
[data-block="myoverview"] .card-header {
    display: none !important;
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

/* ═══ V3: СКРЫТЬ ПУСТОЙ LEFT DRAWER на dashboard ═══ */
body.pagelayout-mydashboard #page.drawers {
    --drawer-width: 0px !important;
}
body.pagelayout-mydashboard.drawer-open-index .main-inner,
body.pagelayout-mydashboard .main-inner {
    margin-left: 0 !important;
    max-width: 100% !important;
}
body.limitedwidth.pagelayout-mydashboard .main-inner {
    max-width: 100% !important;
}
body.pagelayout-mydashboard .drawer.drawer-left,
body.pagelayout-mydashboard [data-region="left-hand-drawer"] {
    display: none !important;
    width: 0 !important;
}

/* ═══ V3: КАБИНЕТ УЧЕНИКА — dashboard layout ═══ */
body.pagelayout-mydashboard #region-main {
    display: block !important;
    max-width: 100% !important;
    width: 100% !important;
}
/* Все блоки на dashboard — полная ширина */
body.pagelayout-mydashboard #region-main > section,
body.pagelayout-mydashboard #region-main > div,
body.pagelayout-mydashboard #region-main > .block,
body.pagelayout-mydashboard .block_myoverview,
body.pagelayout-mydashboard .block_timeline,
body.pagelayout-mydashboard .block_calendar_month {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}

/* ═══ V3: BBB АКТИВНОСТЬ — большая кнопка "Войти в класс" ═══ */
.modtype_bigbluebuttonbn .activity-item,
li.activity.bigbluebuttonbn {
    background: linear-gradient(135deg, #1e3a5f 0%, #2a5298 100%) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    margin: 16px 0 !important;
    border: none !important;
}
/* BUG-054: Вся BBB карточка кликабельна */
.modtype_bigbluebuttonbn .activity-item {
    cursor: pointer !important;
    position: relative !important;
}
.modtype_bigbluebuttonbn .activity-name-area a {
    color: white !important;
    font-size: 1.2em !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
}
.modtype_bigbluebuttonbn .activity-name-area a::after {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
}
li.activity.bigbluebuttonbn .instancename {
    color: white !important;
    font-size: 1.2em !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
}
.modtype_bigbluebuttonbn .activity-icon,
li.activity.bigbluebuttonbn .activityiconcontainer {
    background: #E87722 !important;
    width: 48px !important;
    height: 48px !important;
    border-radius: 50% !important;
}
/* Кнопка Join Session */
.modtype_bigbluebuttonbn .btn,
li.activity.bigbluebuttonbn .btn {
    background: #E87722 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1em !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(232,119,34,0.4) !important;
}

/* ═══ V3: СТРАНИЦА КУРСА — layout с sidebar ═══ */
body.pagelayout-course #page-content {
    display: flex !important;
    gap: 24px !important;
    align-items: start !important;
}
body.pagelayout-course #region-main {
    flex: 1 !important;
    min-width: 0 !important;
}

/* ═══ V3: TEACHER VIEW — дополнительные элементы ═══ */
body.editing .activity-item {
    border-left: 4px solid #E87722 !important;
}

/* ═══ V3: SCHOOL DASHBOARD WIDGET ═══ */
#school-dashboard-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2a5298 100%);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    grid-column: 1 / -1;
}
#school-dashboard-header h2 {
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1.6em !important;
    margin: 0 0 6px !important;
}
#school-dashboard-header p {
    color: rgba(255,255,255,0.8) !important;
    margin: 0 !important;
}
#school-dashboard-header .next-lesson-badge {
    background: #E87722;
    border-radius: 12px;
    padding: 12px 20px;
    text-align: center;
    min-width: 160px;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}
#school-dashboard-header .next-lesson-badge:hover {
    opacity: 0.9 !important;
}
#school-dashboard-header .next-lesson-badge .time {
    font-size: 1.3em;
    font-weight: 700;
    display: block;
    color: white !important;
}
#school-dashboard-header .next-lesson-badge .label {
    font-size: 0.8em;
    opacity: 0.9;
    color: white !important;
}

/* ═══ V3: SCHOOL SIDEBAR WIDGET ═══ */
#school-sidebar {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    position: sticky;
    top: 72px;
}
#school-sidebar h3 {
    color: #1e3a5f !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1em !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin: 0 0 16px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #E87722 !important;
}
.school-lesson-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
}
.school-lesson-item:last-child { border-bottom: none; }
.school-lesson-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #E87722;
    flex-shrink: 0;
}
.school-lesson-dot.done { background: #10B981; }
.school-lesson-dot.upcoming { background: #ddd; }
.school-lesson-info { flex: 1; }
.school-lesson-info .subject {
    font-weight: 600;
    color: #1e3a5f;
    font-size: 0.9em;
}
.school-lesson-info .time-str {
    font-size: 0.8em;
    color: #888;
}

/* ═══ V3: TEACHER QUICK PANEL ═══ */
#school-teacher-panel {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    align-items: center;
}
#school-teacher-panel h3 {
    color: #1e3a5f !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    margin: 0 !important;
    flex-basis: 100%;
    font-size: 0.9em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.school-quick-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9em;
    text-decoration: none !important;
    transition: transform 0.15s, box-shadow 0.15s;
    cursor: pointer;
    border: none;
}
.school-quick-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.school-quick-btn.primary {
    background: linear-gradient(135deg, #E87722, #c45e10);
    color: white !important;
}
.school-quick-btn.secondary {
    background: #f0f4f8;
    color: #1e3a5f !important;
}

/* ═══ BUG-006: Скрыть футер "На платформе Moodle" ═══ */
.moove-container-fluid,
footer .moove-container-fluid,
.moove-footer-content,
#page-footer .logininfo,
.footer-content-debugging,
a[href="https://moodle.org"],
footer a[href*="moodle.org"],
.powered-by-moodle {
    display: none !important;
}

/* ═══ BUG-015: Скрыть toggle темы в navbar ═══ */
.darkmode-toggler,
[data-action="toggle-darkmode"],
.theme-dark-toggle,
.custom-control.custom-switch,
.navbar .custom-switch,
input[name="darkmode-toggle"],
.moove-darkmode-toggle {
    display: none !important;
}

/* ═══ BUG-016: Логотип — скрыть стандартную иконку темы ═══ */
.navbar-brand .logo,
.navbar-brand img:not(.user-avatar) {
    display: none !important;
}
/* Наш логотип через ::before уже задан выше — оставляем как есть */

/* ═══ BUG-013: Скрыть категории курсов для гостя ═══ */
body.notloggedin .coursebox,
body.notloggedin #frontpage-course-list,
body.notloggedin #frontpage-category-names,
body.notloggedin #frontpage-category-combo,
body.notloggedin .frontpage-course-list-all,
body.notloggedin [data-block="course_list"],
body.notloggedin .courses.frontpage-course-list-all {
    display: none !important;
}

/* ═══ BUG-010: BBB страница ожидания — стилизация ═══ */
.mod_bigbluebuttonbn .maincontent,
#bigbluebuttonbn_view_message_box {
    background: linear-gradient(135deg, #f8fafc 0%, #e8f0fe 100%) !important;
    border-radius: 16px !important;
    padding: 40px !important;
    text-align: center !important;
    max-width: 600px !important;
    margin: 40px auto !important;
    box-shadow: 0 4px 16px rgba(30,58,95,0.1) !important;
}
.mod_bigbluebuttonbn .maincontent::before,
#bigbluebuttonbn_view_message_box::before {
    content: '🎥';
    display: block;
    font-size: 48px;
    margin-bottom: 16px;
}
#bigbluebuttonbn_view_message_box span,
.mod_bigbluebuttonbn .maincontent p {
    font-size: 1.2em !important;
    color: #1e3a5f !important;
    font-weight: 600 !important;
}

/* ═══ BUG-011: BBB warning banner — стилизовать ═══ */
.mod_bigbluebuttonbn .alert-warning,
.mod_bigbluebuttonbn .alert-danger {
    border-radius: 12px !important;
    border: 1px solid #E87722 !important;
    background: #fff7ed !important;
    color: #92400e !important;
    font-size: 0.85em !important;
}

/* ═══ BUG-009: Assign карточка "Состояние ответа" ═══ */
.path-mod-assign .submissionstatustable,
.path-mod-assign .submissionstatustable .generaltable {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #E7E5E4 !important;
}
.path-mod-assign .submissionstatustable th {
    background: #1e3a5f !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}
.path-mod-assign .submissionstatustable td {
    padding: 10px 16px !important;
    border-bottom: 1px solid #f0f0f0 !important;
}
.path-mod-assign .submissionstatustable .lastcol a,
.path-mod-assign [data-action="grading"] {
    background: #E87722 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    text-decoration: none !important;
}

/* ═══ BUG-014: Quiz попытки — стилизация ═══ */
.path-mod-quiz .quizattemptsummary,
.path-mod-quiz .generaltable {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #E7E5E4 !important;
}
.path-mod-quiz .quizattemptsummary th,
.path-mod-quiz .generaltable thead th {
    background: #1e3a5f !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}
.path-mod-quiz .quizattemptsummary td,
.path-mod-quiz .generaltable td {
    padding: 10px 16px !important;
}

/* ═══ BUG-003: Скрыть пустую Шкалу времени, уменьшить Календарь ═══ */
body.pagelayout-mydashboard .block_timeline {
    max-height: 200px !important;
    overflow: hidden !important;
}
/* Скрыть календарь и Шкалу времени на dashboard — ученику не нужно */
body.pagelayout-mydashboard .block_calendar_month,
body.pagelayout-mydashboard .block_calendar_upcoming,
body.pagelayout-mydashboard .block_timeline {
    display: none !important;
}
/* Если timeline пустой — скрыть через CSS (empty data region) */
body.pagelayout-mydashboard .block_timeline [data-region="no-events-empty-message"] {
    display: none !important;
}

/* ═══ Футер: скрыть Moodle, показать наш ═══ */
#page-footer .moove-container-fluid,
#page-footer .footer-columns,
footer .tool_dataprivacy,
#page-footer .logininfo,
.footer-content-debugging,
#page-footer a[href*="moodle.org"],
.footer-content .tool_usertours-resettourcontainer {
    display: none !important;
}
/* Наш брендированный футер */
#page-footer {
    display: block !important;
    background: #1e3a5f !important;
    color: rgba(255,255,255,0.7) !important;
    padding: 24px 0 !important;
    text-align: center !important;
    font-size: 14px !important;
}
#page-footer::before {
    content: 'Онлайн-школа EasyDays · Начальная школа · 1–4 класс' !important;
    display: block !important;
    color: rgba(255,255,255,0.9) !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
}
#page-footer::after {
    content: '© 2026 EasyDays Samui · support@easydayssamui.com' !important;
    display: block !important;
    color: rgba(255,255,255,0.5) !important;
    font-size: 12px !important;
}

/* ═══ BUG-010: BBB waiting page ═══ */
body.path-mod-bigbluebuttonbn #region-main-box {
    display: flex !important;
    justify-content: center !important;
    align-items: flex-start !important;
    min-height: 50vh !important;
}
body.path-mod-bigbluebuttonbn #region-main {
    max-width: 650px !important;
    margin: 40px auto !important;
    background: linear-gradient(135deg, #f8fafc 0%, #e8f0fe 100%) !important;
    border-radius: 20px !important;
    padding: 48px 40px !important;
    box-shadow: 0 8px 32px rgba(30,58,95,0.1) !important;
    text-align: center !important;
}
body.path-mod-bigbluebuttonbn h2 {
    color: #1e3a5f !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1.8em !important;
}

/* ═══ BUG-013 partial: Убрать артефакты на мобильной frontpage ═══ */
body.notloggedin .course-section,
body.notloggedin .courses,
body.notloggedin .category-browse,
body.notloggedin #region-main .box.py-3.generalbox,
body.notloggedin .frontpage-course-list-enrolled,
body.notloggedin.pagelayout-frontpage #region-main > div:not(.hero-section):not(#school-hero) {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
body.notloggedin.pagelayout-frontpage #region-main,
body.notloggedin.pagelayout-frontpage #region-main-box,
body.notloggedin.pagelayout-frontpage #topofscroll,
body.notloggedin.pagelayout-frontpage .main-inner,
body.notloggedin.pagelayout-frontpage #page-content {
    min-height: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    height: auto !important;
}

/* ═══ BUG-016: Логотип — скрыть ВСЕ img внутри navbar-brand ═══ */
.navbar-brand > img,
.navbar-brand img {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}
/* Увеличить наш CSS-логотип */
.navbar-brand::before {
    width: 40px !important;
    height: 40px !important;
    margin-right: 8px !important;
}

/* ═══ BUG-019: Карточки на /my/courses.php ═══ */
body.path-my .card.course-card,
body.pagelayout-mycourses .card.course-card,
.courses-view-course-category .card,
[data-region="courses-view"] .card {
    border-radius: 16px !important;
    border: 1px solid #E7E5E4 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s !important;
    overflow: hidden !important;
}
body.path-my .card.course-card:hover,
body.pagelayout-mycourses .card.course-card:hover,
[data-region="courses-view"] .card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(30,58,95,0.15) !important;
    border-color: #E87722 !important;
}

/* ═══ BUG-020: Мобильные секции курса — gaps ═══ */
@media (max-width: 768px) {
    .course-content .course-section {
        margin-bottom: 12px !important;
        border: 1px solid #E7E5E4 !important;
        border-radius: 12px !important;
        padding: 8px !important;
        background: white !important;
    }
    .course-content .course-section-header {
        padding: 8px 12px !important;
        background: #f0f4f8 !important;
        border-radius: 8px 8px 0 0 !important;
    }
}

/* ═══ BUG-009: Расширенные селекторы для assign ═══ */
.path-mod-assign .generaltable,
.path-mod-assign table.flexible {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #E7E5E4 !important;
}
.path-mod-assign .generaltable th,
.path-mod-assign table.flexible th {
    background: #1e3a5f !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}

/* ═══ BUG-011: BBB alert — доп. селекторы ═══ */
.path-mod-bigbluebuttonbn .alert,
body.path-mod-bigbluebuttonbn .alert-warning {
    border-radius: 12px !important;
    border: 1px solid #E87722 !important;
    background: #fff7ed !important;
    color: #92400e !important;
    font-size: 0.85em !important;
    margin-bottom: 20px !important;
}

/* ═══ BUG-004: XP виджет — скрыть весь intro блок, показать один русский текст ═══ */
.block_xp .card-text.content,
.block_xp .introduction {
    display: none !important;
}
/* Показать русский текст ОДИН РАЗ через card-body ::after */
.block_xp .card-body::after {
    content: 'Выполняйте задания и получайте очки опыта!' !important;
    font-size: 13px !important;
    color: #57534E !important;
    display: block !important;
    line-height: 1.4 !important;
    margin-top: 8px !important;
}
/* Скрыть "Level up!" заголовок (на EN) */
.block_xp .card-title:first-child {
    font-size: 0 !important;
    line-height: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}
.block_xp .card-title:first-child::after {
    content: 'Очки опыта' !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1e3a5f !important;
    display: block !important;
    line-height: 1.4 !important;
    height: auto !important;
}

/* ═══ BUG-016: Логотип — загрузить с сервера вместо внешнего URL ═══ */
.navbar-brand::before {
    background-image: url('/pix/school-logo.png') !important;
}

/* ═══ BUG-021: Mobile приветствие responsive ═══ */
@media (max-width: 480px) {
    #school-dashboard-header {
        padding: 16px !important;
        flex-direction: column !important;
    }
    #school-dashboard-header h2 {
        font-size: 1.2em !important;
    }
    #school-dashboard-header p {
        font-size: 0.85em !important;
    }
    #school-dashboard-header .school-badge {
        margin-top: 8px !important;
        align-self: flex-start !important;
    }
}

/* ═══ BUG-009+014: Все таблицы Moodle на страницах активностей ═══ */
.path-mod table.generaltable,
.path-mod table.flexible,
.path-mod .submissionstatustable {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #E7E5E4 !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
}
.path-mod table.generaltable th,
.path-mod table.flexible th,
.path-mod .submissionstatustable th {
    background: #1e3a5f !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    border: none !important;
}
.path-mod table.generaltable td,
.path-mod table.flexible td,
.path-mod .submissionstatustable td {
    padding: 10px 16px !important;
    border-bottom: 1px solid #f0f0f0 !important;
    border-top: none !important;
}

/* ═══ BUG-029: Navbar active/focus ring ═══ */
.navbar a:focus, .navbar a:active,
.navbar .nav-link:focus, .navbar .nav-link:active,
#school-nav-links a:focus, #school-nav-links a:active {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
    background: rgba(255,255,255,0.1) !important;
}

/* ═══ BUG-025: Drawer — не менять position, только z-index ═══ */
.drawer {
    z-index: 1029 !important;
}

/* ═══ BUG-030: Профиль студента ═══ */
.path-user .userprofile .profile_tree section {
    background: white !important;
    border-radius: 12px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

/* ═══ BUG-031: Настройки — карточки ═══ */
.path-user .preferences-groups .preferences-group {
    background: white !important;
    border-radius: 12px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.path-user .preferences-groups a {
    color: #1e3a5f !important;
    font-weight: 500 !important;
}

/* ═══ BUG-032: Forgot password — добавить ссылку назад ═══ */
body.pagelayout-login .login-form-forgotpassword::after {
    content: 'Вернуться на страницу входа' !important;
    display: block !important;
    margin-top: 16px !important;
    color: #E87722 !important;
    cursor: pointer !important;
    text-align: center !important;
}

/* ═══ BUG-033: Кнопки фильтров — оранжевые ═══ */
.btn-primary {
    background-color: #E87722 !important;
    border-color: #E87722 !important;
}
.btn-primary:hover {
    background-color: #c45e10 !important;
    border-color: #c45e10 !important;
}
.btn-outline-secondary {
    border-color: #1e3a5f !important;
    color: #1e3a5f !important;
}

/* Скрыть shortname курса (LIT-1, MAT-1 и т.д.) — техническое название */
.card.course-card .text-muted[data-region="shortenedcoursename"],
.card.course-card .categoryname,
.card.course-card .course-card-category,
.coursebox .coursecat,
.course-card .text-muted:first-child,
[data-region="shortenedcoursename"] {
    display: none !important;
}

/* Скрыть "Легенда событий" popup и ненужные элементы календаря */
.calendarwrapper .calendar-controls .btn[data-action="filter-events"],
[data-region="calendar-filter"],
.calendar_filters,
.calendar-legend,
.calendarwrapper .btn-group,
.calendar_event_course .calendar-circle {
    display: none !important;
}
/* Скрыть "Новое событие" для студента */
body:not(.role-admin) .calendarwrapper .btn[data-action="new-event"],
.calendar-controls .btn-primary[data-action="new-event"] {
    display: none !important;
}

/* ═══ BUG-037: Скрыть синие drawer toggle кнопки ═══ */
.drawer-toggler,
button.drawer-toggler,
[data-toggler="drawers"],
.btn-icon.drawer-toggle,
button[aria-controls*="drawer"] {
    display: none !important;
}

/* ═══ BUG-036: BBB иконка — скрыть "б", показать камеру ═══ */
.modtype_bigbluebuttonbn .activityiconcontainer img,
.modtype_bigbluebuttonbn .activityicon {
    visibility: hidden !important;
    width: 0 !important;
}
.modtype_bigbluebuttonbn .activityiconcontainer::after {
    content: '🎥' !important;
    font-size: 24px !important;
    display: inline-block !important;
}

/* ═══ BUG-040: Mobile фильтры myoverview — повторно скрыть ═══ */
@media (max-width: 768px) {
    .block_myoverview [data-region="filter"],
    .block_myoverview [data-region="courses-view-dropdown"],
    .block_myoverview .dropdown,
    .block_myoverview input[type="search"],
    .block_myoverview .header-action,
    .block_myoverview .block-header,
    .block_myoverview .card-header {
        display: none !important;
    }
}

/* ═══ BUG-044: Frontpage "В начало" — убрать ═══ */
body.notloggedin .primary-navigation {
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
    max-height: 0 !important;
    position: absolute !important;
    width: 0 !important;
    opacity: 0 !important;
}

/* ═══ BUG-045: Mobile footer ═══ */
@media (max-width: 768px) {
    #page-footer .moove-container-fluid,
    #page-footer .footer-columns {
        display: none !important;
    }
}

/* ═══ BUG-053 КРИТИЧЕСКИЙ: Скролл должен работать ВСЕГДА ═══ */
body, html, #page, #page-wrapper, #page-content, #topofscroll, .main-inner {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: auto !important;
    max-height: none !important;
}

/* ═══ BUG-052: Drawer — убрать chevrons, CAPS, обрезку ═══ */
.courseindex .courseindex-section-title .collapsed-icon,
.courseindex .courseindex-section-title .expanded-icon,
.courseindex .courseindex-chevron {
    display: none !important;
}
.courseindex .courseindex-section-title,
.courseindex .courseindex-item-content a {
    text-transform: none !important;
    white-space: normal !important;
    word-wrap: break-word !important;
}

/* ═══ Drawer — верхняя граница совпадает с navbar (56+3=59px) ═══ */
.drawer, #theme_moove-drawers-courseindex {
    top: 59px !important;
    border-right: none !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05) !important;
}

/* ═══ BBB записи — responsive таблица ═══ */
.bbb-recordings-table,
.mod_bigbluebuttonbn table {
    max-width: 100% !important;
    overflow-x: auto !important;
    display: block !important;
    font-size: 14px !important;
}

/* ═══ Drawer правый край — убрать двойную линию ═══ */
.drawer {
    border-right: none !important;
}
#page-content {
    border-left: none !important;
}

/* ═══ BUG-056: Скрыть пустую таблицу записей BBB ═══ */
.mod_bigbluebuttonbn .bbb-recordings-table:empty,
.mod_bigbluebuttonbn table:has(td:only-child),
.path-mod-bigbluebuttonbn .yui3-datatable,
.path-mod-bigbluebuttonbn .bbb_recordings_table {
    display: none !important;
}
/* Скрыть пагинацию записей если нет данных */
.path-mod-bigbluebuttonbn .pagination,
.path-mod-bigbluebuttonbn nav[aria-label="pagination"] {
    display: none !important;
}

/* ═══ BUG-057: BBB навигация — компактно ═══ */
.path-mod-bigbluebuttonbn .activity-navigation,
.path-mod-bigbluebuttonbn [data-region="activity-navigation"] {
    max-width: 400px !important;
    margin: 16px auto !important;
}

/* ═══ BUG-043: Mobile navbar — "Мои предметы" не "Мои уроки" ═══ */
@media (max-width: 768px) {
    .moove-custom-nav .nav-link[href*="courses"] {
        font-size: 0 !important;
    }
    .moove-custom-nav .nav-link[href*="courses"]::after {
        content: 'Мои предметы' !important;
        font-size: 14px !important;
    }
}

/* ═══ BUG-059: Скрыть "Новое событие" для студента ═══ */
body:not(.role-admin):not(.role-editingteacher):not(.role-teacher) .calendarwrapper .btn[data-action="new-event"],
body:not(.role-admin):not(.role-editingteacher):not(.role-teacher) .calendar-controls .btn-primary {
    display: none !important;
}

/* ═══ BUG-061: Контент не наезжает на navbar/footer ═══ */
.navbar.fixed-top {
    z-index: 1040 !important;
}
#page-footer {
    z-index: 1035 !important;
    position: relative !important;
}
#topofscroll, .main-inner {
    margin-top: 0 !important;
}

/* ═══ BUG-052 reopened: Drawer — отступы между секциями ═══ */
.courseindex .courseindex-section {
    margin-bottom: 4px !important;
    padding: 4px 0 !important;
    border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}
.courseindex .courseindex-item-content {
    padding-left: 12px !important;
}

/* ═══ BUG-063: Расписание — скрыть техническую информацию ═══ */
.calendar_event_course .description,
.calendar_event_course .location,
[data-type="event"] .col-11 small,
.calendarwrapper .calendar-controls select,
.calendarwrapper [data-action="filter-events"] {
    display: none !important;
}
/* Упростить карточку события */
.calendar_event_course {
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin-bottom: 4px !important;
}

</style>"""

# ─── TOPOFBODY ───────────────────────────────────────────────────────────────
TOPOFBODY = """<div id="school-hero" style="background:linear-gradient(135deg,#E87722 0%,#c45e10 100%);color:white;text-align:center;padding:48px 20px 40px;margin-bottom:0;">
<p style="font-size:0.95em;opacity:0.85;letter-spacing:2px;text-transform:uppercase;margin:0 0 10px;">Онлайн-школа</p>
<h1 style="font-size:2.4em;margin:0 0 16px;font-weight:700;line-height:1.2;">Начальная школа<br>для детей за рубежом</h1>
<p style="font-size:1.1em;opacity:0.9;max-width:520px;margin:0 auto 28px;">Программа «Школа России», 1–4 класс. Группы 3–5 человек.</p>
<a href="/my/" style="background:white;color:#E87722;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.1em;display:inline-block;">Войти в личный кабинет</a>
</div>
<div id="school-login-header" style="flex-direction:column;align-items:center;padding:44px 20px 28px;color:white;text-align:center;">
<img src="/pix/school-logo.png" style="max-height:62px;width:auto;margin-bottom:14px;filter:brightness(0) invert(1);" alt="Онлайн-школа" onerror="this.style.display='none'">
<div style="color:white;font-size:1.8em;margin:0 0 8px;font-weight:700;line-height:1.2;">Онлайн-школа</div>
<div style="color:rgba(255,255,255,0.8);font-size:0.92em;">Начальная школа · 1–4 класс</div>
</div>"""

# ─── BOTTOMOFPAGE: JavaScript DOM manipulation ────────────────────────────────
BOTTOMOFPAGE = """<script>
(function() {
'use strict';

var path = window.location.pathname;
var isDashboard = path === '/my/' || path === '/my/index.php';

// Логотип → /my/ вместо /
var brand = document.querySelector('.navbar-brand');
// Лого → /my/ (dashboard), дубль с "Мои предметы" = ОК, лого это shortcut
if (brand) {
    brand.href = '/my/';
    brand.title = 'На главную';
}
// Скрыть стандартные nav items (В начало, Дополнительно) — только для залогиненных
if (!document.body.classList.contains('notloggedin')) {
document.querySelectorAll('.primary-navigation .nav-item').forEach(function(item) {
    var link = item.querySelector('a');
    if (link) {
        var text = link.textContent.trim();
        if (text === 'В начало' || text === 'Дополнительно' || text === 'Home' || text === 'More') {
            item.style.display = 'none';
        }
    }
});
// Также скрыть весь dropdownmoremenu
document.querySelectorAll('.dropdownmoremenu, .moremenu').forEach(function(el) {
    el.style.display = 'none';
});
} // end notloggedin check

// Кастомное навигационное меню (только для залогиненных)
if (!document.getElementById('school-nav-links') && !document.body.classList.contains('notloggedin')) {
    var navContainer = document.querySelector('.navbar .navbar-nav, .navbar');
    if (brand && brand.parentElement) {
        var navLinks = document.createElement('div');
        navLinks.id = 'school-nav-links';
        navLinks.innerHTML = '<a href="/my/courses.php">Мои предметы</a><a href="/calendar/view.php">Расписание</a><a href="/message/index.php">Сообщения</a>';
        brand.parentElement.insertBefore(navLinks, brand.nextSibling);
    }
}
var isCourse = path.indexOf('/course/') !== -1;
var isTeacher = !!document.querySelector(
  '.editmode-switch-form, [data-action="toggle-editing"], .editing-mode-toggle-on, .editing-mode-toggle, input[name="setmode"]'
);

function getGreeting() {
    var h = (new Date().getUTCHours() + 7) % 24;
    if (h >= 5 && h < 12) return 'Доброе утро';
    if (h >= 12 && h < 17) return 'Добрый день';
    if (h >= 17 && h < 22) return 'Добрый вечер';
    return 'Добрый вечер';
}

function getUserName() {
    var selectors = [
        '.usermenu .usertext',
        '.logininfo a',
        '[data-username]',
        '#usernavigation .nav-link span'
    ];
    for (var i = 0; i < selectors.length; i++) {
        var el = document.querySelector(selectors[i]);
        if (el && el.textContent.trim()) {
            return el.textContent.trim().split(' ')[0];
        }
    }
    return '';
}

// ═══ CLOSE LEFT DRAWER ON DASHBOARD ═══
if (isDashboard) {
    document.body.classList.remove('drawer-open-index');
    var leftDrawer = document.querySelector('.drawer-left, [data-region="left-hand-drawer"]');
    if (leftDrawer) { leftDrawer.style.display = 'none'; leftDrawer.style.width = '0'; }
    var pageEl = document.getElementById('page');
    if (pageEl) { pageEl.style.setProperty('--drawer-width', '0px', 'important'); }
    var mainInner = document.querySelector('.main-inner');
    if (mainInner) { mainInner.style.marginLeft = '0'; mainInner.style.maxWidth = '100%'; }
}

// ═══ DASHBOARD ═══
if (isDashboard) {
    var mainContent = document.querySelector('#region-main');
    if (mainContent) {
        var firstChild = mainContent.firstElementChild;
        if (firstChild) {
            var name = getUserName();
            var greeting = getGreeting();

            // Приветственный заголовок
            var header = document.createElement('div');
            header.id = 'school-dashboard-header';
            header.innerHTML =
                '<div>' +
                '<h2>' + greeting + (name ? (', ' + name) : '') + '!</h2>' +
                '<p>Программа «Школа России» · Начальная школа · 1–4 класс</p>' +
                '</div>' +
                '<a href="/calendar/view.php" class="next-lesson-badge" style="text-decoration:none;color:white">' +
                '<span class="time">Скоро урок</span>' +
                '<span class="label">Смотреть расписание</span>' +
                '</a>' +
                '</div>';
            mainContent.insertBefore(header, firstChild);
        }
    }

    // Sidebar с расписанием
    var myoverview = document.querySelector('.block_myoverview');
    if (myoverview) {
        var sidebar = document.createElement('div');
        sidebar.id = 'school-sidebar';
        // Берём реальные события из блока "Предстоящие события"
        var events = document.querySelectorAll('.block_calendar_upcoming .event, [data-region="event-list-content-events"] [data-type="event"]');
        var lessonsHTML = '<h3>Ближайшие уроки</h3>';
        if (events.length > 0) {
            events.forEach(function(ev, i) {
                if (i >= 5) return;
                var name = ev.querySelector('.name, a')?.textContent?.trim() || '';
                var timeEl = ev.querySelector('.date, small, .col-11')?.textContent?.trim() || '';
                lessonsHTML += '<div class="school-lesson-item"><div class="school-lesson-dot' + (i === 0 ? '' : ' upcoming') + '"></div><div class="school-lesson-info"><div class="subject">' + name + '</div><div class="time-str">' + timeEl + '</div></div></div>';
            });
        } else {
            lessonsHTML += '<p style="color:#57534E;font-size:0.9em">Расписание в <a href="/calendar/view.php" style="color:#E87722">календаре</a></p>';
        }
        sidebar.innerHTML = lessonsHTML;

        // Ссылки на курсы из карточек
        var courseCards = document.querySelectorAll('.card.course-card .coursename.aalink, .card.course-card .card-title a, .aalink.coursename');
        if (courseCards.length > 0) {
            var coursesHeader = document.createElement('h3');
            coursesHeader.style.marginTop = '20px';
            coursesHeader.textContent = 'Мои предметы';
            sidebar.appendChild(coursesHeader);

            courseCards.forEach(function(card) {
                var item = document.createElement('div');
                item.className = 'school-lesson-item';
                item.innerHTML =
                    '<div class="school-lesson-dot done"></div>' +
                    '<div class="school-lesson-info"><div class="subject">' +
                    '<a href="' + card.href + '" style="color:#1e3a5f;text-decoration:none">' +
                    card.textContent.trim() +
                    '</a></div></div>';
                sidebar.appendChild(item);
            });
        }

        myoverview.parentNode.insertBefore(sidebar, myoverview.nextSibling);
    }
}

// ═══ СТРАНИЦА КУРСА ═══
// Если на section.php — добавить навигацию "Все уроки"
if (path.indexOf('/course/section.php') !== -1) {
    var backLink = document.createElement('a');
    var courseLink = document.querySelector('#courseindex a[href*="/course/view.php"], .breadcrumb a[href*="/course/view.php"]');
    backLink.href = courseLink ? courseLink.href : '/my/courses.php';
    backLink.innerHTML = '← Все уроки предмета';
    backLink.style.cssText = 'display:inline-block;margin:12px 16px;padding:8px 16px;background:#f0f4f8;border-radius:8px;color:#1e3a5f;text-decoration:none;font-weight:600;font-size:14px';
    var regionMain = document.getElementById('region-main');
    if (regionMain) regionMain.insertBefore(backLink, regionMain.firstChild);
}

if (isCourse) {
    // Стилизуем BBB активности
    var bbbItems = document.querySelectorAll('.modtype_bigbluebuttonbn');
    bbbItems.forEach(function(item) {
        // Badge "Живой урок" (один раз, без дублей)
        if (item.querySelector('.school-bbb-badge')) return;
        var nameArea = item.querySelector('.activity-name-area');
        if (nameArea) {
            var badge = document.createElement('span');
            badge.className = 'school-bbb-badge';
            badge.style.cssText = 'background:#E87722;color:white;padding:3px 10px;border-radius:20px;font-size:0.75em;font-weight:700;margin-left:12px;vertical-align:middle;display:inline-block';
            badge.textContent = 'ЖИВОЙ УРОК';
            nameArea.appendChild(badge);
        }
    });

    // Панель учителя
    if (isTeacher) {
        var courseContent = document.querySelector('.course-content, #region-main');
        if (courseContent) {
            var courseId = new URLSearchParams(window.location.search).get('id') || '2';

            var panel = document.createElement('div');
            panel.id = 'school-teacher-panel';
            panel.innerHTML =
                '<h3>Панель учителя</h3>' +
                '<a href="/grade/report/grader/index.php?id=' + courseId + '" class="school-quick-btn secondary">📊 Журнал оценок</a>' +
                '<a href="/user/index.php?id=' + courseId + '" class="school-quick-btn secondary">👥 Список учеников</a>' +
                '<a href="/mod/assign/index.php?id=' + courseId + '" class="school-quick-btn secondary">📝 Задания</a>' +
                '<a href="/report/participation/index.php?id=' + courseId + '" class="school-quick-btn secondary">📈 Активность</a>' +
                '<a href="#" class="school-quick-btn primary" onclick="alert(&quot;Нажмите на Онлайн-урок в списке тем&quot;);return false">🎥 Начать урок</a>';

            courseContent.insertBefore(panel, courseContent.firstChild);
        }
    }
}

// ═══ ФУТЕР — ссылки ═══
var footer = document.getElementById('page-footer');
if (footer && !footer.querySelector('.school-footer-links')) {
    var links = document.createElement('div');
    links.className = 'school-footer-links';
    links.style.cssText = 'margin-top:12px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap';
    links.innerHTML = '<a href="https://samuidays2103-creator.github.io/russchool-online/" target="_blank" style="color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px">О школе</a>' +
        '<a href="/my/courses.php" style="color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px">Мои предметы</a>' +
        '<a href="/calendar/view.php" style="color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px">Расписание</a>' +
        '<a href="mailto:support@easydayssamui.com" style="color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px">Поддержка</a>';
    footer.appendChild(links);
}

// ═══ ЗАМЕНА "курс" → "предмет" в тексте страницы ═══
document.querySelectorAll('*').forEach(function(el) {
    if (el.children.length === 0 && el.textContent) {
        var t = el.textContent;
        if (t.includes('элемент курса')) el.textContent = t.replace(/элемент курса/g, 'задание');
        if (t.includes('Следующий задание')) el.textContent = t.replace('Следующий задание', 'Следующее задание');
        if (t.includes('Обзор курсов')) el.textContent = t.replace(/Обзор курсов/g, 'Обзор предметов');
        if (t.includes('Все курсы')) el.textContent = t.replace('Все курсы', 'Все предметы');
        if (t.includes('События курса')) el.textContent = t.replace('События курса', 'Уроки');
        if (t.includes('No data to display')) el.textContent = t.replace('No data to display', 'Нет записей');
        if (t.includes('No data')) el.textContent = t.replace('No data', 'Нет данных');
        if (t.includes('курса')) el.textContent = t.replace(/курса/g, 'предмета');
        if (t.includes('курсы')) el.textContent = t.replace(/курсы/g, 'предметы');
        if (t.includes('курс ')) el.textContent = t.replace(/курс /g, 'предмет ');
    }
});

// Повторить замену через 2 сек (Moodle рендерит AJAX после load)
setTimeout(function() {
    document.querySelectorAll('*').forEach(function(el) {
        if (el.children.length === 0 && el.textContent) {
            var t = el.textContent;
            if (t.includes('элемент курса')) el.textContent = t.replace(/элемент курса/g, 'задание');
            if (t.includes('Следующий задание')) el.textContent = t.replace('Следующий задание', 'Следующее задание');
            if (t.includes('No data')) el.textContent = t.replace('No data', 'Нет данных');
            if (t.includes('Обзор курсов')) el.textContent = t.replace(/Обзор курсов/g, 'Обзор предметов');
        }
    });
}, 2000);

// ═══ ОБЩИЕ УЛУЧШЕНИЯ ═══
// Кнопка scroll-to-top
var scrollBtn = document.createElement('button');
scrollBtn.innerHTML = '↑';
scrollBtn.title = 'Наверх';
scrollBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;width:44px;height:44px;border-radius:50%;background:#1e3a5f;color:white;border:none;font-size:1.2em;cursor:pointer;opacity:0;transition:opacity 0.3s;z-index:9999;box-shadow:0 2px 12px rgba(0,0,0,0.2);line-height:1;display:flex;align-items:center;justify-content:center';
scrollBtn.onclick = function() { window.scrollTo({top:0, behavior:'smooth'}); };
document.body.appendChild(scrollBtn);
window.addEventListener('scroll', function() {
    scrollBtn.style.opacity = window.scrollY > 300 ? '1' : '0';
});

// Убираем edit-иконки для не-редактирующего режима
if (!document.querySelector('body.editing')) {
    var editControls = document.querySelectorAll('.block-controls .dropdown');
    editControls.forEach(function(el) { el.style.visibility = 'hidden'; });
}

})();
</script>"""


# ─── MAIN ────────────────────────────────────────────────────────────────────
print("=" * 60)
print("apply_theme_v3.py — Platform v3")
print("Dashboard widgets + Teacher panel + BBB styling + JS DOM")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.set_default_timeout(45000)

    # ── 1. Login ──────────────────────────────────────────────────────────────
    print("\n[1/4] Logging in as admin...")
    page.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded")
    page.fill("#username", "admin")
    page.fill("#password", "Admin2026!")
    page.click("#loginbtn")
    page.wait_for_url(lambda u: "/login" not in u, timeout=30000)
    print("  ✓ Logged in")

    # ── 2. Apply CSS + TOPOFBODY + BOTTOMOFPAGE ───────────────────────────────
    print("\n[2/4] Applying CSS/HTML to Additional HTML settings...")
    page.goto(f"{BASE}/admin/settings.php?section=additionalhtml", wait_until="networkidle")

    # HEAD (CSS)
    head_ta = page.locator('textarea[name="s__additionalhtmlhead"]')
    head_ta.fill(CSS)
    print("  ✓ CSS filled in head textarea")

    # TOP OF BODY
    top_ta = page.locator('textarea[name="s__additionalhtmltopofbody"]')
    top_ta.fill(TOPOFBODY)
    print("  ✓ Top-of-body HTML filled")

    # BOTTOM OF PAGE / FOOTER (JavaScript)
    # Moodle 4.5 uses s__additionalhtmlfooter instead of bottomofpage
    try:
        bottom_ta = page.locator('textarea[name="s__additionalhtmlfooter"]')
        if bottom_ta.is_visible(timeout=5000):
            bottom_ta.fill(BOTTOMOFPAGE)
            print("  ✓ Bottom JS filled (footer)")
        else:
            print("  ~ footer textarea not visible, skipping")
    except Exception as e:
        print(f"  ~ footer textarea: {e}")

    # Save
    page.locator('button:has-text("Save changes")').click()
    page.wait_for_load_state('networkidle')
    print("  ✓ Settings saved")

    # ── 3. Purge caches ───────────────────────────────────────────────────────
    print("\n[3/4] Purging caches...")
    page.goto(f"{BASE}/admin/purgecaches.php", wait_until="networkidle")
    purged = False
    for sel in ['input[type=submit]', 'button[type=submit]', 'button:has-text("Purge")']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=3000):
                btn.click()
                page.wait_for_load_state('networkidle')
                print("  ✓ Caches purged")
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
                print("  ✓ Caches purged (retry)")
        except Exception as e:
            print(f"  ! Cache purge skipped: {e}")

    time.sleep(3)

    # ── 4. Screenshots ────────────────────────────────────────────────────────
    print("\n[4/4] Taking screenshots...")

    def shot(name, url, user=None, mobile=False, scroll_y=0):
        vp = {"width": 390, "height": 844} if mobile else {"width": 1440, "height": 900}
        c = browser.new_context(viewport=vp)
        pg = c.new_page()
        pg.set_default_timeout(40000)
        try:
            if user:
                pg.goto(f"{BASE}/login/index.php", wait_until="domcontentloaded")
                time.sleep(1)
                pg.fill("#username", user[0])
                pg.fill("#password", user[1])
                pg.click("#loginbtn")
                pg.wait_for_url(lambda u: "/login" not in u, timeout=30000)
            pg.goto(url, wait_until="networkidle")
            time.sleep(1)
            if scroll_y:
                pg.evaluate(f"window.scrollTo(0, {scroll_y})")
                time.sleep(0.5)
            pg.screenshot(path=f"screenshots/{name}.png", full_page=(scroll_y == 0))
            print(f"  ✓ {name}.png")
        except Exception as e:
            print(f"  ✗ {name}: {type(e).__name__}: {str(e)[:120]}")
        finally:
            c.close()

    # Страница входа
    shot("login_final",          f"{BASE}/login/index.php")

    # Dashboard студента
    shot("dashboard_student",    f"{BASE}/my/",
         user=("ivanov_misha", "Test1234!"))

    # Dashboard студента — мобиль
    shot("dashboard_student_mobile", f"{BASE}/my/",
         user=("ivanov_misha", "Test1234!"), mobile=True)

    # Страница курса (студент, курс 2 = RUS-1)
    shot("course_student",       f"{BASE}/course/view.php?id=2",
         user=("ivanov_misha", "Test1234!"))

    # Страница курса (admin/teacher — с панелью учителя)
    shot("course_teacher",       f"{BASE}/course/view.php?id=2",
         user=("admin", "Admin2026!"))

    # Журнал оценок
    shot("grades_teacher",       f"{BASE}/grade/report/grader/index.php?id=2",
         user=("admin", "Admin2026!"))

    # Список учеников
    shot("students_list",        f"{BASE}/user/index.php?id=2",
         user=("admin", "Admin2026!"))

    # Доп: мобиль курса
    shot("course_student_mobile", f"{BASE}/course/view.php?id=2",
         user=("ivanov_misha", "Test1234!"), mobile=True)

    browser.close()

print("\n" + "=" * 60)
print("✓ apply_theme_v3.py DONE")
print("=" * 60)
