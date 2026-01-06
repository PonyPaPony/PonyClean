import tomllib
from pathlib import Path
from .paths import CLEAN_DIR, USER_DIR

def load_toml_if_valid(path: Path) -> dict | None:
    if not path.exists() or path.stat().st_size == 0:
        return None

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError:
        return None

    return data if data else None


def load_clean_config() -> dict:
    if user := load_toml_if_valid(USER_DIR):
        return user

    return load_toml_if_valid(CLEAN_DIR) or {}