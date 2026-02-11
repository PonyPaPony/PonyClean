from pathlib import Path
from pony_clean.errors.exceptions import PonyAPIError


def check_protected(path: Path, protected: set[str]):
    if path.parts and path.parts[0] in protected:
        raise PonyAPIError(f"Cannot clean protected directory: {path}")

def check_dangerous(real_base: Path, real_path: Path):
    if real_base not in real_path.parents and real_path != real_base:
        raise PonyAPIError(f"Dangerous path {real_base}")
