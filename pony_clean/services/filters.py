from pathlib import Path
from pony_clean.core.target_resolver import matches

def collect_allowed_directories(
        root: Path,
        protected_paths: set[str],
        dirs: list[str],
        patterns: list[str],
        found: set[Path],
) -> None:
    for d in dirs:
        if d in protected_paths:
            continue
        path = root / d
        if matches(path, patterns):
            found.add(path)

def collect_allowed_files(
        root: Path,
        protected_paths: set[str],
        files: list[str],
        patterns: list[str],
        found: set[Path],
) -> None:
    for file in files:
        if file in protected_paths:
            continue
        path = root / file
        if matches(path, patterns):
            found.add(path)