---
name: cold-start-interview
description: >
  Запускает онбординг команды по защите ПДн и пишет practice profile в
  `~/.ru-legal/profiles/data-protection/PROFILE.md`. Используй при первом запуске,
  когда profile отсутствует или содержит placeholder'ы, или пользователь говорит
  "настрой плагин privacy", "первый запуск", "перенастрой data-protection profile".
argument-hint: "[--redo] [--check-integrations] [--quick]"
user_invocable: true
adaptation_category: B
inspired_by: privacy-legal/cold-start-interview
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (data-protection)

Запускает онбординг для команды по защите ПДн. Использует тот же pattern что
`contract-law/cold-start-interview` — Quick/Full path, pause/resume, verify facts —
но с **privacy-specific** вопросами.

## Quick vs Full

> **`data-protection` — для compliance с 152-ФЗ "О персональных данных" РФ.**
>
> **2 минуты (Quick):** DPO контакт, тип организации, основные системы обработки
> ПДн, локализация. Defaults для всего остального.
>
> **15 минут (Full):** + полная инвентаризация систем, sub-processors с ДОУ статусом,
> cross-border practices, DSAR процесс, шаблоны ответов, план реагирования на
> утечку, регуляторный footprint (отрасль = специфические нормы — банковская /
> медицинская тайна).

---

## Interview structure

### Part 0: Who's using

- Юрист / DPO (ст.22.1) / IT compliance / не-юрист?
- Контакт DPO?
- Уровень доступа к плагину?

### Part 1: Организация

- Название + ИНН + ОПФ
- **Зарегистрированы в реестре операторов РКН?** (по умолчанию — обязательно ст.22)
  - № в реестре?
  - Дата уведомления?

### Part 2: Системы обработки ПДн (критично!)

**Это самый важный раздел для DSAR ответов.**

Перечень систем где обрабатываются ПДн (по примеру):

- [ ] CRM (название, vendor) — какие категории ПДн, локализация
- [ ] HRM / 1С:ЗУП — для сотрудников
- [ ] Email системы (Microsoft 365 / Yandex 360 / другая)
- [ ] Helpdesk
- [ ] Аналитика (auto-flag Google Analytics!)
- [ ] Маркетинг / mailing (Mindbox / Sendsay / другая)
- [ ] Облачное хранилище (Yandex Cloud / VK Cloud / Selectel)
- [ ] Прочее

Для каждой:
- Категории ПДн (ФИО / email / биометрия / спец)
- Локализация серверов (РФ / зарубеж)
- Retention период

### Part 3: Категории субъектов

- [ ] Сотрудники
- [ ] Клиенты
- [ ] Контрагенты-физлица
- [ ] Кандидаты
- [ ] Посетители сайта
- [ ] Получатели рассылок
- [ ] Спец.категории (ст.10): здоровье / политика / биометрия

### Part 4: Локализация и cross-border

- Первичное хранение ПДн в РФ? (ст.18 ч.5)
- Cross-border передача? Куда?
- Уведомления РКН (двухэтапные с 03.2023)?

### Part 5: DSAR процесс

- Канал приёма запросов
- Адрес для запросов (email / почтовый)
- Метод идентификации субъекта
- Internal turnaround (DPO → IT → Legal → sign-off)
- Шаблоны ответов есть?

### Part 6: Регуляторный footprint

**Отрасль определяет sectoral overlays:**

- [ ] Банк / финорганизация — банковская тайна (395-1)
- [ ] Медицина — медицинская тайна (323-ФЗ)
- [ ] Связь — тайна связи (126-ФЗ)
- [ ] Образование — особенности
- [ ] Госорган
- [ ] Иное

### Part 7: План реагирования на утечку

- Есть план реагирования?
- Сроки уведомления РКН (рекомендация 24 ч с обнаружения, новая практика)?
- Шаблон уведомления?
- Кто принимает решения (DPO + GC + CEO)?

### Part 8: Политика обработки ПДн

- URL опубликованной политики
- Дата последней редакции
- Покрывает ли actual practice? (запустим `policy-monitor` после setup)

---

## Output

После interview — write PROFILE.md (используя шаблон из
[packs/data-protection/PROFILE.md](../../PROFILE.md)).

После записи — predложить:

> "Готово. Profile сохранён в `~/.ru-legal/profiles/data-protection/PROFILE.md`.
>
> Рекомендую сразу запустить:
> 1. `/data-protection:policy-monitor --sweep` — найти gap'ы между политикой и
>    practice
> 2. `/data-protection:reg-gap-analysis [новый ФЗ или приказ]` — если есть
>    pending regulatory изменения для compliance
>
> Re-run interview: `/data-protection:cold-start-interview --redo`"

---

## Attribution

Inspired by [`privacy-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/privacy-legal/skills/cold-start-interview/SKILL.md)
by Anthropic (Apache 2.0).

**Не straight port** — структура interview переделана под РФ:

- **РФ-specific questions:**
  - Регистрация в реестре операторов РКН (ст.22)
  - Sectoral overlays (банковская, медицинская, тайна связи)
  - Локализация (ст.18 ч.5)
  - Cross-border двухэтапное уведомление РКН
  - DPO по ст.22.1
  - Уровень защиты ПДн (ПП РФ 1119 — определяется через PIA)
- **Системы обработки ПДн** — критичный inventory для DSAR ответов
- **Google Analytics auto-flag** — РКН квалифицировал как нарушение локализации
- **РФ vendor стандарты:** Yandex Cloud, VK Cloud, Selectel
- **Path:** → `~/.ru-legal/profiles/data-protection/PROFILE.md`

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-18.

---

## Disclaimer

Этот skill настраивает profile DPO команды. Не legal advice. Profile — **живой
документ**, ре-run раз в 6 месяцев или при существенных изменениях.

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
