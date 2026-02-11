from unittest.mock import patch
from pony_clean.services.discovery import discover_targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
def test_discover_targets_finds_matching_files(mock_rules, mock_protected, tmp_path):
    mock_rules.return_value = {"files": ["*.pyc", "__pycache__"]}
    mock_protected.return_value = set()

    (tmp_path / "test.pyc").touch()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "keep.py").touch()

    targets = discover_targets(tmp_path)

    assert len(targets) == 2
    assert tmp_path / "test.pyc" in targets
    assert tmp_path / "__pycache__" in targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
def test_discover_targets_respects_protected_dirs(mock_rules, mock_protected, tmp_path):
    mock_rules.return_value = {"files": ["__pycache__"]}
    mock_protected.return_value = set()

    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "__pycache__").mkdir()

    (tmp_path / "__pycache__").mkdir()

    targets = discover_targets(tmp_path)

    assert venv / "__pycache__" not in targets
    assert tmp_path / "__pycache__" in targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
def test_discover_targets_empty_patterns(mock_rules, mock_protected, tmp_path):
    mock_rules.return_value = {"files": []}
    mock_protected.return_value = set()

    (tmp_path / "test.pyc").touch()

    targets = discover_targets(tmp_path)

    assert targets == []


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
def test_discover_targets_prunes_nested_paths(mock_rules, mock_protected, tmp_path):
    mock_rules.return_value = {"files": ["*"]}
    mock_protected.return_value = set()

    parent = tmp_path / "build"
    parent.mkdir()
    child = parent / "dist"
    child.mkdir()

    targets = discover_targets(tmp_path)

    assert parent in targets
    assert child not in targets


@patch("pony_clean.services.discovery.load_protected_rules")
@patch("pony_clean.services.discovery.load_user_rules")
def test_discover_targets_respects_user_protected_paths(mock_rules, mock_protected, tmp_path):
    mock_rules.return_value = {"files": ["*"]}
    mock_protected.return_value = {"custom_protected"}

    (tmp_path / "build").mkdir()
    (tmp_path / "custom_protected").mkdir()

    targets = discover_targets(tmp_path)

    assert tmp_path / "build" in targets
    assert tmp_path / "custom_protected" not in targets