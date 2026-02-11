from pony_clean.core.target_resolver import prune_nested_paths, matches

def test_prune_nested_paths(tmp_path):
    parent = tmp_path / "build"
    parent.mkdir()

    child = parent / "tmp"
    child.mkdir()

    paths = {parent, child}
    result = prune_nested_paths(paths)

    assert parent in result
    assert child not in result

def test_matches_exact_name(tmp_path):
    file = tmp_path / "build"
    file.touch()

    assert matches(file, ["build"])
    assert not matches(file, ["tmp"])

def test_matches_wildcard_pattern(tmp_path):
    file = tmp_path / "test.log"
    file.touch()

    assert matches(file, ["*.log"])
    assert matches(file, ['test.*'])
    assert not matches(file, ['*.txt'])


def test_matches_directory(tmp_path):
    """Совпадение директории"""
    dir_path = tmp_path / "node_modules"
    dir_path.mkdir()

    assert matches(dir_path, ["node_modules"])
    assert matches(dir_path, ["node_*"])


def test_matches_multiple_patterns(tmp_path):
    """Проверка нескольких паттернов"""
    file = tmp_path / "cache.tmp"
    file.touch()

    assert matches(file, ["*.log", "*.tmp", "build"])
    assert not matches(file, ["*.log", "*.txt"])


def test_matches_empty_patterns(tmp_path):
    """Пустой список паттернов"""
    file = tmp_path / "anything"
    file.touch()

    assert not matches(file, [])


def test_matches_egg_info_directory(tmp_path):
    """Паттерн *.egg-info должен находить директории типа mypackage.egg-info"""
    egg_info = tmp_path / "mypackage.egg-info"
    egg_info.mkdir()

    assert matches(egg_info, ["*.egg-info"])


def test_matches_dist_directory(tmp_path):
    """Паттерн dist должен находить директорию dist"""
    dist = tmp_path / "dist"
    dist.mkdir()

    assert matches(dist, ["dist"])