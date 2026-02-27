# Как запустить и протестировать текущий проект

Сейчас репозиторий — это **спецификация MVP** (документы + JSON-схемы), без готового мобильного/backend приложения.

## 1) Что уже можно «запускать»
- Проверку корректности JSON-схем;
- Проверку, что реальные примеры проходят валидацию по этим схемам;
- Ручную проверку UX-флоу по UX-карте.

## 2) Подготовка окружения
Требуется Python 3.10+.

```bash
python --version
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jsonschema
```

## 3) Быстрые проверки
### 3.1 Проверить, что схемы — валидный JSON
```bash
python -m json.tool docs/schemas/user_profile.schema.json > /dev/null
python -m json.tool docs/schemas/daily_plan.schema.json > /dev/null
python -m json.tool docs/schemas/daily_log.schema.json > /dev/null
python -m json.tool docs/schemas/evidence_source.schema.json > /dev/null
```

### 3.2 Проверить примеры против схем
```bash
python scripts/validate_schemas.py
```
Ожидаемый результат — 4 строки `[OK]`.

## 4) Как тестировать бизнес-логику (следующий шаг)
Когда появится backend, рекомендую сразу добавить:
- endpoint-тесты `/onboarding`, `/daily-plan`, `/daily-log`;
- контрактные тесты: ответ API валиден по JSON-схемам;
- smoke-тест цикла: onboarding -> план -> лог -> пересчет плана.

## 5) Как протестировать UX до кода
Используйте `docs/ux_map_ru.md` как чек-лист:
1. Пройти полный сценарий onboarding -> план -> лог.
2. Проверить edge-cases (пропуск дней, высокий стресс, высокий RPE).
3. Проверить, что на экране плана есть evidence-level и ссылка на источник.

## 6) Что делать, если хотите уже «живой» запуск
Следующий практический этап: собрать минимальный прототип (Flutter + FastAPI),
после чего можно запускать E2E сценарий локально.
