"""
Service that calls an external API (Frankfurter - free, no API key needed).
This is the pattern to learn: isolate the external call in its own class,
so main.py / routes stay thin and this class can be mocked in tests.
"""

import httpx

from src.calculator import multiply

FRANKFURTER_BASE_URL = "https://api.frankfurter.dev/v1"


class ExchangeRateError(Exception):
    """Raised when the external API call fails or returns bad data."""


class ExchangeRateService:
    def __init__(
        self, base_url: str = FRANKFURTER_BASE_URL, timeout: float = 5.0
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout

    async def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Fetch the current exchange rate from_currency -> to_currency."""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        params = {"base": from_currency, "symbols": to_currency}
        url = f"{self._base_url}/latest"

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ExchangeRateError(
                f"Failed to reach exchange rate API: {exc}"
            ) from exc

        try:
            return float(data["rates"][to_currency])
        except (KeyError, ValueError) as exc:
            raise ExchangeRateError(
                f"Unexpected response shape or unknown currency: {to_currency}"
            ) from exc

    async def convert(
        self, amount: float, from_currency: str, to_currency: str
    ) -> float:
        """Convert `amount` from one currency to another, reusing our own multiply()."""
        rate = await self.get_rate(from_currency, to_currency)
        return multiply(amount, rate)
