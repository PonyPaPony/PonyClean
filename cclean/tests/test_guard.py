import pytest
from cclean.runner import guard_clean


def test_guard_allows_inside(tmp_path):
    f = tmp_path / "a.txt"
    f.touch()

    guard_clean(f, tmp_path)


def test_guard_allows_base(tmp_path):
    guard_clean(tmp_path, tmp_path)


def test_guard_blocks_outside(tmp_path):
    outside = tmp_path.parent / "evil.txt"
    outside.touch()

    with pytest.raises(RuntimeError):
        guard_clean(outside, tmp_path)
