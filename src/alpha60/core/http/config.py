"""Configuration for the generic HTTP client."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HTTPConfig:
    """Configuration for HTTP client behaviour."""

    timeout: float = 30.0
    max_retries: int = 3
    backoff_factor: float = 1.0
    user_agent: str = "ALPHA60-Data-Platform/1.0"