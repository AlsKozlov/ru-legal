---
name: review
description: >
  Главный router для review коммерческого договора по российскому праву. Определяет
  тип агрита из заголовков и приложений, делегирует к нужному sub-skill (nda-review,
  vendor-agreement-review, saas-msa-review, supply-agreement-review), интегрирует
  output в единый memo. Используй когда пользователь говорит "проверь договор",
  "review этого MSA", "посмотри NDA", "проанализируй услуги", или прикладывает
  inbound договор для review.
argument-hint: '[файл | путь | text]'
user-invocable: true
ported_from: commercial-legal/review
ported_at: 2026-05-17
adaptation_category: B
---

# /review

Review инбаунд договора против playbook в `~/.ru-legal/profiles/contract-law/PROFILE.md`.
Определяет структуру договора из заголовков, выбирает нужный skill, и (если
confirm_routing включён) подтверждает routing у пользователя перед началом анализа.

## Назначение

В отличие от монолитного review всех договоров одним длинным workflow — этот router
делегирует **specialized sub-skills**:
- **NDA / соглашения о неразглашении** → `nda-review` (GREEN/YELLOW/RED triage)
- **Договоры услуг / поставки / подряда** → `vendor-agreement-review` (полный buy-side
  review)
- **SaaS / облачные сервисы / подписки** → `saas-msa-review` (overlay на vendor-agreement
  с фокусом на auto-renewal, ценовая эскалация, SLA, subprocessor's)
- **Договоры с госкорпорациями / по ФЗ-44/223** → `tender-contract-review` (если pack
  `public-procurement` установлен)

Каждый sub-skill **глубже работает с своим жанром**, потому что договор поставки IT
hardware и договор облачной подписки на 3 года имеют принципиально разные риск-профили.

## Инструкции

### Шаг 1. Загрузить practice profile

Прочитай `~/.ru-legal/profiles/contract-law/PROFILE.md`. Если содержит placeholder'ы
(`[заполнить]` и подобные) — остановись:

> "Запусти сначала `/contract-law:cold-start-interview` — мне нужен ваш playbook,
> чтобы review был осмысленным."

Также прочитай → `## Review preferences` → `confirm_routing`. Если поле отсутствует —
treat как `true` (более safe default).

### Шаг 2. Получить договор

Из пути к файлу, текста, или [CLM integration coming soon]. Если ничего не дано — спроси:

> "Дай путь к договору, или вставь текст. Поддерживаются `.docx`, `.txt`, `.md`, `.pdf`
> (PDF только с текстовым слоем — scanned PDF без OCR не сработает)."

### Шаг 3. Прочитать структуру — заголовки в первую очередь

**Перед чтением тела** извлеки:

- Главное название договора (например "Договор оказания услуг", "Договор поставки
  товаров", "Соглашение о неразглашении", "Лицензионный договор")
- Все приложения, дополнительные соглашения, спецификации, протоколы (например
  "Приложение №1 — Спецификация", "Приложение №2 — Регламент SLA", "Приложение №3 — ДОУ
  (договор о обработке ПДн)")

**Это routing signal.** Не полагайся только на body keywords — 40-страничный договор
оказания услуг с словом "конфиденциальность" повсюду — **не NDA**.

### Шаг 4. Выбрать sub-skill(s) на основе структуры

Map по таблице:

| Заголовок главного договора / приложения содержит | Sub-skill |
|---------------------------------------------------|-----------|
| "Соглашение о неразглашении", "NDA", "Договор о конфиденциальности" (как **основной** договор) | **nda-review** |
| "Договор оказания услуг" (гл. 39 ГК), "Договор подряда" (гл. 37 ГК), "Договор на выполнение работ" | **vendor-agreement-review** |
| "Договор поставки" (§3 гл. 30 ГК, ст.506-524), "Договор купли-продажи" (гл. 30 ГК) | **vendor-agreement-review** (с supply-specific overlay) |
| "Подписка", "SaaS", "Облачные услуги", "Договор оказания услуг с ежемесячной/ежегодной оплатой и auto-renewal", "Лицензионный договор на ПО с recurring fees" | **saas-msa-review** (overlay на vendor-agreement-review) |
| "ДОУ", "Договор о обработке персональных данных", "Поручение на обработку ПДн" (как приложение или standalone) | примечание для **vendor-agreement-review** → секция 152-ФЗ |
| "Регламент SLA", "Соглашение об уровне сервиса" (как приложение) | примечание для **saas-msa-review** → SLA секция |
| "Лицензионный договор" (ст.1235 ГК, ст.1286 ГК) на ИС, патенты, ТЗ | **vendor-agreement-review** (с IP overlay) |
| "Договор аренды" (гл. 34 ГК) | **vendor-agreement-review** (с lease overlay) |
| "Договор займа" (гл. 42 ГК), "Кредитный договор" (гл. 42 §2) | (custom — отдельный skill, не покрыто этим router'ом) |

**Множественные skills** часто применяются. Типичные комбинации:

- Договор услуг + ДОУ как приложение → vendor-agreement-review с пометкой про DPA
- SaaS подписка + Спецификация + SLA → saas-msa-review (покрывает все три)
- Договор услуг + Спецификация с auto-renewal → vendor-agreement-review +
  saas-msa-review overlay

Когда структура **genuinely ambiguous** после чтения titles (например документ
назван "Соглашение" без указания exhibits) — прочти первые 2 страницы body чтобы
resolve, потом stop и route.

### Шаг 5. Подтвердить routing (если confirm_routing включён)

Если `confirm_routing: true` в PROFILE.md (или поле отсутствует) — покажи пользователю:

```
Я планирую review как: [тип(ы) договора].

Документы определены:
- [Главный договор title] → [sub-skill]
- [Приложение А title] → [как будет обработано]
- [Приложение B title] → [как будет обработано]

Всё правильно? (да / нет — или подскажи, что не так)
```

Ожидай confirmation перед продолжением. Если пользователь корректирует routing —
apply его инструкцию и продолжай.

Если `confirm_routing: false` — proceed silently. Запиши routing decision в начале
review memo, чтобы пользователь видел, что было применено.

### Шаг 6. Запустить sub-skill(s)

Follow каждый sub-skill полностью. Если несколько применяются — запускай
**последовательно**, потом **интегрируй output в единый memo**. Не производи
отдельные memo для каждого sub-skill.

### Шаг 7. Check эскалации

Если любой issue превышает authority текущего reviewer'а по матрице
`~/.ru-legal/profiles/contract-law/PROFILE.md` → invoke **escalation-flagger** чтобы
route и draft ask.

### Шаг 8. Предложи follow-ups

После завершения review:

- **`stakeholder-summary`** — двухминутное "можно ли подписать" для business owner'а
- **Redline .docx** с tracked changes (через external tool — наш SDK пока не генерит docx)
- **[CLM record creation]** (если CLM подключён — coming soon)
- **Добавить в renewal-tracker** (если auto-renewal обнаружен)
- **`amendment-history`** — если у договора есть доп.соглашения, trace их

## Конфигурация confirm_routing

Добавь в `~/.ru-legal/profiles/contract-law/PROFILE.md` → `## Review preferences`:

```markdown
## Review preferences

confirm_routing: true   # Установи false чтобы пропускать confirmation и proceed automatically.
                        # Рекомендация: true пока строится trust в AI; false когда после 10-20 review
                        # вы уверены в качестве routing decisions.
```

`cold-start-interview` должен спросить про это preference. Default — `true`.

## Примеры

```
/contract-law:review договор-Acme.docx
```

```
/contract-law:review
[вставь текст договора]
```

```
/contract-law:review ./contracts/yandex-cloud-msa.pdf
```

## Output

Полный review memo по format'у sub-skill'а. Routing decision залогирован в начале.
Deviation-by-deviation, конкретные redlines, названный approver.

Сохраняется по пути, который PROFILE.md `## House style` указывает для work product
(default: `./contract-reviews/<contract-id>-<YYYY-MM-DD>/review.md`).

---

## Специфика для РФ контекста

### Особенности routing для РФ договоров

Российская договорная классификация **отличается от US**. Несколько частых ловушек:

1. **"Договор оказания услуг" vs "Договор подряда"** — ГК разделяет (гл.39 vs гл.37),
   и применимые нормы существенно разные:
   - Услуги: результат — действия (ст.779 ГК). Нет деталируемых требований к
     результату — заказчик платит за процесс.
   - Подряд: результат — материальный или нематериальный продукт (ст.702 ГК). Есть
     ответственность за качество результата.
   - При routing — если документ называется "услуги" но фактически описывает создание
     продукта (например IT-разработка), пометь это в routing decision: "формально
     услуги, по содержанию ближе к подряду".

2. **Смешанные договоры** — ст.421 п.3 ГК разрешает смешанные договоры. Часто
   встречается "договор поставки оборудования с услугами установки и обслуживания" —
   это **mixed**. При routing — может потребоваться **множественные sub-skills**:
   vendor-agreement (поставка) + vendor-agreement (услуги) + saas-msa (если есть
   recurring обслуживание).

3. **Договоры с госкорпорациями (по ФЗ-44/223)** — имеют **обязательные** template
   formы. Reviewer's authority ограничена — нельзя менять fundamental terms.
   Если в routing определён госконтракт — пометь и route к специальному
   `public-procurement/tender-contract-review` (если pack установлен).

4. **Договоры в иностранной валюте** — auto-flag: валютный контроль (173-ФЗ).
   Эскалация автоматическая по escalation-flagger.

### Применимое право — особая внимание

Если в договоре указано `governing law: не РФ` (англ. право, право Кипра, и т.д.) —
**это auto-escalate** до решения юриста с международной практикой. Текущие
ограничения на признание иностранных судебных решений в РФ делают такие договоры
проблемными к исполнению. Skill не должен этот вопрос решать сам.

---

## Attribution

Adapted from [`commercial-legal/review`](https://github.com/anthropics/claude-for-legal/blob/main/commercial-legal/skills/review/SKILL.md)
by Anthropic (Apache 2.0).

**Изменения от оригинала:**
- Practice profile path: → `~/.ru-legal/profiles/contract-law/PROFILE.md`
- Routing таблица переписана для РФ договорной классификации:
  - "Master Services Agreement" → "Договор оказания услуг" / "Договор подряда"
  - "Subscription / SaaS" — оставлен (термин universal)
  - "DPA" → "ДОУ / Поручение на обработку ПДн"
  - Добавлены: договор поставки (§3 гл.30 ГК), договор аренды (гл.34), лицензионный (ст.1235)
- Добавлена секция "Специфика для РФ контекста" с **критичными distinction'ами**:
  услуги vs подряд (гл.39 vs гл.37 ГК), смешанные договоры (ст.421 п.3), госконтракты,
  применимое право не-РФ
- "Drive link" и "CLM ID" упоминания заменены на placeholder coming-soon
- Matter context секция убрана (наш SDK пока не поддерживает matters)

**Original copyright:** © 2026 Anthropic PBC, licensed under Apache License 2.0.
**Adapted by:** ru-legal contributors, 2026-05-17.

---

## Disclaimer

Этот skill производит preliminary routing и анализ для использования
квалифицированным юристом. Не legal advice. Routing decisions требуют верификации
юристом для critical договоров (M&A, инвестиционные сделки, госконтракты).

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
