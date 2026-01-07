import asyncio

from AsyncRates.services.api_client import ApiClient
from AsyncRates.services.cache_manager import CacheManager
from AsyncRates.services.rate_manager import RateManager
from AsyncRates.app_models.reports import RatesReport

async def _run_async() -> RatesReport:
    client = ApiClient()
    cache = CacheManager()
    manager = RateManager(api_client=client, cache_manager=cache)
    return await manager.get_rates()

async def run_async(print_result=True) -> RatesReport:
    """Async-точка входа. Возвращает RatesReport."""
    report = await _run_async()
    if print_result:
        print(report)
    return report


def run(print_result=True) -> RatesReport:
    """Sync-точка входа (CLI, скрипты)."""
    return asyncio.run(run_async(print_result))
