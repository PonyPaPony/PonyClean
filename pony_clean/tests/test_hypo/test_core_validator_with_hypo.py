import string
from pathlib import Path

import pytest
from hypothesis import given, strategies as st, assume
from hypothesis.strategies import composite
from pony_clean.core.validators import check_protected, check_dangerous
from pony_clean.errors.exceptions import PonyAPIError

valid_dir_name = st.text(
    alphabet=string.ascii_letters + string.digits + '_-',
    min_size=1,
    max_size=15
)

path_parts_strategy = st.lists(
    valid_dir_name,
    min_size=1,
    max_size=5
)

@composite
def path_strategy(draw):
    parts = draw(path_parts_strategy)
    return Path(*parts)

protected_dirs_strategy = st.sets(
    valid_dir_name,
    min_size=3,
    max_size=5
)

@composite
def safe_path_and_protected(draw):
    protected = draw(protected_dirs_strategy)
    path_parts = draw(path_parts_strategy)

    assume(path_parts[0] not in protected)

    return Path(*path_parts), protected

@composite
def protected_path_and_protected(draw):
    protected = draw(protected_dirs_strategy)
    protected_dir = draw(st.sampled_from(list(protected)))

    extra_parts = draw(st.lists(valid_dir_name, min_size=0, max_size=3))

    path = Path(protected_dir, *extra_parts)

    return path, protected

@composite
def nested_safe_paths(draw):
    base_parts = draw(st.lists(valid_dir_name, min_size=1, max_size=3))
    base = Path(*base_parts)

    extra_parts = draw(st.lists(valid_dir_name, min_size=1, max_size=3))
    child = base / Path(*extra_parts)

    return base, child

@composite
def unrelated_paths(draw):
    path1_parts = draw(st.lists(valid_dir_name, min_size=1, max_size=3))
    path2_parts = draw(st.lists(valid_dir_name, min_size=1, max_size=3))

    path1 = Path(*path1_parts)
    path2 = Path(*path2_parts)

    assume(path1 != path2)
    assume(path1 not in path2.parents)
    assume(path2 not in path1.parents)

    return path1, path2

@given(safe_path_and_protected())
def test_check_protected_safe(data):
    path, protected = data
    check_protected(path, protected)

@given(protected_path_and_protected())
def test_check_protected_raises(data):
    path, protected = data
    with pytest.raises(PonyAPIError, match="Cannot clean protected directory"):
        check_protected(path, protected)

@given(nested_safe_paths())
def test_check_dangerous_safe(data):
    base, child = data
    check_dangerous(base, child)

@given(unrelated_paths())
def test_check_dangerous_unrelated(data):
    path1, path2 = data
    with pytest.raises(PonyAPIError, match="Dangerous path"):
        check_dangerous(path1, path2)
