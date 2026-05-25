---
name: terms-review
description: >
  RU-unique. Review Условий использования (Terms of Service) / EULA / Public
  Offer для consumer products. РФ specifics: публичная оферта (ст.437 ГК),
  consumer-friendly clauses (ЗЗПП ст.16 — недействительность ущемляющих),
  152-ФЗ ПДн, ст.426 публичный договор обязательные условия.
argument-hint: "[path к draft Terms]"
user_invocable: true
ported_at: 2026-05-20
adaptation_category: D
---

# /terms-review

## Назначение

Review TOS перед публикацией. Flag ущемляющие условия (могут быть признаны недействительными), missing required disclosures, и compliance gaps.

## Workflow

### Шаг 1. Identify тип

| Тип | Структура | РФ regulator |
|-----|-----------|--------------|
| Публичная оферта (ст.437 ГК) | Условия доступа к товару / услуге для любого потребителя | ЗЗПП |
| EULA (лицензия на ПО) | Для пользователя SaaS / app | ст.1235-1241 ГК |
| Public договор (ст.426) | Услуги для каждого обратившегося — почта, телеком, банки | ЗЗПП + sectoral |
| Договор присоединения (ст.428) | Standard terms без negotiation | ЗЗПП |

### Шаг 2. Mandatory elements (ст.10 ЗЗПП — для B2C)

- [ ] **Информация о продавце:** наименование + ОГРН/ИНН + адрес
- [ ] **Цена** (с НДС если применимо) — final, без скрытых fees
- [ ] **Существенные условия** (описание / характеристики)
- [ ] **Срок исполнения / поставки** (или способ определения)
- [ ] **Гарантия** (если применима)
- [ ] **Условия оплаты**
- [ ] **Контактная информация** (для жалоб)

### Шаг 3. Red-flag clauses (ст.16 ЗЗПП — недействительные)

🔴 **Эти clauses автоматически недействительны:**

| Clause | Why bad |
|--------|---------|
| "Споры только в суде по месту нахождения продавца" | ст.17 ЗЗПП — потребитель выбирает |
| "Возврат денег только bonus-ами / промокодами" | ст.18 ЗЗПП — возврат деньгами |
| "Отказ от ответственности за качество" | ст.18 — недействимо |
| "Запрет копии договора потребителю" | ст.4 ГК |
| "Изменение условий в одностороннем порядке" | ст.310 ГК — только по соглашению |
| "Невозможность возврата товара" | ст.18, 25 ЗЗПП |
| "Возрастные ограничения 0+ для контента 18+" | 436-ФЗ defence детей |
| "Согласие на любую обработку ПДн" (broad consent) | 152-ФЗ ст.9 — конкретность |

→ Все эти clauses — потребитель может requesting refund + suit за неустойку.

### Шаг 4. Missing required (по типу продукта)

#### Для SaaS / digital

- Cooling-off период (ст.26.1 ЗЗПП) — 7 дней для дистанционной продажи
- Лицензионные условия (если есть proprietary IP — ст.1235)
- SLA / availability
- Data export / portability
- Termination procedures

#### Для маркетплейса

- Roles: оператор vs продавцы
- Возврат: кто несёт ответственность
- Disputes resolution
- Возврат через маркетплейс (с retroactive обращения к продавцу)

#### Для финансовых

- Лицензия Банка России (если applicable)
- Кредитный риск disclaimer
- Cooling-off (для кредита — ст.5 ФЗ-353, для страхования — 14 дней)
- Полная стоимость кредита (ст.6 ФЗ-353)

### Шаг 5. Output report

```markdown
# Terms Review — [продукт]

## Bottom line

[Sign / Sign with changes / Don't publish]

## Mandatory elements check

[Per Step 2 — какие missing]

## Red-flag clauses identified

[Per Step 3 — что нужно убрать или будут признаны недействительными]

## Missing per product type

[Per Step 4]

## Recommendations

1. Critical fixes (must do)
2. Strongly recommended
3. Nice to have

## Legal references

- ЗЗПП ст.10, 16, 17, 18, 25, 26.1
- ГК ст.426, 428, 437, 1235
- 152-ФЗ ст.9
- 436-ФЗ (защита детей)
- Sectoral
```

## Что НЕ делает

- Не drafts terms from scratch (это outside-адв)
- Не handles ЭДО / accept mechanism — это product team
- Не replaces qualified legal review для material products

## ⚠ Юридический disclaimer

См. [DISCLAIMER.md](../../../../DISCLAIMER.md). Public-facing terms — engage outside-адв ФПА для finalize.
