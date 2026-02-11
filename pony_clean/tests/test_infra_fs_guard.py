import pytest
from pony_clean.errors.exceptions import PonyValidationError
from pony_clean.infra.fs_guard import ensure_directory, ensure_marker_file, ensure_rules_file, validate_existing_path

def test_ensure_directory(tmp_path):
    path = tmp_path / "my_dir"

    result = ensure_directory(path)

    assert result is True
    assert path.is_dir()

    result2 = ensure_directory(path)

    assert result2 is False
    assert path.is_dir()

def test_ensure_rules_file(tmp_path):
    content = "test rules content"
    path = tmp_path / "clean.toml"

    result = ensure_rules_file(path, content)

    assert result is True
    assert path.is_file()
    assert path.read_text(encoding='utf-8') == content

    result2 = ensure_rules_file(path, content)

    assert result2 is False
    assert path.is_file()

def test_ensure_marker_file(tmp_path):
    path = tmp_path / "protected.txt"

    result = ensure_marker_file(path)

    assert result is True
    assert path.is_file()

    result2 = ensure_marker_file(path)

    assert result2 is False
    assert path.is_file()

def test_validate_existing_path_success(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text('test')

    validate_existing_path(path)

def test_validate_existing_path_nonexistent(tmp_path):
    """Несуществующий файл должен вызвать ошибку"""
    path = tmp_path / "test_failure.txt"

    with pytest.raises(PonyValidationError, match="does not exist"):  # ← Обновлено
        validate_existing_path(path)

def test_validate_existing_path_directory(tmp_path):
    """Директория (не файл) должна вызвать ошибку"""
    path = tmp_path / "some_dir"
    path.mkdir()

    with pytest.raises(PonyValidationError, match="is not a file"):
        validate_existing_path(path)