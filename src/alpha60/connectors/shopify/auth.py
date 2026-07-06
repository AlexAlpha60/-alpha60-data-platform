"""Shopify authentication support."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import logging

from alpha60.core.http.client import HTTPClient

_LOGGER = logging.getLogger(__name__)

_CLIENT_CREDENTIALS_GRANT = "client_credentials"
_REFRESH_BUFFER = timedelta(minutes=5)


@dataclass(frozen=True, slots=True)
class ShopifyAccessToken:
    """Access token returned by Shopify OAuth."""

    access_token: str
    scope: str
    expires_at: datetime

    def is_valid(self, *, now: datetime) -> bool:
        """Return whether the token is valid beyond the refresh buffer."""
        return now + _REFRESH_BUFFER < self.expires_at


class ShopifyAuthenticator:
    """Exchange Shopify app credentials for a temporary access token."""

    def __init__(
        self,
        *,
        shop_domain: str,
        client_id: str,
        client_secret: str,
        http_client: HTTPClient | None = None,
    ) -> None:
        """Initialize the Shopify authenticator."""
        self.shop_domain = shop_domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_client = http_client or HTTPClient()
        self._cached_token: ShopifyAccessToken | None = None

    def get_access_token(self) -> str:
        """Return a valid cached access token or exchange credentials for a new one."""
        now = datetime.now(UTC)

        if self._cached_token is None or not self._cached_token.is_valid(now=now):
            self._cached_token = self._exchange_access_token(now=now)

        return self._cached_token.access_token

    def _exchange_access_token(self, *, now: datetime) -> ShopifyAccessToken:
        """Exchange client credentials for a Shopify access token."""
        _LOGGER.info(
            "Exchanging Shopify client credentials for access token",
            extra={"shop_domain": self.shop_domain},
        )

        response = self.http_client.post(
            self._build_token_url(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": _CLIENT_CREDENTIALS_GRANT,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        payload = response.json()
        expires_in = int(payload.get("expires_in", 0))

        token = ShopifyAccessToken(
            access_token=str(payload["access_token"]),
            scope=str(payload.get("scope", "")),
            expires_at=now + timedelta(seconds=expires_in),
        )

        _LOGGER.info(
            "Shopify access token exchange succeeded",
            extra={
                "shop_domain": self.shop_domain,
                "scope": token.scope,
                "expires_at": token.expires_at.isoformat(),
            },
        )

        return token

    def _build_token_url(self) -> str:
        """Build the Shopify OAuth token URL."""
        return f"https://{self.shop_domain}/admin/oauth/access_token"
