import fnmatch
import os
from pathlib import Path
from .config import load_clean_config

def collect_clean_targets(base_dir: Path) -> list[Path]:
    config = load_clean_config(base_dir)
    patterns = [p for p in config.get("files", []) if isinstance(p, str)]

    found: set[Path] = set()

    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)

        dirs[:] = [
            d for d in dirs
            if should_descend(root_path / d, patterns)
        ]

        for d in dirs:
            path = root_path / d
            if matches(path, patterns):
                found.add(path)

        for f in files:
            path = root_path / f
            if matches(path, patterns):
                found.add(path)

    return prune_nested_paths(found)

def matches(path: Path, patterns: list[str]) -> bool:
    is_dir = path.is_dir()
    name = path.name

    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
        if is_dir and name == pattern:
            return True
    return False

def should_descend(path: Path, patterns: list[str]) -> bool:
    for pattern in patterns:
        # glob может матчить глубже
        if "*" in pattern:
            return True
        # директория может быть целью или содержать цель
        if path.name == pattern:
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