---
name: fto-triage
description: >
  Freedom to Operate (FTO) analysis — проверка не нарушаем ли мы существующих
  патентов / товарных знаков, когда launching новый продукт. РФ specifics:
  патенты на изобретение — 20 лет с подачи; полезная модель — 10 лет; промобразец
  — 25 лет (5 + 4×5 продления). Search через ФИПС + WIPO PatentScope + EPO
  Espacenet. Опасные зоны post-2022 — параллельный импорт меняет landscape.
argument-hint: "[описание продукта или технологии]"
user_invocable: true
ported_from: ip-legal/fto-triage
ported_at: 2026-05-19
adaptation_category: C
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /fto-triage

## Назначение

Pre-launch FTO analysis — мы не нарушаем ли существующих IP rights в РФ при
выходе на рынок с новым продуктом?

Differs from `/clearance` (которое проверяет можем ли регистрировать) — FTO
проверяет **можем ли производить / продавать** (т.е. свободно operate).

## Pre-flight

- **Описание продукта / технологии** конкретное
- **Целевой рынок** (РФ только / EAEU / cross-border)
- **Дата запуска** запланирована
- **Бюджет на FTO** (полный FTO — дорогая процедура; triage — quick screen)

## Workflow

### Шаг 1. Decompose продукт на технические features

```markdown
## Product: [описание]

### Технические features

- Feature 1: [описание]
- Feature 2: [описание]
- ...
- Feature N: [описание]

### Каждая feature потенциально может infringe patent если:
- Patent claim covers эту feature
- Patent активен (не expired)
- Patent действителен в РФ

### Особо опасные зоны

- Core competing technology (если known конкуренты с patents)
- Базовые platform technologies (e.g., chemistry, biotech, electronics)
- Software algorithms (РФ — patentовать ПО как изобретение ограничено, но компонентные технологии можно)
```

### Шаг 2. Search patents

#### Sources

- **ФИПС база поиска** (bd.fips.ru) — РФ patents
- **EPO Espacenet** (worldwide.espacenet.com) — global
- **WIPO PatentScope** (patentscope.wipo.int) — international PCT
- **Google Patents** — broad search
- **USPTO** — US patents (если интересно для context)
- **EAPO** — Евразийские patents (action в РФ)

#### Strategy

1. Keyword search по technical terms
2. CPC / IPC classification search
3. Citation chains (cited / citing)
4. Competitor name search
5. Inventor name search (если known)

### Шаг 3. Identify relevant patents

```markdown
## Relevant patents identified

### Patent 1: RU N-NNNNNN
- **Правообладатель:** [...]
- **Дата подачи:** [DD.MM.YYYY]
- **Дата окончания:** [DD.MM.YYYY] (20 лет с подачи для изобретений, поддерживается пошлинами)
- **Status:** [действующий / истёкший / прекращён за неуплату]
- **Title:** [...]
- **Independent claims (ключевые):** [list, abstract analysis]
- **Релевантные claims:**
  - Claim 1 — [coverage]
  - Claim 5 — [coverage]
- **Pre-grant continuation pending:** [Y/N]

### Patent 2: [...]

[То же]

### Patent 3: [...]

[То же]
```

### Шаг 4. Claim chart analysis

Для каждого relevant patent — analysis на element-by-element basis:

```markdown
## Claim chart — Patent RU N-NNNNNN, Claim 1

| Element of claim | Наш продукт contains? | Detail |
|------------------|----------------------|--------|
| (a) X with Y | Yes | наш product has X with Y |
| (b) connected to Z | Yes | наш product Z connected |
| (c) configured to do W | **No** | у нас другой принцип |
| (d) | Yes | ... |

### Анализ

- **Все elements present** → likely infringement
- **Some elements missing** → no literal infringement; possibly doctrine of equivalents
- **Material differences** → likely no infringement

### Conclusion

[Infringe / Do not infringe / Unclear]
```

### Шаг 5. Validity / enforceability analysis

Patent может быть **недействительным** даже если зарегистрирован:

- Новизна issues — известно ли it до приоритетной даты?
- Изобретательский уровень — очевидно ли для специалиста?
- Расширенная защита claim's — может быть narrowed
- Pre-grant continuation issues
- Pay-of-maintenance fees (РФ — ежегодные пошлины)

Если patent validity questionable → может быть challenged через **opposition / cancellation в Палате по патентным спорам Роспатента + СИП**.

### Шаг 6. Risk assessment

