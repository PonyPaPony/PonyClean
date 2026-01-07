import argparse
from .runner import run_clean
from .reports import print_report
from .init import init_config_files
from .paths import get_base_dir

def main():
    parser = argparse.ArgumentParser(
        prog="cclean",
        description="Clean project trash"
    )

    subparsers = parser.add_subparsers(
        required=True,
        dest="command"
    )

    run = subparsers.add_parser("run", help="Clean project files")
    run.add_argument("--root", type=str, help="Root directory to clean")
    run.add_argument("--dry-run", action="store_true")
    run.set_defaults(func=handle_clean)

    init = subparsers.add_parser("init", help="Create PonyClean config files")
    init.add_argument("--root", type=str, help="Root directory")
    init.set_defaults(func=handle_init)

    args = parser.parse_args()
    args.func(args)

def handle_clean(args):
    base_dir = get_base_dir(args.root)

    print("Cleaning...")
    cleaned = run_clean(base_dir, dry_run=args.dry_run)

    if not cleaned:
        print("Nothing to clean.")
    else:
        print_report(cleaned, base_dir, args.dry_run)

    print("Done")

def handle_init(args):
    base_dir = get_base_dir(args.root)

    print("Initializing...")
    created = init_config_files(base_dir)

    if created:
        print("Created .ponyclean/ directory with config files.")
    else:
        print("Config already exists, nothing to do.")