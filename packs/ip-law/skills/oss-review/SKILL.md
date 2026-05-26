---
name: oss-review
description: >
  Review OSS (open-source) лицензий используемых в продукте. Universal +
  РФ specifics: ст.1286 ГК — лицензионный договор; OSS лицензии классифицируются
  по copyleft strength; potentially conflicting комбинации; РФ-specific
  considerations для IT-аккредитации (реестр Минцифры) — ограничения по OSS
  components.
argument-hint: "[путь к проекту или список зависимостей]"
user_invocable: true
ported_from: ip-legal/oss-review
ported_at: 2026-05-19
adaptation_category: A
last_legislative_update: "2026-05"  # auto-added 2026-05-26
---

# /oss-review

## Назначение

Review OSS licenses в продукте + identify compliance obligations + flag risks.

## OSS license categories

### A. Permissive (наименее ограничивающие)

| Лицензия | Key rules |
|----------|-----------|
| **MIT** | Сохранять copyright notice + permission notice |
| **BSD 2-Clause** | То же |
| **BSD 3-Clause** | + non-endorsement |
| **Apache 2.0** | + patent grant + NOTICE file + state changes |
| **ISC** | Минималистичный |
| **Unlicense / CC0** | Public domain dedication |

**Использование:** Свободно в proprietary продуктах. Минимальные obligations.

### B. Weak copyleft

| Лицензия | Key rules |
|----------|-----------|
| **LGPL 2.1 / 3.0** | Изменения в LGPL компонентах → LGPL. Linking с proprietary — OK, но user должен иметь возможность relink. |
| **MPL 2.0** (Mozilla) | Изменения в MPL files → MPL. Можно combine с proprietary в larger product. |
| **EPL 1.0/2.0** (Eclipse) | Похоже на MPL |
| **CDDL 1.0/1.1** | Похоже на MPL |

**Использование:** OK в proprietary при выполнении requirements.

### C. Strong copyleft

| Лицензия | Key rules |
|----------|-----------|
| **GPL 2.0 / 3.0** | Производные работы должны быть GPL. Distribution → must offer source. **Не** working в proprietary без significant restructuring. |
| **AGPL 3.0** | GPL + network use trigger. Если используешь как online service → source должен быть доступен users. |
| **EUPL** | EU equivalent of GPL |

**Использование:** Avoid в proprietary unless вы готовы opensource весь project.

### D. Non-standard / proprietary с open-source claims

- **Source-Available** licenses (BSL, SSPL, etc.) — НЕ true open-source; restrictions
- **Creative Commons** — generally not для software
- **Custom licenses** — review carefully

### E. Public domain / equivalent

- **CC0** — public domain
- **Unlicense** — public domain
- **WTFPL** — public domain effectively

## Workflow

### Шаг 1. Inventory dependencies

#### Для Python project

```bash
pip-licenses --format=markdown --order=license
```

#### Для Node.js project

```bash
npx license-checker --markdown
# or
npx license-report
```

#### Для Java / Maven

```bash
mvn license:add-third-party
```

#### Для Go

```bash
go-licenses report ./...
```

#### Для C/C++

Manually + проверка через FOSSology / Black Duck для commercial scans

### Шаг 2. Categorize each dependency

```markdown
## Dependencies analysis

| Package | License | Category | Direct / Transitive | Risk |
|---------|---------|----------|---------------------|------|
| numpy | BSD-3-Clause | Permissive | Direct | 🟢 |
| react | MIT | Permissive | Direct | 🟢 |
| openssl | Apache 2.0 / SSLeay | Permissive (dual) | Transitive | 🟢 |
| ffmpeg | LGPL 2.1+ / GPL 2.0+ | Weak / Strong copyleft | Direct | 🟡 (зависит — какие части) |
| readline | GPL 3.0 | Strong copyleft | Transitive | 🔴 if linked |
| custom-lib | Proprietary (с EULA) | Non-OSS | Direct | 🔵 separate review |
```

### Шаг 3. Identify obligations + risks

#### Per-license obligations (для distributed software)

```markdown
### MIT / BSD / Apache 2.0

- [ ] Сохранить copyright notices в исходниках
- [ ] Сохранить лицензионный текст в distribution
- [ ] Apache 2.0: создать NOTICE file со всеми attribution
- [ ] Apache 2.0: если модифицировали — пометить modifications
- [ ] BSD 3-Clause: не использовать имя оригинальных контрибьюторов для endorsement

### LGPL

- [ ] Linking dynamically (preferred) или предоставить object files для relink
- [ ] Сохранить лицензионный текст
- [ ] Если modified — пометить modifications + предоставить source

### GPL / AGPL

- [ ] **Полная производная работа** должна быть GPL / AGPL
- [ ] Distribution → offer source for 3 years
- [ ] AGPL — network use → source доступен users
- [ ] **Если не хотим opensource — refactor / replace GPL components**

### MPL

- [ ] Modified MPL files — оставить MPL
- [ ] Можно combine с proprietary в larger product (file-level boundary)
```

