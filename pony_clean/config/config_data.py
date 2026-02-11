DEFAULT_RULES = {
    "files": [
        # Python build artifacts
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".Python",

        # Build directories
        "dist",
        "build",
        "*.egg-info",

        # Testing
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
        "htmlcov",
        ".tox",

        # Project-specific (можно убрать из дефолтов)
        ".ponyinit",
        ".benchmarks",
        ".hypothesis",
    ]
}

PROTECTED_DIRS = {
    "venv",
    ".venv",
    ".git",
    ".ponyclean",
    "__pypackages__",
}