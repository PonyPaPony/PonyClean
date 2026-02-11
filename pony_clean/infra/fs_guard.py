from pathlib import Path
from pony_clean.errors.exceptions import PonyValidationError


def ensure_directory(config: Path) -> bool:
    if not config.exists():
        config.mkdir(parents=True)
        return True
    return False

def ensure_rules_file(clean_path: Path, content: str) -> bool:
    if not clean_path.exists():
        clean_path.write_text(
            content,
            encoding="utf-8"
        )
        return True
    return False

def ensure_marker_file(protected_path: Path) -> bool:
    if not protected_path.exists():
        protected_path.touch()
        return True
    return False

def validate_existing_path(path: Path) -> None:
    if not path.exists():
        raise PonyValidationError(f"{path} does not exist")
    if not path.is_file():
        raise PonyValidationError(f"{path} is not a file")