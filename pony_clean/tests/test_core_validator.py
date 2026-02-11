import pytest
from pathlib import Path
from pony_clean.config.config_data import PROTECTED_DIRS
from pony_clean.errors.exceptions import PonyAPIError
from pony_clean.core.validators import check_protected, check_dangerous


def test_check_protected():
    path = Path("my_project/build")
    check_protected(path, PROTECTED_DIRS)


def test_check_protected_error():
    path = Path(".venv/some/nested/path")

    with pytest.raises(PonyAPIError, match="Cannot clean protected directory"):
        check_protected(path, PROTECTED_DIRS)

def test_check_dangerous():
    base = Path("/home/user/project")
    path = Path("/home/user/project/build")

    check_dangerous(base, path)

def test_check_dangerous_error():
    base = Path("/home/user/project")
    path = Path("/home/user/other_folder")

    with pytest.raises(PonyAPIError, match="Dangerous path"):
        check_dangerous(base, path)


def test_check_dangerous_super_error():
    base = Path("/home/user/project")
    path = Path("/etc/passwd")

    with pytest.raises(PonyAPIError, match="Dangerous path"):
        check_dangerous(base, path)