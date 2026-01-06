from pathlib import Path
from .paths import get_clean_paths

DEFAULT_CONTENT = """\
files = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "*.pyc",
    ".coverage",
    ".ponyinit",
    ".benchmarks",
]
"""

def ensure_config_files(base_dir: Path):
    clean_default, clean_user = get_clean_paths(base_dir)
    data_dir = clean_default.parent
    data_dir.mkdir(parents=True, exist_ok=True)

    if not clean_default.exists():
        clean_default.write_text(DEFAULT_CONTENT, encoding="utf-8")

    if not clean_user.exists():
        clean_user.touch()