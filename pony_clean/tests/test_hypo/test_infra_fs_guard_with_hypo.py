from pathlib import Path
from pony_clean.errors.exceptions import PonyValidationError
from pony_clean.infra.fs_guard import ensure_directory, ensure_rules_file, ensure_marker_file, validate_existing_path
from hypothesis import given, strategies as st
import tempfile
import string
import pytest


#* GOAL: Построить стратегию для hypothesis
#- TEST: Тестируемые объекты ensure_directory, ensure_rules_file, ensure_marker_file, validate_existing_path

def is_valid_windows_name(name: str) -> bool:
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3',
                'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    return name.upper() not in reserved

valid_name = st.text(
    alphabet=string.ascii_letters + string.digits + '_-',
    min_size=1,
    max_size=20
).filter(is_valid_windows_name)

valid_content = st.text(
    alphabet=string.printable.replace("\r", '').replace('\n', ''),
    min_size=1,
    max_size=100
)

@given(valid_name)
def test_ensure_directory_creates_directory(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name

        result = ensure_directory(path)

        assert result is True
        assert path.is_dir()

@given(valid_name)
def test_ensure_directory_idempotent(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name

        result = ensure_directory(path)
        assert result is True

        result2 = ensure_directory(path)
        assert result2 is False
        assert path.is_dir()


@given(name=valid_name, content=valid_content)
def test_ensure_rules_file_creates_file(name, content,):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name

        result = ensure_rules_file(path, content)

        assert result is True
        assert path.is_file()
        assert path.read_text(encoding='utf-8') == content

@given(valid_name)
def test_ensure_marker_file_creates_empty(name):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / name

            result = ensure_marker_file(path)

            assert result is True
            assert path.is_file()
            assert path.stat().st_size == 0

@given(valid_name, valid_content)
def test_validate_existing_path_valid(name, content):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name
        path.write_text(content, encoding='utf-8')

        validate_existing_path(path)

@given(valid_name)
def test_validate_existing_path_rejects_nonexistent(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name

        with pytest.raises(PonyValidationError, match="does not exist"):
            validate_existing_path(path)

@given(valid_name)
def test_validate_existing_path_rejects_directory(name):
    """Директория (не файл) должна вызвать ошибку"""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name
        path.mkdir()

        with pytest.raises(PonyValidationError, match="is not a file"):
            validate_existing_path(path)