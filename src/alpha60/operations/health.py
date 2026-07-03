"""Operational health checks for ALPHA60 dependencies."""

from dataclasses import dataclass
from enum import StrEnum


class HealthStatus(StrEnum):
    """Possible health check statuses."""

    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class HealthCheckResult:
    """Result of a single operational health check."""

    name: str
    status: HealthStatus
    message: str