import cclean.config as config
from cclean.paths import get_clean_paths


def test_load_toml_if_valid_valid(tmp_path):
    path = tmp_path / "a.toml"
    path.write_text('files = ["x"]')

    result = config.load_toml_if_valid(path)

    assert result == {"files": ["x"]}


def test_load_toml_if_valid_empty(tmp_path):
    path = tmp_path / "empty.toml"
    path.touch()

    assert config.load_toml_if_valid(path) is None


def test_load_clean_config_user_priority(tmp_path):
    clean_default, clean_user = get_clean_paths(tmp_path)

    clean_default.parent.mkdir(parents=True, exist_ok=True)
    clean_default.write_text('files = ["default"]')
    clean_user.write_text('files = ["user"]')

    result = config.load_clean_config(tmp_path)

    assert result == {"files": ["user"]}
