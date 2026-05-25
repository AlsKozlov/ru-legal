---
name: clearance
description: >
  Pre-launch clearance ТЗ / товарного знака — поиск collisions в реестре
  Роспатент перед регистрацией. Для патентов — clearance через ФИПС /
  EPO / WIPO. Анализ confusing similarity, классов МКТУ (44 классов товаров
  + 11 услуг = 45 классов), вероятности отказа в регистрации.
argument-hint: "[проект ТЗ или название]"
user_invocable: true
ported_from: ip-legal/clearance
ported_at: 2026-05-19
adaptation_category: B
---

# /clearance

## Назначение

Pre-filing / pre-launch clearance — проверка collisions с existing IP в реестрах.
Output: probability отказа в регистрации + risk infringement + recommendations.

## Pre-flight

- **Объект:** название / логотип / комбинированный знак / patентная idea
- **Классы МКТУ** определены (для ТЗ)
- **Регионы интереса** определены

## Workflow

### Шаг 1. Identify object

#### ТЗ

```markdown
## Проект ТЗ

- **Тип:** [словесный / изобразительный / комбинированный / объёмный / звуковой / иной]
- **Содержание:** [текст / описание изображения]
- **Классы МКТУ:** [список — по Ниццкой классификации, 45 классов]
- **Конкретные товары / услуги:** [перечень]
- **География защиты:** [РФ / EAEU / Мадрид / иное]
```

#### Патент

```markdown
## Проект патента

- **Тип:** [изобретение / полезная модель / промобразец]
- **Объект:** [техническое решение / устройство / способ / вещество]
- **МПК / СПК код:** [классификация]
- **Ключевые признаки:** [...]
```

### Шаг 2. Search в реестрах

#### Для ТЗ

**Основные источники:**

- **Реестр Роспатент** — fips.ru (open access)
- **Мадридская система** — WIPO Global Brand Database (madrid.wipo.int)
- **EAEU единый ТЗ** — реестр EAPO (eapatis.com)

**Search strategies:**

1. **Точное совпадение** — буквенный match
2. **Транслитерация** — RU ↔ LAT (если знак латиницей, искать кириллицу также)
3. **Фонетическое сходство** — "kola" vs "cola" vs "kolla"
4. **Семантическое сходство** — "звезда" vs "star" vs "stella"
5. **Визуальное сходство** (для логотипов) — image search через ФИПС
6. **По классам МКТУ + смежные** — для определения collision risk

#### Для патентов

- **Реестр Роспатент** — fips.ru
- **ФИПС база поиска** — bd.fips.ru
- **EPO Espacenet** — global patent search
- **WIPO PatentScope** — international search

### Шаг 3. Analyze collisions

#### Для ТЗ — критерии отказа (ст.1483 ГК)

ТЗ **не регистрируется**, если:

**Абсолютные основания (ст.1483 ч.1-3):**
- Описательный характер (только для конкретных товаров)
- Введение в заблуждение
- Совпадение с государственными символами / гербами
- Противоречие public order / morality
- Состоит только из цвета / простого имени фамилии
- Без различительной способности

**Относительные основания (ст.1483 ч.6):**
- **Сходство до степени смешения** с ранее зарегистрированным ТЗ для однородных товаров
- Совпадение с фирменным наименованием другой компании
- Совпадение с коммерческим обозначением
- Объект авторского права другого лица
- Промышленный образец другого лица

#### Confusing similarity test

Учитываются:
- **Визуальное** сходство (буквы, шрифт, изображение)
- **Фонетическое** (произношение)
- **Семантическое** (значение / ассоциации)
- **Концептуальное** сходство overall

#### Однородность товаров

Один класс — однородные by default.
Разные классы — могут быть однородными по существу (например, "одежда" 25 кл и "обувь" 25 кл — да; "одежда" 25 кл и "косметика" 3 кл — нет).

### Шаг 4. Risk assessment

```markdown
## Clearance Report — [объект]

### Collisions found

| # | Conflicting mark | № регистрации | Правообладатель | Классы | Similarity | Однородность товаров | Risk |
|---|------------------|---------------|-----------------|--------|------------|----------------------|------|
| 1 | "АЛЬФА" | 555555 | ООО "Альфа" | 35 | 95% (visual + phonetic) | Да | 🔴 critical |
| 2 | "АLFА" (Мадрид) | IR 666666 | Foreign Inc. | 35, 42 | 85% (phonetic) | Частично | 🟡 medium |
| 3 | "АЛЬФАН" | 777777 | ИП Сидоров | 25 | 60% | Нет | 🟢 minor |

### Probability отказа в регистрации

- **Точно откажут** (если есть 🔴 collision): high
- **Возможно** (🟡 collisions): med
- **Скорее всего пройдёт** (только 🟢): low

### Recommendations

1. **Изменить** название чтобы уменьшить сходство — [предложения]
2. **Согласовать** с правообладателем conflicting mark — получить согласие (ст.1483 ч.7) — может оплатить за это
3. **Сузить** классы МКТУ — exclude problematic classes
4. **Отказаться** от регистрации — заняться другим брендом
5. **Подать с рисками** — иногда экспертиза не находит коллизий
```

### Шаг 5. Decision matrix

| Risk | Action |
|------|--------|
| 🔴 critical collision (high similarity + same classes) | Change или get consent от правообладателя |
| 🟡 medium (similar в смежных классах) | Limit classes, consider opposition / disclosure |
| 🟢 minor (low similarity или other classes) | Proceed с filing |

### Шаг 6. Для патентов — clearance отличается

#### Critical вопросы

- **Новизна** (ст.1350) — известно ли это техническое решение?
- **Изобретательский уровень** (ст.1350) — не очевидно ли для специалиста?
- **Промышленная применимость** — может ли быть реализовано?

Patentовая clearance ≠ FTO (Freedom to Operate — см. `/fto-triage`).

Clearance проверяет **могут ли запатентовать** — а FTO проверяет **не нарушим ли существующих**.

### Шаг 7. Output

```markdown
# Clearance Report — [объект]

## Bottom line

- **Recommendation:** [PROCEED / PROCEED WITH FIXES / DO NOT PROCEED]
- **Probability registration success:** [%]
- **Identified critical risks:** [N]

## Detailed findings

[Полная таблица collisions]

## Action items

1. [Concrete action]
2. ...

## Outside-help recommended

[Yes/No — для material matters рекомендуется патентный поверенный с experience]

## Next steps

- [ ] Engage патентного поверенного для filing
- [ ] Подача заявки → `/rospatent-application`
- [ ] Мониторинг expiration ТЗ конкурентов (10 лет с возможностью продления)
```

## Что НЕ делает

- Не подаёт заявку в Роспатент (это `/rospatent-application` + патентный поверенный)
- Не делает полную FTO analysis (это `/fto-triage`)
- Не handles opposition / cancellation proceedings — это outside-адв ФПА + СИП

## Attribution

Adapted from [`ip-legal/clearance`](https://github.com/anthropics/claude-for-legal/blob/main/ip-legal/skills/clearance/SKILL.md) by Anthropic (Apache 2.0).

**Категория B:** US USPTO trademark/patent search → РФ Роспатент / ФИПС; ст.1483 ГК (отказ в регистрации) vs US Lanham Act 15 USC §1052; Мадридская система search via WIPO; EAEU единый ТЗ added; МКТУ (Ниццкая classification — universal but framing РФ); ст.1350 ГК для патентной clearance.

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
