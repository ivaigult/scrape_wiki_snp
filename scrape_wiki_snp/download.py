"""File download routine."""

from __future__ import annotations

import requests
import requests_cache


def _install_cache() -> None:
    if requests_cache.is_installed():
        return

    requests_cache.install_cache(
        cache_name="scrape_wiki_snp",
        use_cache_dir=True,
        cache_control=True,
        allowable_methods=["GET"],
        allowable_codes=[200, 400],
        match_headers=True,
        stale_if_error=True,
    )


def download(url: str) -> str:
    """
    Download url as a string.

    :param url: url to download.
    :return: content.
    """
    _install_cache()

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text
