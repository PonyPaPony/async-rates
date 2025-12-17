import pytest
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
from AsyncRates.services.api_client import ApiClient
from AsyncRates import app_config

pytest_plugins = ("pytest_asyncio")

@pytest.fixture
def client():
    return ApiClient()


@pytest.fixture()
def mock_session():
    """
    Создает фейковую сессию, которая имитирует поведение aiohttp.
    Самое сложное тут - имитировать 'async with session.get() as response'.
    """
    session = MagicMock()

    # Создаем мок ответа (Response)
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}

    # Создаем мок контекстного менеджера (то, что возвращает session.get())
    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__.return_value = mock_response
    mock_context_manager.__aexit__.return_value = None

    session.get.return_value = mock_context_manager

    return session

@pytest.mark.asyncio
async def test_fetch_currency_rates_success(client, mock_session):
    """Тест 2.1: Успешное получение курсов валют."""
    result = await client.fetch_currency_rates(mock_session)

    assert result == {"EUR": 0.85, "GBP": 0.75}

    mock_session.get.assert_called_once_with(
        app_config.CURRENCY_API_URL,
        params={
        app_config.CURRENCY_PARAM_FROM: app_config.BASE_CURRENCY,
        app_config.CURRENCY_PARAM_TO: app_config.SUPPORTED_CURRENCIES
        })

@pytest.mark.asyncio
async def test_fetch_currency_rates_error(client, mock_session):
    """Тест 2.2: Успешное получение крипты (проверка маппинга)."""
    crypto_response = {
        'bitcoin': {'usd': 50000},
        'ethereum': {'usd': 3000},
        'dogecoin': {'usd': 0.1}
    }

    mock_response = mock_session.get.return_value.__aenter__.return_value
    mock_response.json.return_value = crypto_response

    result = await client.fetch_crypto_rates(mock_session)

    assert result['BTC'] == 50000
    assert result['ETH'] == 3000
    assert result['DOGE'] == pytest.approx(0.1)

@pytest.mark.asyncio
async def test_fetch_retry_logic(client, mock_session):
    """Тест 2.3: Проверка механизма ретраев (2 ошибки -> успех)."""

    mock_context = mock_session.get.return_value

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"rates": {"EUR": 0.9}}

    mock_context.__aenter__.side_effect = [
        aiohttp.ClientError("Network error"),
        mock_response
    ]

    with patch("asyncio.sleep", new_callable=AsyncMock):
        result = await client.fetch_currency_rates(mock_session)

    assert  result == {"EUR": 0.9}

    assert mock_session.get.call_count == 2