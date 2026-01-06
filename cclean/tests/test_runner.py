from cclean.runner import run_clean


def test_run_clean_dry_run(tmp_path):
    f = tmp_path / "a.txt"
    f.touch()

    def fake_collect(base_dir):
        return [f]

    import cclean.runner as runner
    runner.collect_clean_targets = fake_collect

    cleaned = run_clean(tmp_path, dry_run=True)

    assert f in cleaned
    assert f.exists()
