# Security Policy

## Reporting vulnerabilities

**Не публикуй уязвимости в публичных Issues / PRs.**

Если ты нашёл security проблему:

- **GitHub Security Advisory:** воспользуйся "Report a vulnerability" во вкладке Security репозитория (включается автоматически после форка)
- **Email / приватные каналы:** будут добавлены после настройки maintainer-инфраструктуры

Включи:
- Описание уязвимости
- Steps to reproduce
- Potential impact
- Suggested fix (если есть идеи)

## Что считается security issue

### 🔴 Critical

- **Path traversal** в MCP / harness кода (чтение arbitrary файлов)
- **SSRF** в MCP HTTP requests
- **Command injection** в shell commands (если будут)
- **Credentials в logs** (API keys в stderr / stdout)
- **Code execution** через crafted skill / MCP response

### 🟡 Medium

- **Information disclosure** через error messages
- **Rate limiting bypass** в MCP servers
- **Cache poisoning** в MCP caches
- **Dependency vulnerabilities** в высоком CVSS

### 🟢 Low

- **Logging issues** (verbose / missing logs)
- **Edge case crashes** без data leakage
- **Performance issues** не leading to DoS

## Response time

| Severity | First response | Fix targeting |
|----------|----------------|---------------|
| Critical | 48 hours | 7 days |
| Medium | 5 days | 30 days |
| Low | 14 days | best-effort |

## Disclosure

После fix:
- **Coordinated disclosure** — мы publish advisory одновременно с release
- **Credit** в advisory (если хочешь — указываем твоё имя / handle)
- **CVE assignment** — если applicable, через GitHub Security Advisory

## Specifically для MCP servers

Каждый MCP server делает HTTP запросы к external sources. Risk vectors:

| Vector | Mitigation |
|--------|------------|
| Поддельный response от source может trigger crash | Все responses pydantic-validated; broad except → ToolError |
| Cache poisoning | Cache keyed by exact request params; TTL bounded |
| SSRF через URL params | Все URLs hardcoded; params в querystring only |
| API key leakage | Keys читаются из env vars; never logged |

## Specifically для skills

Skills — это просто Markdown. Не код, не execute. **Однако:**

- **Prompt injection** через skill content — теоретически possible если кто-то закоммитит malicious skill
- **Mitigation:** все PRs review; suspicious skills reverted
- **Read users:** не используй forks от unknown sources без review

## Скоуп **не security**

- Hallucinations LLM — это known limitation (см. [DISCLAIMER.md](DISCLAIMER.md))
- Outdated legal норм — same
- Wrong analysis в skill — bug, не security issue
- Юридический совет qualified как профессиональная услуга — см. DISCLAIMER

Эти issues — обычные bug reports / issues, не security advisories.

## Bug bounty

В данный момент **нет formal bug bounty programme** (проект на early stage). Рассматриваем:
- Public recognition в advisory
- Сувениры (для critical issues)
- Future: возможно paid bounty после roundу финансирования

Спасибо за помощь в безопасности проекта!
