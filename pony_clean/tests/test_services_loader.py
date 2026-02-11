import pytest
from pony_clean.services.loader import load_user_rules, load_protected_rules, load_toml_if_valid
from pony_clean.errors.exceptions import PonyServError
from pony_clean.config.config_data import DEFAULT_RULES


def test_load_toml_if_valid_success(tmp_path):
    toml_file = tmp_path / "config.toml"
    toml_file.write_text("files = ['build', 'dist']")

    result = load_toml_if_valid(toml_file)

    assert result == {"files": ["build", "dist"]}


def test_load_toml_if_valid_invalid_toml(tmp_path):
    toml_file = tmp_path / "config.toml"
    toml_file.write_text("invalid toml {]")

    with pytest.raises(PonyServError, match="Invalid TOML format"):
        load_toml_if_valid(toml_file)


def test_load_user_rules_returns_defaults_when_file_missing(tmp_path):
    """Если файла нет, возвращаются DEFAULT_RULES"""
    result = load_user_rules(tmp_path)

    assert result == DEFAULT_RULES

def test_load_user_rules_returns_defaults_when_toml_empty(tmp_path):
    """Если TOML пустой, возвращаются DEFAULT_RULES"""
    config_dir = tmp_path / ".ponyclean"
    config_dir.mkdir()
    toml_file = config_dir / "clean.toml"
    toml_file.write_text("# Just a comment")

    result = load_user_rules(tmp_path)

    assert result == DEFAULT_RULES

def test_load_user_rules_loads_toml(tmp_path):
    """Если есть валидный TOML, он загружается"""
    config_dir = tmp_path / ".ponyclean"
    config_dir.mkdir()
    toml_file = config_dir / "clean.toml"
    toml_file.write_text("files = ['build']")

    result = load_user_rules(tmp_path)

    assert result == {"files": ["build"]}

def test_load_protected_rules_returns_empty_when_file_missing(tmp_path):
    """Если файла нет, возвращается пустое множество"""
    result = load_protected_rules(tmp_path)

    assert result == set()

def test_load_protected_rules_returns_empty_when_toml_empty(tmp_path):
    """Если TOML пустой, возвращается пустое множество"""
    config_dir = tmp_path / ".ponyclean"
    config_dir.mkdir()
    toml_file = config_dir / "protected.toml"
    toml_file.write_text("# Just a comment")

    result = load_protected_rules(tmp_path)

    assert result == set()

def test_load_toml_if_valid_empty_dict(tmp_path):
    """TOML с пустым словарем эквивалентен отсутствию конфига"""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text("# Just a comment\n")

    result = load_toml_if_valid(toml_file)

    assert result is None

def test_load_protected_rules_loads_toml(tmp_path):
    """Если есть защищенные пути, они загружаются"""
    config_dir = tmp_path / ".ponyclean"
    config_dir.mkdir()
    toml_file = config_dir / "protected.toml"
    toml_file.write_text("paths = ['build', 'dist']")

    result = load_protected_rules(tmp_path)

    assert result == {"build", "dist"}
