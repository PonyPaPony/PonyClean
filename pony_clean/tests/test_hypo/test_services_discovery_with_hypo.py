import tempfile
import string
from pathlib import Path
from unittest.mock import patch
from hypothesis import given, strategies as st
from pony_clean.services.discovery import discover_targets
from pony_clean.config.config_data import PROTECTED_DIRS


def is_valid_windows_name(name: str) -> bool:
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3',
                'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    return name.upper() not in reserved and name not in PROTECTED_DIRS

valid_name = st.text(
    alphabet=string.ascii_letters + string.digits + '_-',
    min_size=1,
    max_size=20
).filter(is_valid_windows_name)


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
@given(valid_name)
def test_discover_targets_finds_matching_directories(mock_rules, mock_protected, name):
    mock_rules.return_value = {"files": [name]}
    mock_protected.return_value = set()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        target = tmp_path / name
        target.mkdir()

        targets = discover_targets(tmp_path)

        assert target in targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
@given(valid_name)
def test_discover_targets_finds_matching_files(mock_rules, mock_protected, name):
    mock_rules.return_value = {"files": [name]}
    mock_protected.return_value = set()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        target = tmp_path / name
        target.touch()

        targets = discover_targets(tmp_path)

        assert target in targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
@given(st.lists(valid_name, min_size=1, max_size=5, unique=True))
def test_discover_targets_with_wildcard_pattern(mock_rules, mock_protected, names):
    mock_rules.return_value = {"files": ["*"]}
    mock_protected.return_value = set()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Фильтруем case-insensitive дубликаты для Windows
        unique_names = []
        seen_lower = set()
        for name in names:
            name_lower = name.lower()
            if name_lower not in seen_lower:
                unique_names.append(name)
                seen_lower.add(name_lower)

        # Создаем несколько файлов
        for name in unique_names:
            (tmp_path / name).touch()

        targets = discover_targets(tmp_path)

        # Все файлы должны быть найдены
        assert len(targets) == len(unique_names)
        for name in unique_names:
            assert tmp_path / name in targets