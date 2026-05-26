---
name: customize
description: >
  Guided customization вашего practice profile для договорной работы — изменить одну
  вещь без re-run полного cold-start interview. Adjust risk posture, escalation
  contacts, playbook positions, NDA triage preferences, house style, review
  preferences. Используй когда пользователь говорит "измени мой [thing]", "обнови
  profile", "edit my playbook", "tune config", или "customize".
argument-hint: "[название секции, или опиши что хочешь изменить]"
user_invocable: true
ported_from: commercial-legal/customize
ported_at: 2026-05-17
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /customize

## Когда запускается

Пользователь набрал `/contract-law:customize`. Хочет изменить что-то в practice
profile — risk posture, escalation contact, playbook position, jurisdiction, output
format — **без** re-run полного cold-start interview и **без** ручного редактирования
YAML.

## Что делать

### Шаг 1. Прочитай config

Прочитай `~/.ru-legal/profiles/contract-law/PROFILE.md`. Если файл не существует —
скажи:

> "Profile ещё не создан. Запусти `/contract-law:cold-start-interview` сначала
> — он соберёт базовую конфигурацию, а потом можно tune через customize."

### Шаг 2. Определи целевую секцию

Если пользователь указал секцию явно (например `customize escalation` или
`customize playbook sell-side`) — иди к ней напрямую.

Если описание свободное (например "хочу другую матрицу эскалации" или "слишком строго
по NDA") — match по таблице:

| Что хочет изменить | Секция в PROFILE.md |
|--------------------|---------------------|
| "risk posture", "риск-аппетит" | `## Кто мы → Risk posture` |
| "escalation", "матрица эскалации", "approvers" | `## Эскалация` |
| "playbook", "позиции", "default условия" | `## Playbook → Sales-side` или `Purchase-side` |
| "NDA triage", "GREEN/YELLOW/RED для NDA" | `## NDA triage positions` |
| "house style", "формат вывода", "куда сохранять" | `## Стиль работы → House style` |
| "review preferences", "confirm routing", "auto-confirm" | `## Review preferences` |
| "контакты", "ответственные", "responsible_legal" | `## Кто пользуется → Контакты` |
| "tracker", "renewal register" | (не в PROFILE.md — `renewal-register.yaml`) |

Если ambiguous — спроси:

> "Я могу изменить несколько вещей:
> 1. [option from таблицы]
> 2. [option]
> 3. [option]
>
> Что именно?"

### Шаг 3. Покажи текущее значение

Перед изменением — покажи **что сейчас**:

```
Текущее значение в `## Эскалация`:

| Кто согласовывает | Лимит | Эскалирует к | Через |
|-------------------|-------|--------------|-------|
| Менеджер | До 1 млн руб., стандартные условия | Юрист | Slack |
| Юрист | До 10 млн руб., в пределах fallbacks | Главный юрисконсульт | Email |
| Главный юрисконсульт | Всё прочее | Гендиректор | Встреча |

Что хочешь изменить?
```

### Шаг 4. Confirm change

После предложения изменения — **покажи diff** и спроси confirmation:

```
Я собираюсь применить:

**Было:**
| Менеджер | До 1 млн руб., стандартные условия | Юрист | Slack |

**Станет:**
| Менеджер | До 500 тыс. руб., стандартные условия | Юрист | Slack |

Применить? (да / нет / другое значение)
```

**Не применяй без явного "да"** или конкретного counter-предложения.

### Шаг 5. Apply и confirm

Запиши новое значение в PROFILE.md. Покажи confirmation:

```
✅ Готово.

Изменено: `## Эскалация` → лимит менеджера 1 млн руб. → 500 тыс. руб.

Изменение войдёт в силу при следующем запуске skills этого pack'а.
Профиль остаётся в `~/.ru-legal/profiles/contract-law/PROFILE.md`.
```

## Что можно изменить через customize

### Quick edits (одна строка)

- Контакты в эскалации (email, Slack)
- Лимиты сумм
- Default LoL цель
- Confirm_routing (true/false)
- Маркировка output (КОНФИДЕНЦИАЛЬНО / ДСП / другое)
- Сторона по default (sell-side / buy-side / both)

### Medium edits (секция)

- NDA triage positions (что GREEN, YELLOW, RED)
- Карты эскалации (полная таблица)
- Playbook sell-side / buy-side (LoL, indemnity, governing law, term)
- House style preferences

### Heavy edits (нужно cold-start)

Если пользователь хочет radical change (например смена индустрии, размера компании,
sell-side → buy-side) — **не пытайся** через customize. Скажи:

> "Это существенное изменение профиля. Лучше run `/contract-law:cold-start-interview
> --redo` — пройдёт быстрее (5-10 мин) и я обновлю всю конфигурацию consistently.
> Customize лучше для точечных правок."

## Что этот skill НЕ делает

- Не редактирует другие файлы кроме PROFILE.md (для `renewal-register.yaml` есть отдельный
  skill — `renewal-tracker --add`).
- Не запускает re-cold-start automatically.
- Не валидирует семантику (например пользователь может set lim 0 руб. — это его
  выбор; skill только применяет).
- Не сохраняет revision history (TODO: добавить в Phase 2).

---

## Examples

```
/contract-law:customize escalation
→ открывает секцию эскалации, спрашивает что менять
```

```
/contract-law:customize "хочу строже по NDA"
→ открывает NDA triage positions, спрашивает какой term tighten
```

```
/contract-law:customize playbook
→ спрашивает sell-side или buy-side, потом открывает соответствующую секцию
```

```
/contract-law:customize "получатели renewal алертов"
→ ищет в `## Стиль работы` секцию про alerts, предлагает изменить
```

---

## Специфика для РФ контекста

### Что часто нужно изменять РФ in-house юристам

По опыту работы с РФ командами, самые частые customize requests:

1. **Лимиты эскалации в рублях** — компании растут, пороги становятся outdated.
   Раз в полгода — пересмотр.

2. **Список auto-escalation triggers** — добавление новых жанров рисков (например,
   sanctions exposure после 2022, валютный контроль после изменений 173-ФЗ).

3. **Маркировка documents** — особенно когда компания инвестировала в режим
   коммерческой тайны (98-ФЗ ст.10) — нужно явно маркировать "Коммерческая тайна"
   в дополнение к "Конфиденциально".

4. **Жёсткость по applicable law не-РФ** — компании постепенно становятся conservative
   из-за ограничений признания иностранных судебных решений.

5. **NDA term** — РФ юристы постепенно укорачивают до 3 лет (от 5+) для большинства
   контекстов.

---

## Attribution

Adapted from [`commercial-legal/customize`](https://github.com/anthropics/claude-for-legal/blob/main/commercial-legal/skills/customize/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала:**
- Profile path: → `~/.ru-legal/profiles/contract-law/PROFILE.md`
- Таблица секций mapping адаптирована под РФ structure PROFILE.md
- Сумма thresholds в рублях
- Добавлена секция "Что часто нужно изменять РФ in-house юристам"
- Примеры на русском с realistic РФ scenarios (sanctions, валютный контроль,
  режим коммерческой тайны)

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-17.

---

## Disclaimer

Customize — это утилитный skill. Не legal advice. Изменения PROFILE.md влияют на
поведение всех downstream skills — рекомендуется review с lead attorney перед
существенными изменениями (особенно playbook positions и escalation matrix).

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
