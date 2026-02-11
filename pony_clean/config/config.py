from pathlib import Path
from pony_clean.core.rules import render_toml
from pony_clean.config.config_data import DEFAULT_RULES

def get_rules():
    render_toml(DEFAULT_RULES)

def get_paths(base_path: Path):
    return (
        base_path / ".ponyclean/clean.toml",
        base_path / ".ponyclean/protected.toml",
    )