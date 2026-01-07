from cclean.init import init_config_files
from cclean.paths import get_clean_paths


def test_init_creates_config(tmp_path):
    created = init_config_files(tmp_path)

    clean_path, ignore_path = get_clean_paths(tmp_path)

    assert created is True
    assert clean_path.exists()
    assert ignore_path.exists()
    assert "files" in clean_path.read_text()


def test_init_does_not_overwrite_existing(tmp_path):
    clean_ignore, clean_rules = get_clean_paths(tmp_path)

    clean_rules.parent.mkdir(parents=True, exist_ok=True)
    clean_rules.write_text("keep")
    clean_ignore.write_text("user")

    created = init_config_files(tmp_path)

    assert created is False
    assert clean_rules.read_text() == "keep"
    assert clean_ignore.read_text() == "user"
