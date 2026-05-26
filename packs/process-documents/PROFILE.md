---
pack_name: process-documents
description: |
  Подготовка процессуальных документов: иски, отзывы, апелляции, кассации,
  ходатайства, мировые соглашения. Cross-cutting pack — используется во всех
  доменах (трудовое, семейное, налоговое, и т.д.).
domain: process
status: alpha
domain_owner: TBD
skill_count: 15
last_updated: "2026-05-26"
target_audience:
  - Юристы всех специализаций (everyone drafts documents)
  - Юр.ассистенты / paralegals
  - In-house юристы корпов
---

# process-documents — Процессуальные документы

## Что внутри

Cross-cutting pack для подготовки процессуальных документов **любого типа**:
- Исковые заявления (гражданские, арбитражные, административные)
- Отзывы и возражения
- Апелляции, кассации, надзорные
- Ходатайства (отвод, истребование, экспертиза, отложение)
- Мировые соглашения
- Расчёт процессуальных сроков

Pack не привязан к domain — используется в **сочетании с domain pack'ами**
(labor-law + process-documents = иск о восстановлении на работе).

## Skills

| Skill | Status | Priority | Description |
|---|---|---|---|
| claim-draft-civil | 🟢 in-progress | P0 | Иск в суд общей юрисдикции (ГПК) |
| claim-draft-arbitration | 🔴 alpha | P0 | Иск в арбитражный суд (АПК) |
| response-draft | 🔴 alpha | P0 | Отзыв на иск (возражения) |
| appeal-draft | 🔴 alpha | P1 | Апелляционная жалоба |
| cassation-draft | 🔴 alpha | P1 | Кассационная жалоба |
| supervisory-complaint | 🔴 alpha | P2 | Надзорная жалоба |
| motion-evidence-collection | 🟢 in-progress | P0 | Ходатайство об истребовании доказательств |
| motion-judge-recusal | 🔴 alpha | P1 | Отвод судьи |
| motion-expertise | 🔴 alpha | P1 | Назначение судебной экспертизы |
| motion-postponement | 🔴 alpha | P2 | Отложение разбирательства |
| settlement-agreement | 🔴 alpha | P1 | Мировое соглашение |
| statement-of-claim-amendment | 🔴 alpha | P2 | Уточнение исковых требований |
| procedural-deadlines-calc | 🔴 alpha | P1 | Расчёт процессуальных сроков |
| jurisdiction-determination | 🔴 alpha | P0 | Определение подсудности |
| court-fee-calculation | 🔴 alpha | P1 | Расчёт госпошлины |

## Когда использовать

**Всегда когда юристу нужно подготовить процессуальный документ.**

Типичные сценарии:
- "Подготовь иск о восстановлении на работе" → labor-law/termination-review + process-documents/claim-draft-civil
- "Прислали иск, нужно ответить" → response-draft + relevant domain pack
- "Хочу обжаловать решение суда" → appeal-draft

## Когда НЕ использовать

- Если нужны нюансы конкретного домена (например, особенности налогового иска) — нужен parallel domain pack
- Для уголовных дел — отдельный pack (criminal-process, ещё не написан)

## Required MCPs

- `pravo-mcp` — актуальные редакции АПК/ГПК
- `documents-mcp` (planned) — шаблоны процессуальных документов
- `kad-mcp` — для проверки подсудности (если арбитраж)
- `gas-pravosudie-mcp` (planned) — для проверки подсудности (если СОЮ)

## Ключевая нормативка

- ГПК РФ (для СОЮ)
- АПК РФ (для арбитража)
- КАС РФ (для административных дел)
- Постановления Пленума ВС РФ по процессу
- НК РФ Глава 25.3 (госпошлины)
