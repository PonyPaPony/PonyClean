import os
from pathlib import Path
from pony_clean.config.config_data import PROTECTED_DIRS
from pony_clean.services.loader import load_user_rules, load_protected_rules
from pony_clean.core.target_resolver import prune_nested_paths
from pony_clean.services.filters import collect_allowed_directories, collect_allowed_files


def discover_targets(base_path: Path) -> list[Path]:
    config = load_user_rules(base_path)
    protected_paths = load_protected_rules(base_path)

    patterns = [p for p in config.get("files", []) if isinstance(p, str)]

    if not patterns:
        return []

    found: set[Path] = set()

    for root, dirs, files in os.walk(base_path):
        root_path = Path(root)

        dirs[:] = [d for d in dirs if d not in PROTECTED_DIRS]

        collect_allowed_directories(root_path, protected_paths, dirs, patterns, found)
        collect_allowed_files(root_path, protected_paths, files, patterns, found)

    return prune_nested_paths(found)