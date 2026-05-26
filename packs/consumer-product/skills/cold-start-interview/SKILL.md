---
name: cold-start-interview
description: >
  First-run для consumer-product pack. Заполняет PROFILE.md: тип бизнеса,
  product характеристики, regulatory context (ЗЗПП / 152-ФЗ / 38-ФЗ /
  sectoral), маркетинговые channels.
argument-hint: "[optional: section]"
user_invocable: true
ported_from: product-legal/cold-start-interview
ported_at: 2026-05-20
adaptation_category: B
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /cold-start-interview (consumer-product)

## Workflow

### Шаг 1. Тип бизнеса + sector

- E-commerce / SaaS / mobile app / маркетплейс / физ.магазин
- B2C / B2B
- Sector — определяет sectoral regulators

### Шаг 2. Product characteristics

- Товар / услуга / digital good
- Целевая аудитория (возраст, география)
- Цена range

### Шаг 3. Regulatory context

- ЗЗПП applicable (B2C → yes)
- 152-ФЗ (обработка ПДн потребителей)
- 38-ФЗ (если делаем рекламу)
- Sectoral overlay (финансы / медицина / education / алкоголь / иное)

### Шаг 4. Маркетинговые channels

- Web / mobile / маркетплейсы / соц.сети

### Шаг 5. Compliance документы

- Terms of Service
- Privacy Policy
- Политика возврата
- Cookie Policy
- Возрастные ограничения

### Шаг 6. Outside counsel + risk posture

## Attribution

Adapted from [`product-legal/cold-start-interview`](https://github.com/anthropics/claude-for-legal/blob/main/product-legal/skills/cold-start-interview/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:** US FTC framework → РФ ЗЗПП + 152-ФЗ + 38-ФЗ + sectoral.

**Original copyright:** © 2026 Anthropic PBC, Apache 2.0.

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md).
