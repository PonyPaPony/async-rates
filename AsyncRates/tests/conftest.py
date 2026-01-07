import pytest
from unittest.mock import AsyncMock, MagicMock
from pathlib import Path
from AsyncRates.services.rate_manager import RateManager
from AsyncRates.services.cache_manager import CacheManager
from AsyncRates.services.api_client import ApiClient
from AsyncRates.utils.validators import Validators

@pytest.fixture
def client():
    return ApiClient()

@pytest.fixture
def validator():
    return Validators()

@pytest.fixture
def api():
    return AsyncMock()

@pytest.fixture
def cache(tmp_path: Path):
    temp_file = tmp_path / "test_rates.json"
    return CacheManager(path=temp_file)

@pytest.fixture
def cache_without_tmp():
    return MagicMock()

@pytest.fixture
def session():
    session = MagicMock()
    response = AsyncMock()
    response.status = 200
    response.raise_for_status = MagicMock()
    response.json.return_value = {"rates": {"EUR": 0.85, "GBP": 0.75}}
    response.text.return_value = "{}"

    context_manager = MagicMock()
    context_manager.__aenter__.return_value = response
    context_manager.__aexit__.return_value = None

    session.get.return_value = context_manager

    return session

@pytest.fixture
def rm(api, cache_without_tmp):
    return RateManager(api, cache_without_tmp)