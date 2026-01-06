import shutil
from pathlib import Path
from .paths import BASE_DIR
from .resolver import collect_clean_targets

def guard_clean(obj: Path):
    real_base = BASE_DIR.resolve()
    real_obj = obj.resolve()

    if real_base not in real_obj.parents and real_obj != real_base:
        raise RuntimeError(f"Опасный путь: {obj}")

def remove_obj(obj: Path):
    if obj.is_file():
        obj.unlink()
    elif obj.is_dir():
        shutil.rmtree(obj)

def run_clean(dry_run: bool = False):
    targets = collect_clean_targets()

    if not targets:
        return []

    cleaned = []
    for obj in targets:
        if not obj.exists():
            continue

        guard_clean(obj)

        if not dry_run:
            remove_obj(obj)

        cleaned.append(obj)

    return cleaned
