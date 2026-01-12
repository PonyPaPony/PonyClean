import tomllib
from pathlib import Path
from .paths import get_clean_paths
from .init import DEFAULT_RULES

def load_toml_if_valid(path: Path) -> dict | None:
    if not path.exists() or path.stat().st_size == 0:
        return None

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError:
        return None

    return data if data else None


def load_clean_config(base_dir: Path) -> dict:
    clean_path, _ = get_clean_paths(base_dir)

    user = load_toml_if_valid(clean_path)
    return user if user is not None else DEFAULT_RULES


def load_ignore_config(base_dir: Path) -> set[str]:
    _, ignore_path = get_clean_paths(base_dir)

    data = load_toml_if_valid(ignore_path)
    return set(data.get("paths", [])) if data else set()