from pathlib import Path
import tomllib


def load_toml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def merge_dicts(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(value, dict)
        ):
            merge_dicts(base[key], value)
        else:
            base[key] = value
    return base


def load_config() -> dict:
    root = Path(__file__).resolve().parent.parent

    defaults = load_toml(root / "config" / "defaults.toml")
    user = load_toml(root / "config" / "user.toml")

    return merge_dicts(defaults, user)
