import tempfile
import string
from pathlib import Path
from pony_clean.api.cli import remove, guard
from hypothesis import given, strategies as st


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

protected_dirs_strategy = st.sets(
    valid_name,
    min_size=3,
    max_size=5
)

@given(valid_name)
def test_remove_removes_directory(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name
        path.mkdir()
        remove(path)
        assert not path.exists()

@given(valid_name)
def test_remove_removes_file(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name
        path.touch()
        remove(path)
        assert not path.exists()

@given(valid_name)
def test_remove_remove_file(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / name
        path.mkdir()

        (path / 'deb').mkdir()
        (path / 'deb' / 'file.deb').touch()
        (path / 'debebe.txt').touch()

        remove(path)

        assert not path.exists()

@given(st.lists(valid_name, min_size=1, max_size=10))
def test_remove_handlers_deeply_nested_dirs(names):
    with tempfile.TemporaryDirectory() as tmpdir:
        cur = Path(tmpdir)
        for name in names:
            cur = cur / name
            cur.mkdir()

        root = Path(tmpdir) / names[0]
        remove(root)

        assert not root.exists()

@given(valid_name, valid_name)
def test_guard_accepts_save_paths(name1, name2):
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = Path(tmpdir) / name1
        path1.mkdir()

        path2 = path1 / name2
        path2.mkdir()

        guard(path2, path1)
