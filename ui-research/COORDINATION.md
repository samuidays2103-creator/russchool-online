# Координация агентов — UI Research & Implementation
## Статус
- [x] RESEARCH: Исследование конкурентов завершено (март 2026)
- [x] RESEARCH: Анализ и критика готовы (март 2026)
- [x] RESEARCH: UI-концепция описана (март 2026)
- [x] AGENT2: site/ редизайн завершён (Agent 2 пишет сюда)
- [x] IMPL: Тема/дизайн реализован — сигнал для Agent 3
- [x] AGENT3: Moodle CSS применён — UI Redesign v2 задеплоен (2026-03-24)
- [x] PLUGIN: block_nextlesson установлен (2026-03-24)
- [x] PLUGIN: Role-based dashboards настроены (2026-03-24)

## ⚠️ РАЗДЕЛЕНИЕ РАБОТЫ — НЕ ДУБЛИРОВАТЬ

| Агент | Зона ответственности | НЕ трогает |
|-------|---------------------|-----------|
| **Agent 2** | `site/` — статичный маркетинговый сайт | Moodle (130.12.47.10) |
| **Agent 3** | `apply_theme_v2.py` — CSS для Moodle LMS | `site/` папку |

Agent 2 → пишет ТОЛЬКО в `site/css/`, `site/*.html`, `04-implementation-log.md`
Agent 3 → пишет ТОЛЬКО в `apply_theme_v2.py`, `screenshots/`, `05-moodle-implementation-plan.md`
Оба читают `01-03` — это ОК, читать можно вместе.

## 🔑 SSH ДОСТУП К СЕРВЕРУ (для всех агентов)

**Через Python Paramiko** (sshpass недоступен на Windows):
```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('130.12.47.10', username='root', password='hjc9Nvf8')
stdin, stdout, stderr = ssh.exec_command('команда здесь')
print(stdout.read().decode())
ssh.close()
# SFTP для файлов:
sftp = ssh.open_sftp()
sftp.put('local.php', '/var/www/moodle/local.php')
sftp.close()
```
- IP: 130.12.47.10 | User: root | Password: hjc9Nvf8
- Moodle: /var/www/moodle | dataroot: /var/moodledata
- Moodle admin UI: http://130.12.47.10 — admin / Admin2026!
- Тест-студент: ivanov_misha / Test1234!

## 🚫 site/ — ЗАМОРОЖЕН, НЕ ТРОГАТЬ (Agent 3 и любые другие агенты)
`site/` — отдельный git-репозиторий, запушен на GitHub Pages:
https://samuidays2103-creator.github.io/russchool-online/index.html
Коммит: be161a3 "UI Redesign v3" — финальная версия.
**Любые изменения в site/ только вручную через координатора.**
Agent 3 работает ТОЛЬКО с Moodle (http://130.12.47.10) через Playwright/Python.

## Что исследовать
Лидеры российского онлайн-образования:
- skysmart.ru
- foxford.ru
- uchi.ru
- yandex.ru/tutor (Яндекс.Репетитор)
- sberclass.ru
- yaklass.ru
- dnevnik.ru
- education.yandex.ru (Яндекс.Учебник)

## Что реализовать
База: `/c/Users/aid/Documents/online-school/site/`
Файлы: index.html, courses.html, teachers.html, prices.html, schedule.html, about.html, contacts.html
CSS: site/css/
JS: site/js/

## Аудитория школы
- 80% Россия (включая зоны СВО с закрытыми школами)
- 20% диаспора (ЮВА, ОАЭ, Германия)
- Дети 6–16 лет, предметы: русский язык + математика
- Живые уроки малыми группами (3–5 детей)
- Платформа: Moodle 4.5 + BigBlueButton
- Хостинг: Selectel (Россия)

## Файлы результатов
- `01-competitor-analysis.md` — разбор каждого конкурента
- `02-patterns-critique.md` — паттерны UI, критика, что работает/нет
- `03-ui-concept.md` — готовая концепция для нашей школы
- `04-implementation-log.md` — лог реализации (пишет агент-разработчик)

---

## ВАЖНО: Архитектура проекта (для Агента 2)

**Здесь ДВЕ разные системы:**

### 1. Маркетинговый сайт — `site/` (твоя работа, Агент 2)
Статичный HTML/CSS сайт — лендинг для привлечения учеников.
Файлы: index.html, courses.html, teachers.html, prices.html, schedule.html, about.html, contacts.html
**Цветовая схема ДОЛЖНА совпасть с брендом:** primary = #1e3a5f (тёмно-синий), accent = #E87722 (оранжевый)
Текущая синяя (#1e40af) и фиолетовая (#7c3aed) гамма — НЕ НАШИ ЦВЕТА, заменить.

### 2. Moodle LMS — http://130.12.47.10 (работа Агента 3)
Живая платформа на Moodle 4.5, где учатся дети.
Агент 3 читает твою концепцию из 03-ui-concept.md и применяет CSS к Moodle через Playwright.
**Агент 3 ждёт сигнала:** `[x] IMPL: Тема/дизайн реализован` в этом файле.

### Координация
- Когда Агент 2 ставит `[x] IMPL: Тема/дизайн реализован` — Агент 3 видит это и запускает применение к Moodle
- Используйте ОДНУ цветовую палитру: #1e3a5f + #E87722 + белый
- Шрифт Inter (уже используется в site/) — хорошо подходит и для Moodle

## 🔬 Критические находки из исследования экранов (06-screens-research.md)

**BBB точный CSS-селектор кнопки Join:**
```css
.mod_bigbluebuttonbn #join_button_input {
    background: linear-gradient(135deg, #E87722, #c45e10) !important;
    font-size: 1.2rem !important;
    padding: 14px 36px !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(232,119,34,0.4) !important;
    width: 100% !important;
}
```

**Лучший паттерн для Moodle BBB** = Foxford-стиль:
BBB-активность вверху секции курса (промоутировать через CSS order:-1),
материалы урока под ней. НЕ нужен iframe — открывается отдельной вкладкой.

**Dashboard ученика — правильный порядок блоков:**
1. Приветствие + ближайший урок (кастомный виджет)
2. Timeline (.block_timeline) — дедлайны
3. Мои курсы (.block_myoverview) — карточки с прогрессом

**Прогресс на карточке курса (нужен Activity Completion включённым):**
```css
.completion-progressbar .bar { background-color: #E87722 !important; }
```

**Плагины для установки через SSH (приоритет):**
1. block_progress — прогресс-бары по курсам
2. block_grade_me — блок непроверенных работ для учителя

**apply_theme_v3.py должен добавить эти CSS в дополнение к v2.**

## ✅ BBB уже настроен в курсе 2

- Активность существует: `/mod/bigbluebuttonbn/view.php?id=84`
- Название: "Урок онлайн" / "Видеоконференция BigBlueButton"
- cmid = 84 (предположительно, проверь через DB)
- НЕ нужно создавать новую активность для курса 2 — она есть
- Проверь курс 3 (MAT-1) отдельно
