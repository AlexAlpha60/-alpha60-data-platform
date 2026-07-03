"""Pagination helpers for Shopify Admin API responses."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx


def extract_next_page_info(response: httpx.Response) -> str | None:
    """Extract the next page_info cursor from a Shopify Link header."""
    link_header = response.headers.get("Link")

    if link_header is None:
        return None

    for link_part in link_header.split(","):
        if 'rel="next"' not in link_part:
            continue

        url_start = link_part.find("<")
        url_end = link_part.find(">")

        if url_start == -1 or url_end == -1:
            return None

        next_url = link_part[url_start + 1 : url_end]
        query = parse_qs(urlparse(next_url).query)
        page_info = query.get("page_info")

        if page_info:
            return page_info[0]

    return None