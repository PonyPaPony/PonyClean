import fnmatch
from pathlib import Path
from .paths import BASE_DIR
from .config import load_clean_config

def collect_clean_targets() -> list[Path]:
    config = load_clean_config()
    patterns = [p for p in config.get("files", []) if isinstance(p, str)]

    found = set()

    for path in BASE_DIR.rglob("*"):
        for pattern in patterns:
            if fnmatch.fnmatch(path.name, pattern):
                found.add(path)
                break

            if path.is_dir() and path.name == pattern:
                found.add(path)
                break

    found = prune_nested_paths(found)
    return found

def prune_nested_paths(paths: set[Path]) -> list[Path]:
    result = set(paths)

    for path in paths:
        for parent in path.parents:
            if parent in result:
                result.discard(path)
                break

    return list(result)