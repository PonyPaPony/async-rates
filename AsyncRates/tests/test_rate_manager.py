import pytest
from AsyncRates.app_models.reports import RatesReport
from AsyncRates.utils.app_exceptions import ARateError


def setup_cache_status(cache, is_old: bool):
    """Помощник для настройки статуса кэша."""
    cache.is_cache_old.return_value = is_old

@pytest.mark.asyncio
async def test_get_rates_from_fresh_cache(rm, cache_without_tmp, api):
    """Тест 4.1: Кэш свежий -> данные берутся из кэша, API не вызывается."""
    setup_cache_status(cache_without_tmp, False)
    cache_without_tmp.get_data.return_value = {
        "currency": {'EUR': 0.9},
        'crypto': {'BTC': 50000}
    }

    result = await rm.get_rates()

    assert isinstance(result, RatesReport)
    assert result.currency == {'EUR': 0.9}
    api.fetch_all.assert_not_called()

@pytest.mark.asyncio
async def test_get_rates_from_api_success(rm, cache_without_tmp, api):
    """Тест 4.2: Кэш старый -> идем в API -> сохраняем в кэш."""
    setup_cache_status(cache_without_tmp, True)
    fake_report = RatesReport(currency={'USD': 1}, crypto={'BTC': 60000})
    api.fetch_all.return_value = fake_report

    result = await rm.get_rates()

    assert result.crypto['BTC'] == 60000
    api.fetch_all.assert_called_once()
    cache_without_tmp.save_cache.assert_called_once()

@pytest.mark.asyncio
async def test_get_rates_fallback_on_api_error(rm, cache_without_tmp, api):
    """Тест 4.3: Fallback -> API упал, но вернули данные из старого кэша."""
    setup_cache_status(cache_without_tmp, True)
    api.fetch_all.side_effect = ARateError("Connection Lost")

    cache_without_tmp.get_data.return_value = {
        "currency": {"EUR": 0.5},
        "crypto": {"BTC": 10000}
    }

    result = await rm.get_rates()

    assert result.currency == {"EUR": 0.5}
    assert result.crypto['BTC'] == 10000

@pytest.mark.asyncio
async def test_get_rates_critical_failure(rm, cache_without_tmp, api):
    """Тест 4.4: Критическая ошибка -> API упал и кэш пуст."""
    setup_cache_status(cache_without_tmp, True)
    api.fetch_all.side_effect = ARateError("API Down")

    cache_without_tmp.get_data.return_value = None

    with pytest.raises(ARateError, match="Rates unavailable"):
        await rm.get_rates()