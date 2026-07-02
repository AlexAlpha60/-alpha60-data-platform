"""Tests for HTTP configuration."""

from dataclasses import FrozenInstanceError

import pytest

from alpha60.core.http.config import HTTPConfig


def test_default_configuration() -> None:
    config = HTTPConfig()

    assert config.timeout == 30.0
    assert config.max_retries == 3
    assert config.backoff_factor == 1.0
    assert config.user_agent == "ALPHA60-Data-Platform/1.0"


def test_custom_configuration() -> None:
    config = HTTPConfig(
        timeout=10.0,
        max_retries=5,
        backoff_factor=2.0,
        user_agent="TestClient/1.0",
    )

    assert config.timeout == 10.0
    assert config.max_retries == 5
    assert config.backoff_factor == 2.0
    assert config.user_agent == "TestClient/1.0"


def test_configuration_is_immutable() -> None:
    config = HTTPConfig()

    with pytest.raises(FrozenInstanceError):
        config.timeout = 60.0  # type: ignore[misc]