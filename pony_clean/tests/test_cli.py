from unittest.mock import patch
from pony_clean.api.cli import remove, run_clean, guard


def test_remove_file(tmp_path):
    file = tmp_path / "a.txt"
    file.touch()
    remove(file)
    assert not file.exists()

def test_remove_dir(tmp_path):
    dir_path = tmp_path / "dirp"
    dir_path.mkdir()
    (dir_path / "file.txt").touch()
    remove(dir_path)
    assert not dir_path.exists()

def test_remove_nonexistent_path(tmp_path):
    path = tmp_path / "nonexistent"

    remove(path)

@patch("pony_clean.api.cli.discover_targets")
def test_run_clean_dry_run(mock_discover, tmp_path):
    target = tmp_path / 'build'
    target.mkdir()
    mock_discover.return_value = [target]

    cleaned = run_clean(tmp_path, dry_run=True)

    assert target.exists()
    assert cleaned == [target]

@patch("pony_clean.api.cli.discover_targets")
def test_run_clean_removes_files(mock_discover, tmp_path):
    target = tmp_path / 'build'
    target.mkdir()
    mock_discover.return_value = [target]

    cleaned = run_clean(tmp_path, dry_run=False)

    assert not target.exists()  # Файл удален
    assert cleaned == [target]

@patch("pony_clean.api.cli.discover_targets")
def test_run_clean_empty_targets(mock_discover, tmp_path):
    mock_discover.return_value = []

    cleaned = run_clean(tmp_path, dry_run=False)

    assert cleaned == []

@patch("pony_clean.api.cli.discover_targets")
def test_run_clean_skips_nonexistent_targets(mock_discover, tmp_path):
    existing = tmp_path / 'build'
    existing.mkdir()
    non = tmp_path / 'nonexistent'

    mock_discover.return_value = [existing, non]

    cleaned = run_clean(tmp_path, dry_run=False)

    assert not existing.exists()
    assert existing in cleaned
    assert non not in cleaned
    assert len(cleaned) == 1

@patch("pony_clean.api.cli.check_protected")
@patch("pony_clean.api.cli.check_dangerous")
def test_guard_called(mock_check_dangerous, mock_check_protected, tmp_path):
    from pony_clean.config.config_data import PROTECTED_DIRS
    path = tmp_path / "a"
    base = tmp_path / "b"

    guard(path, base)

    mock_check_protected.assert_called_once_with(base.resolve(), PROTECTED_DIRS)
    mock_check_dangerous.assert_called_once_with(base.resolve(), path.resolve())