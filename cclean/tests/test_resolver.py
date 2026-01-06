import cclean.resolver as resolver

def test_collect_clean_targets_basic(tmp_path, monkeypatch):
    pycache = tmp_path / "__pycache__"
    pycache.mkdir()

    pyc_file = pycache / "test.cpython-312.pyc"
    pyc_file.touch()

    other = tmp_path / "keep.txt"
    other.touch()

    fake_config = {
        "files": ["__pycache__", "*.pyc"]
    }

    monkeypatch.setattr(
        resolver,
        "load_clean_config",
        lambda base_dir: fake_config
    )

    result = resolver.collect_clean_targets(tmp_path)

    assert pycache in result
    assert pyc_file not in result
    assert other not in result

def test_collect_clean_targets_files_only(tmp_path, monkeypatch):
    pyc1 = tmp_path / "a.pyc"
    pyc2 = tmp_path / "b.pyc"
    pyc1.touch()
    pyc2.touch()

    monkeypatch.setattr(
        resolver,
        "load_clean_config",
        lambda base_dir: {"files": ["*.pyc"]}
    )

    result = resolver.collect_clean_targets(tmp_path)

    assert pyc1 in result
    assert pyc2 in result

def test_prune_nested_directories(tmp_path, monkeypatch):
    parent = tmp_path / "build"
    parent.mkdir()

    child = parent / "tmp"
    child.mkdir()

    monkeypatch.setattr(
        resolver,
        "load_clean_config",
        lambda base_dir: {"files": ["build", "tmp"]}
    )

    result = resolver.collect_clean_targets(tmp_path)

    assert parent in result
    assert child not in result

def test_collect_clean_targets_empty_config(tmp_path, monkeypatch):
    (tmp_path / "a.txt").touch()

    monkeypatch.setattr(
        resolver,
        "load_clean_config",
        lambda base_dir: {}
    )

    result = resolver.collect_clean_targets(tmp_path)

    assert result == []