#### Compatibility check

Combining lic несовместимы → conflict:

| License A | License B | Compatible? |
|-----------|-----------|-------------|
| MIT | GPL 3.0 | Yes (one direction — MIT can be sublicensed under GPL) |
| Apache 2.0 | GPL 2.0 | **No** (patent retaliation in Apache 2.0 conflicts) |
| Apache 2.0 | GPL 3.0 | Yes |
| GPL 2.0 | GPL 3.0 | **No** (different versions) |
| LGPL 2.1 | GPL 3.0 | Compatible (LGPL re-licensable under GPL) |
| MPL 2.0 | GPL | Compatible (MPL allows GPL combination) |

→ Flag incompatibilities.

### Шаг 4. Risk assessment per use case

#### Use case A: Internal-only (corp internal tool)

- Generally low risk
- GPL OK (no distribution triggers GPL obligations)
- AGPL — caution, "use" может trigger даже internal

#### Use case B: SaaS / network service

- AGPL critical — source disclosure обязательно если modified
- GPL — generally OK (no "distribution" в SaaS sense)
- All others — sane requirements

#### Use case C: Distributed product (binaries / desktop / mobile)

- GPL → must be GPL fully OR refactor to not use
- LGPL → carefully linking
- All others — keep copyright notices

#### Use case D: Open-source distribution

- Все compatible licenses OK
- Document attribution

### Шаг 5. РФ-specific considerations

#### A. Реестр российского ПО (Минцифры)

Для IT-аккредитации (налоговая льгота 0% налог на прибыль до 2030; страх.взносы 7.6%):

- Программное обеспечение должно быть **российского происхождения**
- **OSS компоненты** допустимы, но:
  - Не могут составлять "основную функциональность" продукта
  - Должны быть documented + licensed правильно
  - Постановление Правительства РФ 1236/2017 + дополнения детализируют

**Practical:** в product description для Минцифры — explicitly disclose OSS components + наш value-added на их основе.

#### B. Импортозамещение

Для гос.заказчиков / гос.компаний — приоритет на отечественное ПО. Если product
heavily depends на foreign OSS — может быть disadvantage.

#### C. Sanctions effects на OSS

Post-2022:
- Некоторые US OSS communities ограничили contributions от РФ developers
- GitHub имеет limitations для accounts из санкционных regions
- Mirror на гитXфлекс / Гитуверс / нашисервере recommended для bus continuity
- Forks с РФ developers — потенциальный legal risk для US/EU users (но not affecting нас)

### Шаг 6. Output

```markdown
# OSS License Review — [product / project]

## Summary

- **Total dependencies analyzed:** [N]
- **By category:**
  - Permissive: [N]
  - Weak copyleft: [N]
  - Strong copyleft (GPL / AGPL): [N]
  - Non-OSS / proprietary: [N]
- **Compatibility issues identified:** [N]

## Critical findings

### 🔴 Blocked

- [GPL component used in proprietary product — must refactor or open-source]

### 🟡 Action needed

- [Missing attribution]
- [LGPL — need linking documentation]
- [Compatibility issue X with Y]

### 🟢 OK

- [List]

## Per-license obligations

### Required actions

- [ ] NOTICE file created with all Apache 2.0 attributions
- [ ] LICENSE file lists всех permissive components
- [ ] (For distribution) — source-on-request mechanism for LGPL components
- [ ] Modifications to copyleft components — marked
- [ ] Branding — no endorsement implied (for BSD 3-Clause components)

## Strategic recommendations

- [Refactor / replace problematic components]
- [Documentation update]
- [Process improvements для future intake — license review at PR / dependency add]
```

## Что НЕ делает

- Не replaces full FOSS audit для material distributions (engage FOSSology / Black Duck для material commercial product)
- Не handles community disputes / contribution conflicts
- Не handles patent retaliation в licenses (engage IP counsel)

## Attribution

Adapted from [`ip-legal/oss-review`](https://github.com/anthropics/claude-for-legal/blob/main/ip-legal/skills/oss-review/SKILL.md) by Anthropic (Apache 2.0).

**Категория A:**
- License categories universal (OSS landscape global)
- Compatibility analysis universal
- Add РФ-specific contexts: реестр Минцифры / IT-аккредитация; импортозамещение; post-2022 sanctions effects на OSS supply chain

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
