from pathlib import Path
import sys

COMMON_VENV_NAMES = (".venv", "venv", "env")


def find_active_venv() -> Path | None:
    if sys.prefix != sys.base_prefix:
        return Path(sys.prefix)
    return None


def find_local_venv(root: Path) -> Path | None:
    for name in COMMON_VENV_NAMES:
        candidate = root / name
        cfg_file = candidate / "pyvenv.cfg"
        if candidate.exists() and cfg_file.exists():
            return candidate
    return None

def search_parents(start: Path) -> Path | None:
    for parent in [start, *start.parents]:
        for name in ("venv", ".venv"):
            candidate = parent / name
            if (candidate / "pyvenv.cfg").exists():
                return candidate

def find_venv(start: Path | None = None) -> Path | None:
    return (
        find_active_venv()
        or find_local_venv(start or Path.cwd())
        or search_parents(start or Path.cwd())
    )

