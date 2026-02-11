from pathlib import Path
from pony_clean.core.target_resolver import prune_nested_paths, matches
from hypothesis import given, strategies as st, assume
from hypothesis.strategies import composite
import tempfile
import string

valid_filename = st.text(
    alphabet=string.ascii_letters + string.digits + '_-',
    min_size=1,
    max_size=20
).filter(
    lambda x: x not in {'.', '..'}
    and not x.endswith(' ')
    and not x.endswith('.')
)


@composite
def temp_file_with_name(draw):
    """Создает временный файл с именем"""
    filename = draw(valid_filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / filename
        file_path.touch()
        return file_path, filename


@given(filename=valid_filename, pattern=valid_filename)
def test_matches_exact_match_property(filename, pattern):
    """Если паттерн == имени файла, должно быть совпадение"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / filename
        file.touch()

        if filename == pattern:
            assert matches(file, [pattern])


@given(st.lists(valid_filename, min_size=1, max_size=5))
def test_matches_always_checks_all_patterns(patterns):
    """Функция должна проверять все паттерны"""
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = patterns[0]
        file = Path(tmpdir) / filename
        file.touch()

        assert matches(file, patterns)


@given(st.lists(valid_filename, min_size=0, max_size=3))
def test_matches_empty_or_no_match_returns_false(patterns):
    """Если паттернов нет или они не совпадают, возвращается False"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Используем имя, которое точно не совпадет с паттернами
        unique_name = "definitely_unique_name_12345_xyz"
        file = Path(tmpdir) / unique_name
        file.touch()

        assume(unique_name not in patterns)
        assume(all('*' not in p for p in patterns))  # Упрощаем логику

        result = matches(file, patterns)
        assert not result


@given(st.sets(st.integers(min_value=0, max_value=10), min_size=2, max_size=5))
def test_prune_nested_paths_property(depths):
    """Вложенные пути должны удаляться"""
    with tempfile.TemporaryDirectory() as tmpdir:
        depths_list = sorted(depths)
        assume(len(depths_list) >= 2)

        paths = set()
        current = Path(tmpdir)

        for depth in depths_list:
            current = current / f"dir_{depth}"
            current.mkdir(exist_ok=True)
            paths.add(current)

        result = prune_nested_paths(paths)

        assert len(result) == 1
        assert min(paths, key=lambda p: len(p.parts)) in result


@given(st.lists(valid_filename, min_size=1, max_size=10, unique=True))
def test_prune_non_nested_paths_unchanged(dir_names):
    """Не-вложенные пути не должны удаляться"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Фильтруем дубликаты с учетом регистра (для Windows)
        unique_names = []
        seen_lower = set()
        for name in dir_names:
            name_lower = name.lower()
            if name_lower not in seen_lower:
                unique_names.append(name)
                seen_lower.add(name_lower)

        assume(len(unique_names) >= 1)  # Должен остаться хотя бы один

        paths = set()
        tmp_path = Path(tmpdir)

        for name in unique_names:  # Используем отфильтрованный список
            dir_path = tmp_path / name
            dir_path.mkdir()
            paths.add(dir_path)

        result = prune_nested_paths(paths)

        assert len(result) == len(paths)
        assert set(result) == paths


@given(valid_filename)
def test_matches_with_wildcard_pattern(filename):
    """Тест с wildcard-паттернами"""
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / filename
        file.touch()

        # Паттерн *.* должен совпадать с файлами, содержащими точку
        if '.' in filename:
            assert matches(file, ['*.*'])

        # Паттерн * должен совпадать с любым файлом
        assert matches(file, ['*'])