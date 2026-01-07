import shutil
from pathlib import Path
from .resolver import collect_clean_targets
from .init import PROTECTED_DIRS

def guard_clean(obj: Path, base_dir: Path):
    real_base = base_dir.resolve()
    real_obj = obj.resolve()

    if obj.parts and obj.parts[0] in PROTECTED_DIRS:
        raise RuntimeError(f"Refusing to clean protected path: {obj}")

    if real_base not in real_obj.parents and real_obj != real_base:
        raise RuntimeError(f"Опасный путь: {obj}")

def remove_obj(obj: Path):
    if obj.is_file():
        obj.unlink()
    elif obj.is_dir():
        shutil.rmtree(obj)

def run_clean(base_dir: Path, dry_run: bool = False):
    targets = collect_clean_targets(base_dir)

    if not targets:
        return []

    cleaned = []
    for obj in targets:
        if not obj.exists():
            continue

        guard_clean(obj, base_dir)

        if not dry_run:
            remove_obj(obj)

        cleaned.append(obj)

    return cleaned
