import tomllib
from pathlib import Path
from pony_clean.config.config import get_paths
from pony_clean.config.config_data import DEFAULT_RULES
from pony_clean.infra.fs_guard import validate_existing_path
from pony_clean.errors.exceptions import PonyServError

def load_toml_if_valid(path: Path) -> dict | None:
    validate_existing_path(path)

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise PonyServError(f"Invalid TOML format in {path}: {e}")

    return data if data else None

def load_user_rules(base_path: Path) -> dict:
    clean_path, _ = get_paths(base_path)

    if not clean_path.exists():
        return DEFAULT_RULES

    user = load_toml_if_valid(clean_path)
    return user if user is not None else DEFAULT_RULES

def load_protected_rules(base_path: Path) -> set[str]:
    _, protected_path = get_paths(base_path)

    if not protected_path.exists():
        return set()

    data = load_toml_if_valid(protected_path)
    return set(data.get("paths", [])) if data else set()