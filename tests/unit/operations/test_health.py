"""Tests for operational health checks."""

from alpha60.operations.health import HealthCheckResult, HealthStatus


def test_health_check_result_stores_check_details() -> None:
    """Health check results expose their name, status, and message."""
    result = HealthCheckResult(
        name="config",
        status=HealthStatus.PASS,
        message="Configuration is valid.",
    )

    assert result.name == "config"
    assert result.status == HealthStatus.PASS
    assert result.message == "Configuration is valid."
    