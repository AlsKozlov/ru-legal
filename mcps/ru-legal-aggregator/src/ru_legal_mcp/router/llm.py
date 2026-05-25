"""Lightweight LLM client для router — поддерживает любой OpenAI-compat endpoint.

Не зависим от ru_legal SDK провайдеров (которые уезжают в отдельный agent repo).
Здесь минимум — completion с system + user prompt.

Поддерживает:
- OpenAI cloud (`OPENAI_API_KEY`)
- Anthropic (`ANTHROPIC_API_KEY`) — через специальный path
- YandexGPT (`YC_IAM_TOKEN` + `YC_FOLDER_ID`)
- GigaChat (`GIGACHAT_API_KEY`)
- DeepSeek (`DEEPSEEK_API_KEY`)
- Self-hosted (vLLM / Ollama — через `LLM_BASE_URL`)

Auto-detect from env variables; user может override через `RU_LEGAL_ROUTER_LLM` env.
"""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class RouterLLMClient:
    """Minimal OpenAI-compat LLM client для router."""

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ):
        self.provider = (provider or os.getenv("RU_LEGAL_ROUTER_LLM") or "").lower()
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self._http: httpx.AsyncClient | None = None
        self._auto_configure()

    def _auto_configure(self) -> None:
        """Detect provider from env if not explicitly set."""
        if self.provider:
            self._configure_provider(self.provider)
            return

        # Auto-detect order
        if os.getenv("OPENAI_API_KEY"):
            self._configure_provider("openai")
        elif os.getenv("DEEPSEEK_API_KEY"):
            self._configure_provider("deepseek")
        elif os.getenv("YC_IAM_TOKEN") and os.getenv("YC_FOLDER_ID"):
            self._configure_provider("yandexgpt")
        elif os.getenv("GIGACHAT_API_KEY"):
            self._configure_provider("gigachat")
        elif os.getenv("ANTHROPIC_API_KEY"):
            self._configure_provider("anthropic")
        elif os.getenv("LLM_BASE_URL"):
            self._configure_provider("openai-compat")
        else:
            logger.info("No LLM configured for router — Strategy C unavailable, falls back to keyword")
            self.provider = ""

    def _configure_provider(self, name: str) -> None:
        self.provider = name
        if name == "openai":
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            self.base_url = self.base_url or "https://api.openai.com/v1"
            self.model = self.model or "gpt-4o-mini"
        elif name == "deepseek":
            self.api_key = self.api_key or os.getenv("DEEPSEEK_API_KEY")
            self.base_url = self.base_url or "https://api.deepseek.com"
            self.model = self.model or "deepseek-chat"
        elif name == "yandexgpt":
            # YandexGPT использует свой API — отдельная implementation в complete()
            self.api_key = self.api_key or os.getenv("YC_IAM_TOKEN")
            self.base_url = self.base_url or "https://llm.api.cloud.yandex.net/foundationModels/v1"
            self.model = self.model or "yandexgpt-lite"
        elif name == "gigachat":
            self.api_key = self.api_key or os.getenv("GIGACHAT_API_KEY")
            self.base_url = self.base_url or "https://gigachat.devices.sberbank.ru/api/v1"
            self.model = self.model or "GigaChat"
        elif name == "anthropic":
            self.api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            self.base_url = self.base_url or "https://api.anthropic.com/v1"
            self.model = self.model or "claude-haiku-4-5"
        elif name == "openai-compat":
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY") or "no-key"
            self.base_url = self.base_url or os.getenv("LLM_BASE_URL")
            self.model = self.model or os.getenv("LLM_MODEL") or "default"
        else:
            raise ValueError(f"Unknown provider: {name}")

    @property
    def is_configured(self) -> bool:
        return bool(self.provider and self.base_url)

    def _get_http(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self.timeout)
        return self._http

    async def complete(self, system: str, user: str) -> str:
        """Send chat completion request."""
        if not self.is_configured:
            raise RuntimeError("Router LLM not configured")

        if self.provider == "yandexgpt":
            return await self._complete_yandex(system, user)
        if self.provider == "anthropic":
            return await self._complete_anthropic(system, user)
        return await self._complete_openai_compat(system, user)

    async def _complete_openai_compat(self, system: str, user: str) -> str:
        """OpenAI-compatible chat completions."""
        http = self._get_http()
        resp = await http.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.0,
                "max_tokens": 1024,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    async def _complete_yandex(self, system: str, user: str) -> str:
        """YandexGPT chat completion."""
        http = self._get_http()
        folder_id = os.getenv("YC_FOLDER_ID", "")
        model_uri = f"gpt://{folder_id}/{self.model}/latest"
        resp = await http.post(
            f"{self.base_url}/completion",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "modelUri": model_uri,
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.0,
                    "maxTokens": "1024",
                },
                "messages": [
                    {"role": "system", "text": system},
                    {"role": "user", "text": user},
                ],
            },
        )
        resp.raise_for_status()
        data = resp.json()
        alts = data.get("result", {}).get("alternatives", [])
        return alts[0].get("message", {}).get("text", "") if alts else ""

    async def _complete_anthropic(self, system: str, user: str) -> str:
        """Anthropic Messages API."""
        http = self._get_http()
        resp = await http.post(
            f"{self.base_url}/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "system": system,
                "messages": [{"role": "user", "content": user}],
                "temperature": 0.0,
                "max_tokens": 1024,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        blocks = data.get("content", [])
        return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")

    async def aclose(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None
