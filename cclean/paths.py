from pathlib import Path

def get_base_dir(root: str | None = None) -> Path:
    return Path(root).resolve() if root else Path.cwd().resolve()

def get_clean_paths(base_dir: Path):
    return (
        base_dir / "data/clean_default.toml",
        base_dir / "data/clean_user.toml",
    )