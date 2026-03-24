# Инструкция для тестера: настрой CronCreate

## Шаг 1: Создай cron

Выполни эту команду (CronCreate tool):

```
cron: "*/4 * * * *"
recurring: true
prompt: |
  Прочитай файл C:/Users/aid/Documents/online-school/TEST_TRIGGER.md.
  Если первая строка содержит "ready":
  1. Запиши "status: running" в TEST_TRIGGER.md
  2. Запусти: cd C:/Users/aid/Documents/online-school && python tester.py
  3. Дождись завершения (timeout 10 минут)
  4. Проанализируй новые скриншоты в screenshots/ — сравни с EXPECTATIONS.md и DESIGN-SPEC.md
  5. Обнови bugs.md: поменяй fixed→verified-fixed если баг исправлен, добавь новые open
  6. Запиши "status: done" в TEST_TRIGGER.md
  Если первая строка НЕ содержит "ready" — скажи "Жду триггера." и всё.
```

## Шаг 2: Молчи

НЕ пиши пользователю. Просто работай в фоне. Крон сам сработает когда REPL idle.

## Протокол
- Разработчик ставит `ready` → твой cron подхватывает
- Ты запускаешь tester.py → анализируешь → обновляешь bugs.md → ставишь `done`
- Разработчик видит обновлённый bugs.md → чинит → ставит `ready`
- Повторяется автоматически
