import pytest
from pathlib import Path
import cclean.runner as run

def test_guard_clean_allows_inside_base(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)

    file_inside = tmp_path / "file.txt"
    file_inside.touch()

    run.guard_clean(file_inside)

def test_guard_clean_allows_base_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)

    run.guard_clean(tmp_path)  # не должно упасть

def test_guard_clean_blocks_outside_path(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)

    outside = Path("/tmp/outside.txt")

    with pytest.raises(RuntimeError):
        run.guard_clean(outside)

def test_guard_clean_blocks_parent_escape(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)

    escaped = tmp_path.parent / "evil.txt"

    with pytest.raises(RuntimeError):
        run.guard_clean(escaped)

def test_guard_clean_blocks_symlink_escape(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)

    outside = tmp_path.parent / "outside.txt"
    outside.touch()

    link = tmp_path / "link"

    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks not supported on this system")

    with pytest.raises(RuntimeError):
        run.guard_clean(link)

def test_run_clean_calls_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "BASE_DIR", tmp_path)
    monkeypatch.setattr(run, "collect_clean_targets", lambda: [tmp_path / "a"])

    called = False
    def fake_remove(_):
        nonlocal called
        called = True

    monkeypatch.setattr(run, "remove_obj", fake_remove)

    (tmp_path / "a").touch()
    run.run_clean(dry_run=False)

    assert called