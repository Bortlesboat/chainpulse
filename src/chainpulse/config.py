"""Environment variable loading and validation."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str
    api_base_url: str
    model: str

    @classmethod
    def load(cls) -> Config:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ConfigError(
                "ANTHROPIC_API_KEY not set. "
                "Get one at https://console.anthropic.com/keys"
            )

        api_base_url = os.environ.get(
            "CHAINPULSE_API_URL", "https://bitcoinsapi.com"
        ).rstrip("/")

        model = os.environ.get("CHAINPULSE_MODEL", "claude-sonnet-4-20250514")

        return cls(
            anthropic_api_key=api_key,
            api_base_url=api_base_url,
            model=model,
        )


class ConfigError(Exception):
    """Raised when configuration is invalid."""
