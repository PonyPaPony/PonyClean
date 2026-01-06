from .paths import BASE_DIR

def print_report(cleaned, dry_run: bool):
    if dry_run:
        print(f"[DRY-RUN] Would remove {len(cleaned)} items:")
        for obj in cleaned:
            print(f"  - {obj.relative_to(BASE_DIR)}")
    else:
        print(f"Cleaned {len(cleaned)} items")
