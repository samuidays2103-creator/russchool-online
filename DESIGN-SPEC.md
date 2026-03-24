# Дизайн-спецификация: Онлайн-школа на Moodle 4.5

## Цвета
- Primary: `#1e3a5f` (тёмно-синий)
- Accent: `#E87722` (оранжевый)
- Background: `#FAFAF9` (тёплый серый)
- Cards: `#FFFFFF`
- Border: `#E7E5E4`
- Text: `#1C1917`
- Text muted: `#57534E`

## Шрифты
- Body: Golos Text (Google Fonts)
- Headings: Nunito (Google Fonts)
- Size: 15px body, 1.65 line-height

## Navbar
- Фон: #1e3a5f, border-bottom 3px #E87722
- Логотип: EasyDays через CSS ::before (белый invert)
- Ссылки: белые, hover оранжевый
- Toggle темы: СКРЫТ
- Min-height: 56px

## Dashboard (/my/)
- Порядок блоков: 1) Обзор курсов (myoverview) 2) Шкала времени 3) Календарь
- Left drawer: ЗАКРЫТ (drawer-open-index=0)
- max-width main-inner: 100%
- Right sidebar: события, недавние курсы, следующий урок, XP
- НЕ реализовано (JS виджеты отложены): приветственный header, sidebar расписания

## Карточки курсов
- border-radius: 16px
- box-shadow: 0 1px 3px rgba(0,0,0,0.05)
- hover: translateY(-4px), shadow усиливается, border #E87722
- Название: Nunito 700, #1e3a5f

## Страница курса (/course/view.php)
- BBB активность: gradient фон #1e3a5f → #2a5298, белый текст, иконка оранжевая
- Секции: белый фон, border-radius 8px, header #f0f4f8 с border-bottom #1e3a5f
- Activity items: hover подсветка #f0f4f8
- Teacher panel: НЕ реализован (JS баг)

## Страница входа (/login/)
- Gradient фон (оранжевый → тёмно-синий)
- Белая карточка по центру
- Заголовок "Войдите в личный кабинет"
- Кнопка "Вход" — оранжевая

## BBB страница ожидания
- Пока без стилизации (CSS селекторы не совпали)
- Цель: центрированная карточка с иконкой 🎥 и сообщением

## Frontpage (/)
- Hero: gradient #1e3a5f → #E87722
- Заголовок + кнопка "Войти в личный кабинет"
- Категории курсов: СКРЫТЫ для гостя

## Мобильная версия (375px)
- Карточки в 1 колонку
- Navbar компактный (hamburger menu)
- Футер "На платформе Moodle" — СКРЫТ

## Не реализовано (TODO)
- JS dashboard widgets (приветствие, sidebar)
- Teacher panel на странице курса
- Стилизация BBB waiting page (нужны точные DOM-селекторы)
- Role-based layout (разные dashboard для student/teacher/parent)
