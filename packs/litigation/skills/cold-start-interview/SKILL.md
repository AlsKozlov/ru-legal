---
name: cold-start-interview
description: >
  Запускает онбординг litigation команды и пишет practice profile в
  `~/.ru-legal/profiles/litigation/PROFILE.md`. Используй при первом использовании
  litigation pack'а, или говорит "настрой плагин litigation", "первый запуск",
  "перенастрой litigation profile".
argument-hint: "[--redo] [--check-integrations] [--quick]"
user_invocable: true
adaptation_category: B
inspired_by: litigation-legal/cold-start-interview
---

# /cold-start-interview (litigation)

Тот же pattern что `contract-law/cold-start-interview` (Quick/Full path, pause/resume,
verify legal facts) — с **litigation-specific** вопросами.

## Quick (2 минуты)

- Роль (адвокат ФПА / in-house / paralegal)
- Тип практики (in-house / юр.фирма / адвокатский кабинет)
- Юрисдикции (АС / СОЮ / МКАС)
- Default posture (plaintiff / defense / varies)
- Связь с MCP серверами

## Full (15 минут)

### Part 1: Команда

- Размер litigation команды
- Lead litigator
- Адвокатская тайна applies? (только для ФПА адвокатов)
- Распределение работы (in-house alone / outside counsel heavy)

### Part 2: Юрисдикция

- Основные арбитражные суды (округи)
- СОЮ (регионы)
- МКАС / SIAC / HKIAC — для международных
- Третейские суды
- Регулятор-форумы (досудебка с ФАС / РКН / ЦБ)

### Part 3: Risk calibration

- Materiality thresholds (в рублях)
- Severity bands (что high / medium / low)
- Likelihood bands
- Settlement ladder (когда мы готовы settling)

### Part 4: Outside counsel bench

- Список preferred OC
- Биллинг preferences (почасовой / fixed / contingency)
- Когда привлекаем (порог)

### Part 5: Conflicts process

Метод conflicts check:
- `outside-counsel` — внешняя фирма проверяет
- `system-check` — внутренняя CRM / DMS
- `informal` — counsel's judgment
- `corporate-legal` — отдельная функция

### Part 6: Эскалация

Матрица — кто принимает settlement decisions на каких суммах, когда attended Board.

### Part 7: Matter storage

Где хранятся matter docs (SharePoint / Drive / DMS). Структура папок.

### Part 8: Регуляторный footprint

Какие отрасли регулирования active:
- ФАС (если антимонопольный risk)
- РКН (если 152-ФЗ active matters)
- ЦБ (если финорганизация)
- ФНС (если налоговые споры)

### Part 9: Tracker integrations

- КАД (kad.arbitr.ru) — есть ли мониторинг новых дел против компании?
- Внутренний tracker (Jira / Linear / Excel) для дел?

---

## Attribution

Inspired by `litigation-legal/cold-start-interview` by Anthropic (Apache 2.0).

**РФ-specific adaptations:**
- Юрисдикции — АС / СОЮ / МКАС / третейский
- Адвокатская тайна (ФЗ-63) — applies vs not
- Регуляторный footprint — ФАС / РКН / ЦБ / ФНС
- КАД integration

**Path:** → `~/.ru-legal/profiles/litigation/PROFILE.md`

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## ⚠ Юридический disclaimer

Данный skill — **техническая платформа**, не оказывает юридических услуг по ст.2
ФЗ-63 «Об адвокатской деятельности». Outputs **не заменяют** консультацию
лицензированного юриста / адвоката ФПА.

AI может галлюцинировать, выдавать устаревшие нормы, неверно интерпретировать
факты. Material decisions (увольнение, M&A, налоговый спор, IP litigation) —
**обязательно** engage outside-адв ФПА с релевантной специализацией.

Проект `ru-legal` и его contributors не несут ответственности за решения,
принятые на основе outputs системы. Использование — на свой риск.
