from pathlib import Path

def print_report(cleaned: list[Path], base_dir: Path, dry_run: bool):
    if dry_run:
        print(f"[DRY-RUN] Would remove {len(cleaned)} items:")
        for obj in cleaned:
            try:
                rel = obj.relative_to(base_dir)
            except ValueError:
                # на всякий случай, но guard_clean не должен допустить
                rel = obj
            print(f"  - {rel}")
    else:
        print(f"Cleaned {len(cleaned)} items")