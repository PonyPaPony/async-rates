import pytest
from AsyncRates.utils.app_exceptions import ARateError

def test_validator_data_valid(validator):
    """Тест 3.1: Проверка валидности данных."""
    validator.check_empty_currency({'USD': 100.0})
    validator.check_empty_currency({'EUR': 100.0})

def test_validator_data_empty(validator):
    """Тест 3.2: Проверка на пустые данные."""
    with pytest.raises(ARateError, match="Currency API returned empty rates"):
        validator.check_empty_currency({})

def test_validator_data_none(validator):
    """Тест 3.3: Проверка на некорректные данные."""
    with pytest.raises(ARateError, match="Currency API returned empty rates"):
        validator.check_empty_currency(None)