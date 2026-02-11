from pathlib import Path

def get_base_path(root: str | None = None) -> Path:
    return Path(root).resolve() if root else Path.cwd().resolve()