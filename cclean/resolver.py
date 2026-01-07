import fnmatch
import os
from pathlib import Path
from .config import load_clean_config, load_ignore_config
from .init import PROTECTED_DIRS

def collect_clean_targets(base_dir: Path) -> list[Path]:
    config = load_clean_config(base_dir)
    ignore_paths = load_ignore_config(base_dir)
    patterns = [p for p in config.get("files", []) if isinstance(p, str)]

    if not patterns:
        return []

    found: set[Path] = set()

    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)

        dirs[:] = [d for d in dirs if d not in PROTECTED_DIRS]

        ensure_dirs_not_ignored(root_path, ignore_paths, dirs, patterns, found)
        ensure_file_not_ignored(root_path, ignore_paths, files, patterns, found)

    return prune_nested_paths(found)

def ensure_dirs_not_ignored(
        root: Path,
        ignore_names: set[str],
        dirs: list[str],
        patterns: list[str],
        found: set[Path]
) -> None:
    for d in dirs:
        if d in ignore_names:
            continue
        path = root / d
        if matches(path, patterns):
            found.add(path)


def ensure_file_not_ignored(
        root: Path,
        ignore_names: set[str],
        files: list[str],
        patterns: list[str],
        found: set[Path]
) -> None:
    for f in files:
        if f in ignore_names:
            continue
        path = root / f
        if matches(path, patterns):
            found.add(path)

def matches(path: Path, patterns: list[str]) -> bool:
    is_dir = path.is_dir()
    name = path.name

    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
        if is_dir and name == pattern:
            return True
    return False

def prune_nested_paths(paths: set[Path]) -> list[Path]:
    result = set(paths)

    for path in paths:
        for parent in path.parents:
            if parent in result:
                result.discard(path)
                break

    return list(result)
