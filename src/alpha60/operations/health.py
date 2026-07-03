"""Operational health checks for ALPHA60 dependencies."""

from dataclasses import dataclass
from enum import StrEnum

from alpha60.config.settings import Settings
from alpha60.connectors.shopify.client import ShopifyClient


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


def check_configuration(settings: Settings) -> HealthCheckResult:
    """Validate platform configuration."""
    missing: list[str] = []

    if not settings.shopify.shop_domain:
        missing.append("shopify.shop_domain")

    if not settings.shopify.access_token:
        missing.append("shopify.access_token")

    if not settings.bigquery.project_id:
        missing.append("bigquery.project_id")

    if not settings.bigquery.dataset_id:
        missing.append("bigquery.dataset_id")

    if missing:
        return HealthCheckResult(
            name="config",
            status=HealthStatus.FAIL,
            message=f"Missing configuration: {', '.join(missing)}",
        )

    return HealthCheckResult(
        name="config",
        status=HealthStatus.PASS,
        message="Configuration is valid.",
    )


def check_shopify(settings: Settings) -> HealthCheckResult:
    """Validate Shopify connectivity."""
    client = ShopifyClient(
        shop_domain=settings.shopify.shop_domain,
        access_token=settings.shopify.access_token,
        api_version=settings.shopify.api_version,
    )

    if client.test_connection():
        return HealthCheckResult(
            name="shopify",
            status=HealthStatus.PASS,
            message="Shopify connection succeeded.",
        )

    return HealthCheckResult(
        name="shopify",
        status=HealthStatus.FAIL,
        message="Shopify connection failed.",
    )