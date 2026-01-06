from cclean.init import ensure_config_files
from cclean.paths import get_clean_paths


def test_ensure_config_files_creates(tmp_path):
    ensure_config_files(tmp_path)

    clean_default, clean_user = get_clean_paths(tmp_path)

    assert clean_default.exists()
    assert clean_user.exists()
    assert "files" in clean_default.read_text()


def test_ensure_config_files_no_overwrite(tmp_path):
    clean_default, clean_user = get_clean_paths(tmp_path)

    clean_default.parent.mkdir(parents=True, exist_ok=True)
    clean_default.write_text("keep")
    clean_user.write_text("user")

    ensure_config_files(tmp_path)

    assert clean_default.read_text() == "keep"
    assert clean_user.read_text() == "user"
