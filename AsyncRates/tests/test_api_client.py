import pytest
import aiohttp
from unittest.mock import patch, AsyncMock, MagicMock
from AsyncRates import app_config
from AsyncRates.utils.app_exceptions import ApiError


@pytest.mark.asyncio
async def test_fetch_currency_rates_success(client, session):
    """Тест 1.1: Успешное получение курсов валют."""
    result = await client.fetch_currency_rates(session)

    assert result == {"EUR": 0.85, "GBP": 0.75}

    session.get.assert_called_once_with(
        app_config.CURRENCY_API_URL,
        timeout=app_config.AIOHTTP_TIMEOUT,
        params={
            app_config.CURRENCY_PARAM_FROM: app_config.BASE_CURRENCY,
            app_config.CURRENCY_PARAM_TO: ",".join(app_config.SUPPORTED_CURRENCIES)
        })

@pytest.mark.asyncio
async def test_fetch_currency_rates_error(client, session):
    """Тест 1.2: Ошибка при получении курсов валют."""
    mock_response = session.get.return_value.__aenter__.return_value
    mock_response.status = 404

    mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError(
        request_info=MagicMock(), history=(), status=404
    )

    with pytest.raises(ApiError) as exc_info:
        await client.fetch_currency_rates(session)

    assert exc_info.value.status == 404
    assert exc_info.value.retryable is False
    assert session.get.call_count == 1

@pytest.mark.asyncio
async def test_fetch_crypto_rates_success(client, session):
    """Тест 1.3: Успешное получение крипты (проверка маппинга)."""
    crypto_response = {
        'bitcoin': {'usd': 50000},
        'ethereum': {'usd': 3000},
        'dogecoin': {'usd': 0.1}
    }

    session.get.return_value.__aenter__.return_value.json.return_value = crypto_response

    result = await client.fetch_crypto_rates(session)

    assert result['BTC'] == 50000
    assert result['ETH'] == 3000
    assert result['DOGE'] == pytest.approx(0.1)

@pytest.mark.asyncio
async def test_fetch_crypto_rates_error(client, session):
    """Тест 1.4: Ошибка при получении курса крипты."""
    mock_response = session.get.return_value.__aenter__.return_value
    mock_response.status = 404

    mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError(
        request_info=MagicMock(), history=(), status=404
    )

    with pytest.raises(ApiError) as exc_info:
        await client.fetch_crypto_rates(session)

    assert exc_info.value.status == 404

@pytest.mark.asyncio
async def test_fetch_retry_logic(client, session):
    """Тест 1.5: Проверка механизма ретраев (1 ошибка -> успех)."""
    mock_response_ok = AsyncMock()
    mock_response_ok.status = 200
    mock_response_ok.json.return_value = {"rates": {"EUR": 0.9}}
    mock_response_ok.text.return_value = "{}"

    session.get.return_value.__aenter__.side_effect = [
        aiohttp.ClientError("Server temp error"),
        mock_response_ok
    ]


    with patch("asyncio.sleep", new_callable=AsyncMock):
        result = await client.fetch_currency_rates(session)

    assert result == {"EUR": 0.9}
    assert session.get.call_count == 2