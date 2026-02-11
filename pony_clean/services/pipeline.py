from pathlib import Path
from pony_clean.config.config import get_paths, get_rules
from pony_clean.infra.fs_guard import ensure_directory, ensure_rules_file, ensure_marker_file

def prepare_workspace(base_path: Path) -> bool:
    clean_path, protected_path = get_paths(base_path)
    config = clean_path.parent

    created = False

    created |= ensure_directory(config)

    rules = get_rules()
    if rules is None:
        rules = ""
    created |= ensure_rules_file(clean_path, rules)
    created |= ensure_marker_file(protected_path)

    return created