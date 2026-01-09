"""Centralised application configuration primitives."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple


@dataclass(frozen=True)
class Settings:
    """Immutable settings for the backend service."""

    api_title: str = "Superstore Insights API"
    api_description: str = "API for visualizing Superstore sales data"
    api_version: str = "1.0.0"
    cors_origins: Tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    )
    data_source_url: str = (
        "https://raw.githubusercontent.com/texodus/superstore-arrow/master/superstore.arrow"
    )
    request_timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    """Return the memoised settings instance."""

    return Settings()
