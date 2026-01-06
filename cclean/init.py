from .paths import BASE_DIR, CLEAN_DIR, USER_DIR

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

def ensure_config_files():
    data_dir = CLEAN_DIR.parent
    data_dir.mkdir(parents=True, exist_ok=True)

    if not CLEAN_DIR.exists():
        CLEAN_DIR.write_text(DEFAULT_CONTENT, encoding="utf-8")

    if not USER_DIR.exists():
        USER_DIR.touch()