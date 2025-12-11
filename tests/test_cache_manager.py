import json
import pytest
from datetime import datetime, timedelta
from services.cache_manager import CacheManager
from pathlib import Path
import app_config


@pytest.fixture
def cache_manager(tmp_path):
    temp_file = tmp_path / "test_rates.json"
    return CacheManager(path=str(temp_file))


def test_save_cache(cache_manager):
    """Тест 3.1: Проверка записи данных в файл."""
    test_data = {"currency": {"EUR": 1.0}}

    cache_manager.save_cache(test_data)

    with open(cache_manager.path, "r", encoding='utf-8') as f:
        saved_json = json.load(f)

    assert saved_json[app_config.CACHE_KEY_DATA] == test_data
    assert app_config.CACHE_KEY_TIMESTAMP in saved_json


def test_load_cache_fresh(cache_manager):
    """Тест 3.2: Загрузка свежего кэша."""
    fresh_data = {
        app_config.CACHE_KEY_TIMESTAMP: datetime.now().strftime(app_config.DATE_FORMAT),
        app_config.CACHE_KEY_DATA: {"test": 123}
    }

    with open(cache_manager.path, "w", encoding='utf-8') as f:
        json.dump(fresh_data, f)

    assert cache_manager.is_cache_old() is False
    assert cache_manager.get_data() == {"test": 123}


def test_load_cach_old(cache_manager):
    """Тест 3.3: Загрузка устаревшего кэша."""
    old_time = datetime.now() - timedelta(minutes=100)

    old_data = {
        app_config.CACHE_KEY_TIMESTAMP: old_time.strftime(app_config.DATE_FORMAT),
        app_config.CACHE_KEY_DATA: {"test": 123}
    }

    with open(cache_manager.path, "w", encoding='utf-8') as f:
        json.dump(old_data, f)

    assert cache_manager.is_cache_old(max_age_minutes=30) is True
    assert cache_manager.get_data() == {'test': 123}

def test_corrupted_cache(cache_manager):
    """Тест 3.4: Обработка битого файла."""
    with open(cache_manager.path, "w", encoding='utf-8') as f:
        f.write("{invalid_json...}")

    data = cache_manager.get_data()

    assert data is None

    path_obj = Path(cache_manager.path)

    files_in_dir = list(path_obj.parent.iterdir())

    assert len(files_in_dir) >= 2

    assert any(".bak_" in f.name for f in files_in_dir)
