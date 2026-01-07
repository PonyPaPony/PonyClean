from pathlib import Path
from .paths import get_clean_paths

DEFAULT_RULES = {
    "files": [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "*.pyc",
        ".coverage",
        ".ponyinit",
        ".benchmarks",
    ]
}

PROTECTED_DIRS = {
    "venv",
    ".venv",
    ".git",
    ".ponyclean",
    "__pypackages__",
}

def render_toml(data: dict) -> str:
    lines = []
    for key, values in data.items():
        lines.append(f"{key} = [")
        for v in values:
            lines.append(f'    "{v}",')
        lines.append("]")
        lines.append("")
    return "\n".join(lines)

def init_config_files(base_dir: Path) -> bool:
    clean_path, ignore_path = get_clean_paths(base_dir)
    config_dir = clean_path.parent

    created = False

    if not config_dir.exists():
        config_dir.mkdir(parents=True)
        created = True

    if not clean_path.exists():
        clean_path.write_text(
            render_toml(DEFAULT_RULES),
            encoding="utf-8"
        )
        created = True

    if not ignore_path.exists():
        ignore_path.touch()
        created = True

    return created
