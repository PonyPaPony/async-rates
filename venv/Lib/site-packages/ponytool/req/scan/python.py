import sys
from pathlib import Path


def get_python() -> dict:
    python = Path(sys.executable)

    if sys.prefix != sys.base_prefix:
        return {
            "python": python,
            "venv": Path(sys.prefix),
        }

    return {
        "python": python,
        "venv": None,
    }