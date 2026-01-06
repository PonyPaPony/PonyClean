import cclean.config as config


def test_load_toml_if_valid_missing(tmp_path):
    path = tmp_path / "missing.toml"
    assert config.load_toml_if_valid(path) is None

def test_load_toml_if_valid_empty(tmp_path):
    path = tmp_path / "empty.toml"
    path.touch()
    assert config.load_toml_if_valid(path) is None

def test_load_toml_if_valid_valid(tmp_path):
    path = tmp_path / "valid.toml"
    path.write_text('files = ["__pycache__"]')

    result = config.load_toml_if_valid(path)

    assert result == {"files": ["__pycache__"]}

def test_load_toml_if_valid_invalid(tmp_path):
    path = tmp_path / "broken.toml"
    path.write_text("files = [")

    assert config.load_toml_if_valid(path) is None

def test_load_clean_config_user_priority(tmp_path, monkeypatch):
    user = tmp_path / "user.toml"
    default = tmp_path / "default.toml"

    user.write_text('files = ["user"]')
    default.write_text('files = ["default"]')

    monkeypatch.setattr(config, "USER_DIR", user)
    monkeypatch.setattr(config, "CLEAN_DIR", default)

    result = config.load_clean_config()

    assert result == {"files": ["user"]}
