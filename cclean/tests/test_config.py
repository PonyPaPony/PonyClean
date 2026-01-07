import cclean.config as config
from cclean.paths import get_clean_paths
from cclean.config import load_clean_config


def test_load_toml_if_valid_valid(tmp_path):
    path = tmp_path / "a.toml"
    path.write_text('files = ["x"]')

    result = config.load_toml_if_valid(path)

    assert result == {"files": ["x"]}


def test_load_toml_if_valid_empty(tmp_path):
    path = tmp_path / "empty.toml"
    path.touch()

    assert config.load_toml_if_valid(path) is None


def test_load_clean_config_uses_clean_toml(tmp_path):
    clean_path, ignore_path = get_clean_paths(tmp_path)

    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path.write_text('files = ["user"]')

    result = load_clean_config(tmp_path)

    assert result == {"files": ["user"]}
