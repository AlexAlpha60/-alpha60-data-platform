"""Unit tests for incremental loading state models."""

from __future__ import annotations

from datetime import UTC, datetime

from alpha60.state import IncrementalState


def test_incremental_state_stores_cursor_details() -> None:
    """IncrementalState stores the job cursor details."""
    cursor_value = datetime(2026, 7, 3, 12, 30, tzinfo=UTC)

    state = IncrementalState(
        job_name="shopify-products",
        cursor_field="updated_at",
        cursor_value=cursor_value,
    )

    assert state.job_name == "shopify-products"
    assert state.cursor_field == "updated_at"
    assert state.cursor_value == cursor_value