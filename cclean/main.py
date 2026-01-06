import argparse
from .runner import run_clean
from .reports import print_report
from .init import ensure_config_files
from .paths import get_base_dir

def main():
    parser = argparse.ArgumentParser(
        prog="cclean",
        description="Clean project trash"
    )

    clean = parser.add_subparsers(required=True).add_parser("run")
    clean.add_argument("--root", type=str, help="Root directory to clean")
    clean.add_argument("--dry-run", action="store_true")
    clean.set_defaults(func=handle_clean)

    args = parser.parse_args()
    args.func(args)

def handle_clean(args):
    base_dir = get_base_dir(args.root)

    ensure_config_files(base_dir)

    print("Cleaning...")
    cleaned = run_clean(base_dir, dry_run=args.dry_run)

    if not cleaned:
        print("Nothing to clean.")
    else:
        print_report(cleaned, base_dir, args.dry_run)

    print("Done")