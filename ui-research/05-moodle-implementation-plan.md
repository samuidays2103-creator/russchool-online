# Moodle UI Redesign v2 — Implementation Plan
## Дата: 2026-03-24 (Bangkok UTC+7)
## Основан на: анализ 10 платформ (Foxford, Умскул, Skysmart, Khan Academy, Duolingo, etc.)

## Что реализовано в v2

### 1. Шрифты — Golos Text + Nunito [HIGH] ✓
- Golos Text: российская гарнитура, идеальная кириллица
- Nunito: для заголовков, дружелюбный, округлый
- Источник: Google Fonts, display=swap, preconnect

### 2. Тёмный navbar [HIGH] ✓
- Фон: #1e3a5f, оранжевая полоска снизу #E87722
- Белые ссылки, оранжевый hover
- Источник паттерна: Skysmart, Foxford, Skyeng

### 3. Тёплый фон [MED] ✓
- #FAFAF9 (stone-50) вместо холодного белого
- Ощущение "домашнего пространства"
- Источник: исследование паттернов §1.1

### 4. Карточки курсов — hover-эффект [HIGH] ✓
- border-radius: 16px
- transform: translateY(-4px) при hover
- border-color: #E87722 при hover
- Источник: все лидеры, §1.5

### 5. Страница курса — секции и активности [HIGH] ✓
- Секции: white cards с primary border-bottom
- Активности: hover подсветка
- Иконки: цветные по типу

### 6. Course Index Drawer [MED] ✓
- Брендовые цвета
- Active state с оранжевой левой полоской

### 7. CSS Variables — единая система [MED] ✓
- :root переменные для всех цветов
- Легко обновлять

### 8. Таблицы оценок [MED] ✓
- Тёмная шапка таблицы (#1e3a5f)
- hover строк

### 9. Кнопки улучшены [MED] ✓
- box-shadow, transition, hover lift

## Что НЕ реализовано в v2 (требует backend/плагины)

### 10. Прогресс ученика на dashboard — НУЖЕН ПЛАГИН
- В Moodle нужен блок Activity Completion Summary
- CSS недостаточно — нужна PHP/Moodle разработка

### 11. "Следующий урок" prominently — НУЖЕН ПЛАГИН
- Требует custom block или кастомизацию dashboard через PHP

### 12. Геймификация (XP, достижения) — БУДУЩЕЕ
- Moodle plugin: Local Gamification или Level Up!
- После базового редизайна

### 13. Разные интерфейсы по ролям — БУДУЩЕЕ
- Moodle поддерживает role-based dashboard
- Требует настройки custom home page per role

## Следующие шаги
1. Загрузить логотип на сервер /pix/school-logo.png (SSH недоступен, ждать)
2. Домен + SSL (Let's Encrypt)
3. BigBlueButton интеграция
4. Изучить плагин Level Up! для Moodle (геймификация)
5. Настроить role-based dashboard (разный вид для ученика/учителя/родителя)
