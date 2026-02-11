import shutil
from pathlib import Path
from pony_clean.services.discovery import discover_targets
from pony_clean.config.config_data import PROTECTED_DIRS
from pony_clean.core.validators import check_protected, check_dangerous

"""
API layer: execution boundary.

This module is allowed to perform controlled filesystem side-effects
and enforce safety guarantees (guard/remove).

Business rules and discovery are delegated to services and core.
"""

def guard(path: Path, base_path: Path):
    real_base = base_path.resolve()
    real_path = path.resolve()

    check_protected(real_base, PROTECTED_DIRS)
    check_dangerous(real_base, real_path)

def remove(path: Path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()

def run_clean(base_path: Path, dry_run: bool = False):
    targets = discover_targets(base_path)

    if not targets:
        return []

    cleaned = []

    for target in targets:
        if not target.exists():
            continue

        guard(target, base_path)

        if not dry_run:
            remove(target)

        cleaned.append(target)

    return cleaned