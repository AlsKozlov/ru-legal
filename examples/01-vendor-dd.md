# Example 1: DD контрагента перед сделкой

## Контекст

In-house GC в производственной компании рассматривает заключение договора поставки сырья на ~50 млн ₽/год с новым поставщиком — ООО "Альфа Снаб". Нужна экспресс-проверка перед подписанием SPA.

**Время вручную:** 2-3 часа (открыть 5 порталов, перенести данные в Excel, написать summary).
**Время с ru-legal:** ~3 минуты.

## Skills + MCPs

- Skill: `corporate-law/diligence-issue-extraction`
- MCPs: `egrul`, `kad`, `efrsb`, `rospatent`, `zakupki`

## User prompt

```
GC: /diligence-issue-extraction

Контрагент: ООО "Альфа Снаб"
ИНН: 7707000001
Сделка: договор поставки металлопроката
Annual value: 50,000,000 ₽
Scope: full DD, focus B (Tax) + C (Litigation) + D (Bankruptcy)
```

## Flow under the hood

```
LLM читает SKILL.md и понимает категории A-L для DD
↓
Tool call 1: egrul.find_company(inn="7707000001")
  → {name: "ООО Альфа Снаб", ogrn: "1027707000050",
     director: "Иванов И.И.", founded: "2015-03-15",
     beneficiaries: [...], capital: 2_000_000}
↓
Tool call 2: efrsb.check_company_bankruptcy(inn="7707000001")
  → {status: "no_bankruptcy", _note: "Активного банкротного дела нет"}
↓
Tool call 3: kad.search_cases(defendant_inn="7707000001", limit=20)
  → [3 cases:
      A40-15234/2024 — взыскание 5.2М, в суде (probably защищаются)
      A40-99012/2023 — налоговый спор с ФНС, проиграли 12М
      A40-77001/2022 — поставка некачественных товаров, проиграли 3М]
↓
Tool call 4: kad.search_cases(plaintiff_inn="7707000001", limit=20)
  → [8 cases as plaintiff — взыскивают с своих контрагентов;
     2 successful, 4 ongoing, 2 lost]
↓
Tool call 5: rospatent.search_trademark(holder_inn="7707000001")
  → [] (нет зарегистрированных ТЗ)
↓
Tool call 6: zakupki.get_supplier_contracts(supplier_inn="7707000001")
  → [12 контрактов 44-ФЗ за 3 года; все executed успешно;
     суммарно 180М; track record хороший]
↓
LLM применяет risk thresholds из SKILL.md +
структурирует output по 12 категориям
```

## Output (выдержка)

```markdown
# DD Issues — ООО "Альфа Снаб" (ИНН 7707000001)
**Дата:** 2026-05-20
**Сделка:** договор поставки металлопроката 50М ₽/год
**Scope:** focused — B/C/D + L

## Bottom line

**PROCEED WITH CONDITIONS.** Контрагент действующий, без банкротства, выполняет
гос.контракты. Однако ⚠ **3 проигранных дела за 4 года** indicate proблемы
с качеством товаров и налоговой compliance.

## Critical issues (🔴)

### B Tax (1)

**Налоговый спор с ФНС — A40-99012/2023, проиграли 12М ₽**
- Доначисление НДС за 2021-2022 период
- Решение УФНС в силе, иск в АС проигран
- **Implication:** возможен повтор — контрагент не соблюдает НК аккуратно
- **Recommended action:** запросить tax compliance certificate за 2024-2025;
  включить tax indemnity в SPA на uncapped basis

### C Litigation (2)

**Иск о некачественной поставке — A40-77001/2022, проиграли 3М ₽**
- Поставили металлопрокат не соответствующий ГОСТ
- **Implication:** quality control issue
- **Recommended action:** усиленные quality checks при приёмке; SLA по replace defects

**Активный иск как ответчик — A40-15234/2024, 5.2М ₽ в споре**
- Текущий иск, исход не определён
- **Implication:** возможен exposure
- **Recommended action:** monitor исход; не критично для нашей сделки

## Medium issues (🟡)

### A Corporate

- Уставный капитал 2М ₽ — стандартный для малого business
- Директор стабилен с 2018 года — позитив
- Бенефициары disclosed корректно — OK

### L Reputation

- 12 успешных гос.контрактов за 3 года — strong track record
- Нет в РНП (Реестр недобросовестных поставщиков) — OK

## 🟢 OK

- D Bankruptcy: clean (efrsb проверен)
- G IP: no IP exposure (нет ТЗ / патентов значимых)
- Корпоративная структура простая, без offshore

## Recommended SPA provisions

### Reps & warranties (по ст.431.2 ГК)

1. Tax compliance — отсутствие открытых ВНП, неуплаченных доначислений
2. Quality — товар соответствует ГОСТ X-XX
3. No undisclosed litigation > 1М ₽
4. No bankruptcy filings pending against contractor

### Indemnification (по ст.406.1 ГК)

- **Uncapped:** tax matters (включая ВНП доначисления за период до подписания)
- **Cap 20% от annual value (10М):** quality / SLA нарушения
- **Survival:** 36 мес с подписания

### Other

- **Право unilateral termination** при просрочке поставки > 5 раб.дней
- **Quality control** через independent inspection (Bureau Veritas / СГС / etc.)
- **Security deposit** 5% от annual value (2.5М ₽) на эскроу

## Ссылки на источники

- ЕГРЮЛ выписка: [egrul.nalog.ru/...](https://egrul.nalog.ru)
- Кат.арбитр A40-99012/2023: [kad.arbitr.ru/Card/...](https://kad.arbitr.ru)
- ЕФРСБ проверка: clean (дата 2026-05-20)

## ⚠ Disclaimer

Это AI-output на основе доступных данных гос.реестров. **Не заменяет** full DD
outside-юристом перед сделкой 50М ₽/год. Рекомендуем engage outside-адв ФПА
для review SPA и финального заключения.
```

## Что юрист делает дальше

1. **Review output** — проверяет ключевые findings
2. **Verifies** через КонсультантПлюс / Гарант ссылки на cases
3. **Sends к decision-makers** (CFO / CEO) с recommendation
4. **Если решили GO** — outside-адв ФПА drafts SPA с recommended provisions
5. **Если decided NO** — formal rejection notice контрагенту

**Время сэкономлено:** ~2 часа на DD + 1 час на структурирование report = **3 часа**.

При rate 5000 ₽/час → **сэкономлено ~15,000 ₽ на одной DD**. При 20 DD в месяц — экономия 300k ₽/месяц на in-house юриста.

## Технические детали

- **LLM:** GigaChat (доступен в РФ без VPN) или Claude Sonnet
- **Token cost:** ~3000 input + 2000 output = ~$0.05-0.20 в зависимости от провайдера
- **MCP latency:** ~5 секунд (5 параллельных HTTP calls к гос.реестрам)
- **Total time:** ~30 секунд от prompt до output

## Известные limitations

- `egrul` MCP требует api-fns.ru API key (paid ~3k₽/мес или freemium tier)
- `kad` иногда возвращает 403 (anti-bot); тогда output flagged "verify manually"
- `efrsb` бесплатный и стабильный — самый reliable
- DD-output **не финальный документ** — для signing нужен outside-адв review
