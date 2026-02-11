import string
import pytest
import tempfile
from pathlib import Path
from hypothesis import given, strategies as st
from pony_clean.services.loader import load_user_rules, load_protected_rules, load_toml_if_valid
from pony_clean.errors.exceptions import PonyValidationError


def is_valid_windows_name(name: str) -> bool:
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3',
                'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    return name.upper() not in reserved

def format_toml_array(items: list[str]) -> str:
    formated = ', '.join(f'"{item}"' for item in items)
    return f'[{formated}]'

valid_name = st.text(
    alphabet=string.ascii_letters + string.digits + '_-',
    min_size=1,
    max_size=20
).filter(is_valid_windows_name)

def temp_ready(path, name, obj, patterns):
    tmp_path = Path(path)
    toml_file = tmp_path / '.ponyclean' / name
    toml_file.parent.mkdir(parents=True)

    toml_content = f"{obj} = {format_toml_array(patterns)}"
    toml_file.write_text(toml_content, encoding='utf-8')

    return tmp_path


@given(st.lists(valid_name, min_size=1, max_size=10))
def test_load_user_rules_with_various_patterns(patterns):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = temp_ready(tmpdir, 'clean.toml', 'files', patterns)

        result = load_user_rules(tmp_path)
        assert 'files' in result
        assert result['files'] == patterns


@given(st.lists(valid_name, min_size=1, max_size=10))
def test_load_protected_rules_with_various_paths(paths):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = temp_ready(tmpdir, 'protected.toml', 'paths', paths)

        result = load_protected_rules(tmp_path)

        assert result == set(paths)

@given(valid_name)
def test_load_toml_if_valid_rejects_nonexistent(filename):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        toml_file = tmp_path / filename

        with pytest.raises(PonyValidationError, match="does not exist"):
            load_toml_if_valid(toml_file)