# ru-legal — стандартные команды разработки
#
# Этот repo — content + data layer (skills + MCP servers). Корневого
# Python-пакета нет: каждый MCP в mcps/<name>/ — самостоятельный publishable
# pip-пакет со своим pyproject.toml и tests/.

.PHONY: help install-mcps test lint format vendor clean audit audit-staleness mcp-status

help:  ## Показать это меню
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-mcps:  ## Поставить все MCP-пакеты в editable mode (для разработки)
	pip install -e mcps/pravo
	pip install -e mcps/egrul
	pip install -e mcps/kad
	pip install -e mcps/efrsb
	pip install -e mcps/rospatent
	pip install -e mcps/zakupki
	pip install -e mcps/rosreestr
	pip install -e mcps/cbr
	pip install -e mcps/ru-legal-aggregator

audit-staleness:  ## Аудит skills на staleness (last_legislative_update > 6мес)
	python3 scripts/audit_staleness.py

audit:  ## Полный аудит проекта (staleness + другие проверки)
	@echo "=== Skill staleness ==="
	@python3 scripts/audit_staleness.py
	@echo ""
	@echo "=== MCP-STATUS.md ==="
	@head -20 MCP-STATUS.md

mcp-status:  ## Показать текущий MCP-STATUS
	@cat MCP-STATUS.md | head -50

test:  ## Прогнать тесты всех MCP
	pytest mcps/pravo/tests/ mcps/egrul/tests/ mcps/kad/tests/ \
	       mcps/efrsb/tests/ mcps/rospatent/tests/ mcps/zakupki/tests/ \
	       mcps/rosreestr/tests/ mcps/ru-legal-aggregator/tests/ -v

lint:  ## Линтер по всем MCP + скриптам
	ruff check mcps/ scripts/

format:  ## Форматтер
	ruff format mcps/ scripts/

vendor:  ## Склонировать Anthropic claude-for-legal в vendor/ (для порта skills)
	git submodule update --init --recursive
	@if [ ! -d vendor/claude-for-legal ]; then \
		git clone --depth 1 https://github.com/anthropics/claude-for-legal vendor/claude-for-legal; \
	fi

clean:  ## Удалить build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .ruff_cache/ .pyright/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
