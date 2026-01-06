import cclean.init as init


def test_ensure_config_files_creates_files(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    clean_default = data_dir / "clean_default.toml"
    clean_user = data_dir / "clean_user.toml"

    monkeypatch.setattr(init, "CLEAN_DIR", clean_default)
    monkeypatch.setattr(init, "USER_DIR", clean_user)

    init.ensure_config_files()

    assert data_dir.exists()
    assert clean_default.exists()
    assert clean_user.exists()

    content = clean_default.read_text(encoding="utf-8")
    assert "files" in content


def test_ensure_config_files_does_not_overwrite_existing(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    clean_default = data_dir / "clean_default.toml"
    clean_user = data_dir / "clean_user.toml"

    clean_default.write_text("files = ['keep_me']\n", encoding="utf-8")
    clean_user.write_text("do not touch", encoding="utf-8")

    monkeypatch.setattr(init, "CLEAN_DIR", clean_default)
    monkeypatch.setattr(init, "USER_DIR", clean_user)

    init.ensure_config_files()

    assert clean_default.read_text(encoding="utf-8") == "files = ['keep_me']\n"
    assert clean_user.read_text(encoding="utf-8") == "do not touch"
