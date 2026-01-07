import json
from datetime import datetime, timedelta
from pathlib import Path
from AsyncRates import app_config

test_case = {"test": 123}

def file_op(file_path: Path, mode='w', data=None):
    """Вспомогательная функция для работы с файлами в тестах."""
    if mode == 'w':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    elif mode == 'r':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif mode == 'corrupt':
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("{invalid_json...}")

def test_save_cache(cache):
    """Тест 2.1: Проверка записи данных в файл."""
    test_data = {"currency": {"EUR": 1.0}}
    cache.save_cache(test_data)

    saved_json = file_op(cache.path, 'r')

    assert saved_json[app_config.CACHE_KEY_DATA] == test_data
    assert app_config.CACHE_KEY_TIMESTAMP in saved_json

def test_load_cache_fresh(cache):
    """Тест 2.2: Загрузка свежего кэша."""
    fresh_data = {
        app_config.CACHE_KEY_TIMESTAMP: datetime.now().strftime(app_config.DATE_FORMAT),
        app_config.CACHE_KEY_DATA: test_case
    }

    file_op(cache.path, 'w', fresh_data)

    assert cache.is_cache_old() is False
    assert cache.get_data() == test_case

def test_load_cache_old(cache):
    """Тест 2.3: Загрузка устаревшего кэша."""
    old_time = datetime.now() - timedelta(minutes=100)

    old_data = {
        app_config.CACHE_KEY_TIMESTAMP: old_time.strftime(app_config.DATE_FORMAT),
        app_config.CACHE_KEY_DATA: test_case
    }

    file_op(cache.path, 'w', old_data)

    assert cache.is_cache_old(max_age_minutes=30) is True
    assert cache.get_data() == test_case

def test_corrupted_cache(cache):
    """Тест 2.4: Обработка битого файла."""
    file_op(cache.path, 'corrupt')

    assert cache.get_data() is None

    files_in_dir = list(cache.path.parent.iterdir())
    assert len(files_in_dir) >= 2
    assert any(".bak_" in f.name for f in files_in_dir)