```markdown
## FTO Risk Assessment

### Patent-by-patent

| Patent | Infringement risk | Validity concerns | Combined risk |
|--------|-------------------|---------------------|---------------|
| RU 1 | High (all elements) | Low (strong validity) | 🔴 critical |
| RU 2 | Medium (some elements + DoE) | Medium | 🟡 |
| RU 3 | Low (missing elements) | High (validity questionable) | 🟢 |
| EAEU | Medium | Low | 🟡 |

### Overall

- **Patents с serious infringement risk:** [N]
- **Mitigation options:**
  - Design-around (modify product to avoid claims)
  - License negotiation
  - Challenge validity (opposition / cancellation)
  - Settlement
  - Wait until expiration (если близко)

### Recommended action

[STOP / PROCEED with risks / PROCEED with design-around / SEEK LICENSE]
```

### Шаг 7. Design-around analysis (если critical patents found)

```markdown
## Design-around possibilities

### Patent RU N-NNNNNN, Claim 1 — критичный

**Element (c): "configured to do W"**

**Possible workarounds:**

1. **Change W to alternative principle** — does it still satisfy our product requirements?
2. **Avoid configuration entirely** — use different architecture
3. **Use prior art known before patent's priority date** — может быть not patent-protected

**Cost / benefit:**

| Workaround | Engineering cost | Performance impact | Legal clarity |
|-----------|-------------------|---------------------|---------------|
| Option 1 | $50k | -10% throughput | clear |
| Option 2 | $200k | +5% efficiency | clearer (different category) |
| Option 3 | $20k | similar | unclear (depends on prior art validity) |

**Recommended:** [option + reasoning]
```

### Шаг 8. License analysis (если negotiating)

```markdown
## License negotiation considerations

- **Royalty market rates** for similar tech: [%]
- **One-time license fee vs ongoing royalty:** trade-offs
- **Field-of-use restrictions:** scope
- **Sublicensing rights:** desired?
- **Term:** desired
- **Termination upon CoC** of licensor: consideration
- **Exclusivity:** unlikely if patent is core
- **Cross-license potential:** если у нас есть relevant IP — barter
```

## Special considerations для РФ post-2022

### A. Параллельный импорт

С 2022 — РФ permitted параллельный импорт определённых categories товаров без consent правообладателя (ПП РФ 506/2022 + дополнения).

**Implications:**
- Если product попадает в parallel import allowed categories — может быть imported в РФ без infringement (для conventional infringement)
- Но patent infringement в производстве — separate question

### B. Действие зарубежных patents в РФ

US / EU patent действителен только в jurisdictions of issuance. EAEU patent действителен в РФ + Армении + Беларуси + Казахстане + Киргизии.

**Practical:**
- Если активны только зарубежные patents (без РФ или EAEU равалентов) — нет patent infringement в РФ
- Но возможна commercial exposure если планируем экспорт

### C. Sanctions implications

Некоторые правообладатели (US / EU) после 2022 — приостановили operations в РФ:
- Это **не** автоматически invalидирует их patents в РФ
- Patents остаются enforceable через суд (СИП)
- Иногда — правообладатели pasively не enforce
- Но риск enforcement остаётся

## Output

```markdown
# FTO Analysis — [продукт]

## Bottom line

[PROCEED / DESIGN-AROUND / LICENSE / DO NOT LAUNCH]

## Identified critical patents

[List + brief]

## Mitigation plan

[Concrete actions]

## Budget estimate

- Design-around (если applicable): [сумма]
- License negotiation: [сумма]
- Litigation risk reserve: [сумма]
- Outside-помощь патентного поверенного / адвокат СИП: [сумма]

## Timeline

- Pre-launch analysis: [period]
- Design-around / licensing: [period]
- Re-FTO after changes: [period]
- Launch readiness: [DD.MM.YYYY]
```

## Что НЕ делает

- Не делает full professional FTO — это специализированная услуга outside-патентного поверенного
- Не negotiates licenses — это business + outside-адв
- Не handles patent invalidation в Палате по патентным спорам / СИП

## Attribution

Adapted from [`ip-legal/fto-triage`](https://github.com/anthropics/claude-for-legal/blob/main/ip-legal/skills/fto-triage/SKILL.md) by Anthropic (Apache 2.0).

**Категория C (substantial rewrite):**
- US patent terms (20 from filing for utility) — applicable similar в РФ, but УС / промобразцы РФ-specific terms
- US prior art / 35 USC §102 / 103 → РФ ст.1350 ГК новизна + изобретательский уровень
- EAEU patent — РФ-specific framework (no US equivalent)
- Параллельный импорт post-2022 (ПП 506/2022) — РФ-unique landscape change
- Sanctions implications для patent enforcement — post-2022 РФ-specific risk

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
