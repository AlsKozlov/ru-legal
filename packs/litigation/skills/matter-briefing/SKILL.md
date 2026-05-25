---
name: matter-briefing
description: >
  One-pager status brief по конкретному matter'у — posture, risk, recent changes,
  next deadline, exposure, open questions. Flag'ает stale если updates не было > 30
  дней. Используй когда пользователь говорит "brief по делу X", "what's status of
  matter Y", "обнови меня по делу Z", или perед meeting'ом с CEO / Board / outside
  counsel.
argument-hint: "<slug | название>"
user_invocable: true
ported_from: litigation-legal/matter-briefing
ported_at: 2026-05-18
adaptation_category: A
---

# /matter-briefing

## Назначение

Краткий status brief для stakeholder'а который хочет понять состояние дела за
2 минуты чтения.

## Workflow

### Шаг 1. Load matter

Read:
- `~/.ru-legal/profiles/litigation/matters/[slug]/matter.md`
- `~/.ru-legal/profiles/litigation/matters/[slug]/history.md`
- Row в `_log.yaml`

### Шаг 2. Check staleness

Если `last_updated_at > 30 дней назад` — флагнуть в brief'е:

> ⚠️ Stale (last update [N days ago]). Запусти `/litigation:matter-update` после
> чтения этого brief'а.

### Шаг 3. Output

```markdown
[МАРКИРОВКА из PROFILE.md]

# Matter Brief: [Matter name]

**Slug:** [slug]
**Дата brief'а:** [DD.MM.YYYY]
**Status:** Active / On hold / Closed
**Stale?** [No / ⚠️ Yes — last update DD.MM.YYYY]

---

## TL;DR

[Одно предложение — где мы и что важно знать.]

---

## Posture

- **Тип дела:** [contract / tax / corporate / etc.]
- **Наша роль:** [истец / ответчик / третье лицо]
- **Forum:** [АС / СОЮ / МКАС / др.]
- **Counterparty:** [имя]
- **Стратегия:** [defend / pursue / settle / wait]

## Risk

- **Severity / Likelihood / Risk rating:** [high/medium/low]
- **Экспозиция:** [сумма в руб]
- **Non-monetary risk:** [...]

## Recent changes (last 30 days)

[Top 3-5 событий из history.md за период]

## Next deadline

- **Дата:** [DD.MM.YYYY]
- **Что:** [Подача отзыва на иск / Cуд.заседание / etc.]
- **Owner:** [имя]
- **Days remaining:** [N]
- **Status:** [On track / At risk / Overdue]

## Открытые вопросы

[2-3 ключевых open вопроса, требующих attention]

## Ownership

- **Lead:** [имя]
- **Outside counsel:** [...]
- **Business owner:** [...]

---

## Что я рекомендую сейчас

[1-3 конкретных next steps с owner'ами]
```

### Шаг 4. Calibrate по audience

Спроси (если не очевидно из context'а): "Brief для кого — CEO / GC / Board /
outside counsel / лично себе?"

| Audience | Tone | Что особенно highlight |
|----------|------|------------------------|
| CEO | Краткий, focus на economic + reputational impact | Worst-case exposure |
| GC | Детальный, legal nuance | Правовая стратегия |
| Board | Очень краткий, focus на strategic implication | Material risk |
| Outside counsel | Operational, готов к работе | Open assignments |
| Лично себе | Honest, includes "что не работает" | Reality check |

---

## Attribution

Adapted from [`litigation-legal/matter-briefing`](https://github.com/anthropics/claude-for-legal/blob/main/litigation-legal/skills/matter-briefing/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения:** РФ юр.термины (forum, posture types), audience calibration сохранена,
matter folder path обновлён.

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

---

## Disclaimer

Brief — utility. Не legal advice. Strategy decisions за lead attorney + stakeholders.

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
