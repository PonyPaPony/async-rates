import pytest
from AsyncRates.utils import Validators


@pytest.fixture
def validators():
    return Validators()


def test_validator_data_valid(validators):
    validators.check_empty_currency({'USD': 100.0})
    validators.check_empty_currency({'EUR': 100.0})

def test_validator_data_empty(validators):
    with pytest.raises(ValueError):
        validators.check_empty_currency({})

def test_validator_data_none(validators):
    with pytest.raises(ValueError):
        validators.check_empty_currency(None)

