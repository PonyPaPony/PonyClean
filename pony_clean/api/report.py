from pathlib import Path
from pony_clean.services.writer import print_info, print_success

def report(cleaned: list[Path], base_path: Path, dry_run: bool):
    if dry_run:
        print_info(f"[DRY-RUN] Would remove {len(cleaned)} items:")
        for obj in cleaned:
            try:
                rel = obj.relative_to(base_path)
            except ValueError:
                rel = obj
            print_info(f"  - {rel}")
    else:
        print_success(f"Removed {len(cleaned)} items")