import asyncio

from AsyncRates.services.api_client import ApiClient
from AsyncRates.services.cache_manager import CacheManager
from AsyncRates.services.rate_manager import RateManager


async def _run_async():
    client = ApiClient()
    cache = CacheManager()
    manager = RateManager(api_client=client, cache_manager=cache)
    return await manager.get_rates()


def run(print_result=True):
    report = asyncio.run(_run_async())
    if print_result:
        print(report)
    return report