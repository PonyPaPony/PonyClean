import pytest
import cclean.resolver as resolver


@pytest.fixture
def fake_project(tmp_path):
    pycache = tmp_path / "__pycache__"
    pycache.mkdir()

    pyc_file = pycache / "test.cpython-312.pyc"
    pyc_file.touch()

    fake_config = {
        "files": ["__pycache__", "*.pyc"]
    }

    yield fake_config, tmp_path, pycache, pyc_file


def test_collect_clean_targets(fake_project, monkeypatch):
    fake_config, tmp_path, pycache, pyc_file = fake_project

    monkeypatch.setattr(resolver, "BASE_DIR", tmp_path)
    monkeypatch.setattr(
        resolver,
        "load_clean_config",
        lambda: fake_config
    )

    result = resolver.collect_clean_targets()

    assert pycache in result
    assert pyc_file not in result
