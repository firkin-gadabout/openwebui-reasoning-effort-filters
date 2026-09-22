"""
title: Reasoning Effort (GPT-5.6)
id: reasoning_effort_gpt56
description: Per-chat reasoning effort for the GPT-5.6 family (Sol/Terra/Luna). All three support none/low/medium/high/xhigh/max.
author: branden
version: 1.3.0
required_open_webui_version: 0.11.4
"""

import logging
from typing import Literal, Optional

from pydantic import BaseModel, Field

try:
    from open_webui.models.config import Config
except ImportError:  # pragma: no cover - filter loaded outside the backend
    Config = None

log = logging.getLogger(__name__)

GPT56_MODELS = ("gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna")


class Filter:
    class Valves(BaseModel):
        priority: int = Field(default=0)

    class UserValves(BaseModel):
        effort: Literal["default", "none", "low", "medium", "high", "xhigh", "max"] = (
            Field(
                default="default",
                description=(
                    "How much to think. 'default' = send nothing (model default, medium). "
                    "'none' = no reasoning (fastest, cheapest)."
                ),
            )
        )

    def __init__(self) -> None:
        self.valves = self.Valves()
        self.toggle = True
        self.icon = (
            "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
            "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E"
            "%3Cpath d='M13 2 3 14h9l-1 8 10-12h-9l1-8z'/%3E%3C/svg%3E"
        )

    @staticmethod
    async def _uses_responses_api(__model__: Optional[dict]) -> bool:
        """True when the model's OpenAI connection is set to the Responses API.

        The request filter runs BEFORE Open WebUI converts the Chat-Completions
        payload to the Responses shape (convert_to_responses_payload in
        routers/openai.py), so the body here is ALWAYS the 'messages' form —
        even for Responses-API connections. Keying off the body shape therefore
        always injects the flat 'reasoning_effort', which /v1/responses rejects
        with HTTP 400. The connection's 'api_type' is the only reliable signal.
        """
        if not isinstance(__model__, dict):
            return False
        idx = __model__.get("urlIdx")
        if idx is None:
            return False
        if Config is None:
            log.warning(
                "Reasoning: cannot read OpenAI config; assuming Chat Completions"
            )
            return False
        try:
            configs = await Config.get("openai.api_configs", {}) or {}
            api_config = configs.get(str(idx), configs.get(idx, {})) or {}
            return api_config.get("api_type") == "responses"
        except Exception:
            log.warning(
                "Reasoning: failed to read OpenAI connection config; assuming Chat Completions",
                exc_info=True,
            )
            return False

    async def request(
        self, body: dict, __user__: dict, __model__: Optional[dict] = None
    ) -> dict:
        # NOTE: the runtime only passes params it can supply (body, __user__,
        # __id__, __model__, __metadata__, __request__, ...). 'logger' is NOT
        # one of them — declaring it here crashes every request with a TypeError.
        model_id = str(body.get("model") or "").lower()
        if not any(m in model_id for m in GPT56_MODELS):
            log.info(
                "Reasoning: attached to GPT-5.6 but request targets '%s'; not injecting",
                model_id,
            )
            return body

        effort = getattr(__user__.get("valves"), "effort", "default")
        if effort == "default":
            return body  # send nothing; model default applies

        # Wire format is decided by the CONNECTION, not the body:
        #   Responses API  -> nested  reasoning.effort
        #   Chat Completions -> flat  reasoning_effort
        # 'none' is sent explicitly on purpose: 5.6 reasons by default, and
        # /v1/chat/completions rejects default reasoning when function tools
        # are present. Idempotent, so safe to run on every tool-loop hop.
        if await self._uses_responses_api(__model__):
            reasoning = body.get("reasoning")
            if not isinstance(reasoning, dict):
                reasoning = {}
            reasoning["effort"] = effort
            body["reasoning"] = reasoning
            body.pop("reasoning_effort", None)  # flat key 400s on the Responses API
        else:
            body["reasoning_effort"] = effort
            body.pop(
                "reasoning", None
            )  # nested object isn't accepted by Chat Completions
        return body
