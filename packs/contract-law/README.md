# contract-law — договорное право РФ

Plugin pack для работы с коммерческими договорами по российскому праву. Покрывает: купля-продажа, поставка, услуги, аренда, NDA, лицензии, дистрибьюция, занятость.

## Что внутри

### Skills (MVP — 3 из 12)

| Skill | Команда | Статус |
|-------|---------|--------|
| `cold-start-interview` | `/contract-law:cold-start-interview` | ✅ MVP |
| `contract-review` | `/contract-law:contract-review` | ✅ MVP |
| `nda-draft` | `/contract-law:nda-draft` | ✅ MVP |
| `service-agreement-draft` | `/contract-law:service-agreement-draft` | 🚧 Roadmap |
| `supply-contract-review` | `/contract-law:supply-contract-review` | 🚧 Roadmap |
| `lease-agreement` | `/contract-law:lease-agreement` | 🚧 Roadmap |
| `employment-contract` | `/contract-law:employment-contract` | 🚧 Roadmap |
| `licensing-agreement` | `/contract-law:licensing-agreement` | 🚧 Roadmap |
| `liability-analysis` | `/contract-law:liability-analysis` | 🚧 Roadmap |
| `force-majeure-check` | `/contract-law:force-majeure-check` | 🚧 Roadmap |
| `termination-notice` | `/contract-law:termination-notice` | 🚧 Roadmap |
| `distribution-agreement` | `/contract-law:distribution-agreement` | 🚧 Roadmap |

### Managed agents

| Agent | Назначение |
|-------|-----------|
| `contract-renewal-watcher` | Headless мониторинг — алерт за N дней до auto-renewal или окончания |

## Что нужно подключить

Этот pack оптимально работает с подключёнными MCP серверами:

- `pravo` — тексты НПА (рекомендуется обязательно)
- `egrul` — проверка контрагентов (опционально, но сильно повышает качество review)
- `kad` — судебная практика (опционально)

См. `.mcp.json` в этой папке.

## Первый запуск

```
/contract-law:cold-start-interview
```

Skill задаст вопросы про вашу компанию и заполнит profile. Без profile остальные скиллы работать не будут.

## Юридический disclaimer

Все output'ы — preliminary анализ для использования квалифицированным юристом. Не legal advice. См. главный [README.md](../README.md) репо.
