---
name: launch-review
description: >
  Killer skill — pre-launch product review для compliance check. Перед запуском
  consumer-facing продукта (app / SaaS / e-commerce / маркетплейс) — comprehensive
  review всех legal aspects: ЗЗПП, 152-ФЗ, 38-ФЗ реклама, sectoral, IP,
  возрастные restrictions.
argument-hint: "[product description / link]"
user_invocable: true
ported_from: product-legal/launch-review
ported_at: 2026-05-20
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /launch-review

## Назначение

Pre-launch comprehensive legal review consumer product. Output: go/no-go +
action items с deadlines.

## Pre-flight

- Product MVP готов и понятен
- Target launch date — known
- Sector + applicable regulators — clear (из PROFILE.md)

## Review categories

### A. ЗЗПП (если B2C)

```markdown
- [ ] Условия использования / public offer — оформлены corrrectly
- [ ] Цена окончательная и прозрачная (ЗЗПП ст.10)
- [ ] Информация о продукте: характеристики / противопоказания / срок годности
      / производитель / гарантия (ст.10)
- [ ] Возврат товара / отказ от услуги (ст.18, ст.25, ст.32) — политика clear
- [ ] Кулинг период (для дистанционной продажи) — 7 дней (ст.26.1)
- [ ] Контакты для жалоб + Роспотребнадзор link
```

### B. 152-ФЗ ПДн

```markdown
- [ ] Уведомление РКН подано (или предусмотрено если новый оператор)
- [ ] Политика обработки ПДн опубликована на сайте — accessible
- [ ] Согласие на обработку — collected перед collection
- [ ] Cross-border transfer — отдельное согласие если applicable
- [ ] Локализация (ст.18 ч.5) — DB в РФ
- [ ] Cookie consent banner (если cookies collect)
- [ ] Возрастные restrictions (если < 18 — special protections)
```

### C. 38-ФЗ реклама

```markdown
- [ ] Реклама pattern compliance check (не misleading, нет absolute claims)
- [ ] Возрастные restrictions для рекламы (азарт / алкоголь / финансы)
- [ ] Discrimination в targeting (запрещено по ст.5 38-ФЗ)
- [ ] Маркировка рекламы (с сентября 2022 — токены ОРД)
- [ ] Спецтребования к рекламе:
  - Финансовая (банки / страховые / МФО) — особые правила
  - Медицина / БАДы — обязательные оговорки
  - Алкоголь / табак — практически запрещены multiple channels
  - Игры / гэмблинг — отдельные правила
```

### D. IP (свой product + чужие materials)

```markdown
- [ ] Свои ТЗ — зарегистрированы перед launch (см. `ip-law/rospatent-application`)
- [ ] Используемые third-party images / шрифты / музыка — licensed properly
- [ ] OSS компоненты — compliant с лицензиями (см. `ip-law/oss-review`)
- [ ] Trademark clearance в нашем classes МКТУ (см. `ip-law/clearance`)
```

### E. Sectoral overlay

В зависимости от sector — applicable regulators:

| Sector | Regulator | Key requirements |
|--------|-----------|------------------|
| Финансовые услуги | Банк России | Лицензия + raskрытие |
| Медицина / БАДы | Минздрав / Росздравнадзор | Регистрация + противопоказания |
| Образование | Минобрнауки / Рособрнадзор | Лицензия + аккредитация (если diploma) |
| Алкоголь / табак | Росалкогольрегулирование | Лицензия + возраст control |
| Игры / гэмблинг | ФНС / специальные органы | Лицензия + locations restrictions |
| IT (для гос.заказа) | Минцифры | Реестр российского ПО |

### F. Возрастные restrictions

```markdown
- Контент 18+ — interface должен иметь age gate
- Контент 16+ / 12+ — marking 16+ / 12+ visible
- Сбор ПДн с несовершеннолетних — согласие родителей (152-ФЗ ст.7 ч.1)
- Маркетплейсы для children — special protections (Закон "О защите детей от информации" 436-ФЗ)
```

### G. Платежи

```markdown
- [ ] Платёжная инфраструктура — pci-dss compliant
- [ ] Sanctions screening при cross-border платежах (compliance-aml integration)
- [ ] Прозрачность для потребителя (ЗЗПП ст.16.1 — full price visible)
- [ ] Подтверждение transaction (чек по ФЗ-54 «О ККТ»)
```

### H. Customer support + жалобы

```markdown
- [ ] Channels для жалоб visible
- [ ] Сроки ответа на жалобы compliant (ЗЗПП — 10 days для большинства)
- [ ] Роспотребнадзор jurisdiction explained
- [ ] Возможность судебного разбирательства per ст.17 ЗЗПП (по выбору потребителя)
```

## Workflow

### Шаг 1. Intake продукт

```markdown
- Название
- Тип (товар / услуга / digital)
- Sector
- Target launch
- Channels (web / mobile / маркетплейсы)
```

### Шаг 2. Run checklist по 8 categories

### Шаг 3. Severity per issue

| Severity | Action |
|----------|--------|
| 🔴 Show-stopper | Cannot launch без fix; STOP |
| 🟡 Material | Launch с workaround но fix в 30 дней |
| 🟢 Minor | Launch ОК, fix в roadmap |

### Шаг 4. Output report

```markdown
# Launch Review — [продукт]

## Bottom line

**Recommendation:** [GO / GO WITH CONDITIONS / DO NOT LAUNCH]
**Critical issues:** [N]
**Material issues:** [M]
**Minor issues:** [K]

## Show-stoppers (🔴)

[List с конкретными actions + owners + deadlines]

## Material (🟡)

[List]

## Minor (🟢)

[List]

## Required pre-launch actions

- [ ] Action 1 — owner, deadline
- [ ] ...

## Required compliance documents

- [ ] Terms of Service — drafted, approved
- [ ] Privacy Policy — drafted, published
- [ ] Return policy — drafted, published
- [ ] Cookie policy — implemented + banner
- [ ] (Sectoral) лицензии получены

## Outside-адв engagement

[Recommended если material complexity / sums высокие]
```

## Cross-references

- `data-protection/use-case-triage` — для AI-features в продукте
- `data-protection/dpa-review` — если processor relationship
- `ip-law/clearance` — для бренда / товарного знака
- `compliance-aml/sanctions-screening` — для cross-border payments
- `ai-governance/use-case-triage` — для AI components

## Attribution

Adapted from [`product-legal/launch-review`](https://github.com/anthropics/claude-for-legal/blob/main/product-legal/skills/launch-review/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:**
- US FTC / state AG framework → РФ ЗЗПП + 152-ФЗ + 38-ФЗ + Роспотребнадзор / sectoral
- Маркировка ОРД (с 2022) — РФ-specific
- ФЗ-54 ККТ — РФ-specific
- Реестр российского ПО Минцифры — РФ-specific

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md). Pre-launch reviews of material products — engage outside-адв ФПА для validation.
