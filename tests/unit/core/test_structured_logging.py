"""Unit tests for structured logging."""

from __future__ import annotations

import json
import logging

from alpha60.core.logging import JsonFormatter, get_logger


def test_get_logger_returns_named_logger() -> None:
    """get_logger should return a logger with the requested name."""
    logger = get_logger("alpha60.test")

    assert logger.name == "alpha60.test"


def test_json_formatter_outputs_expected_fields() -> None:
    """JsonFormatter should emit valid JSON with the expected fields."""
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name="alpha60.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "alpha60.test"
    assert payload["message"] == "Test message"
    assert "timestamp" in payload


def test_json_formatter_includes_extra_fields() -> None:
    """JsonFormatter should include structured fields from the log record."""
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name="alpha60.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Loaded records",
        args=(),
        exc_info=None,
    )
    record.rows_loaded = 123

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["rows_loaded"] == 123