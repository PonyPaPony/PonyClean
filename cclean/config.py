import tomllib
from pathlib import Path
from .paths import get_clean_paths

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
    clean_default, clean_user = get_clean_paths(base_dir)

    if user := load_toml_if_valid(clean_user):
        return user

    return load_toml_if_valid(clean_default) or {}