import fnmatch
from pathlib import Path

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