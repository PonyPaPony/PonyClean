import click
from pony_clean.api.cli import run_clean
from pony_clean.api.report import report
from pony_clean.services.pipeline import prepare_workspace
from pony_clean.infra.paths import get_base_path
from pony_clean.services.writer import print_success, print_info


@click.group()
@click.version_option(package_name="pony-clean")
def cli():
    """Clean project trash"""
    pass

@cli.command()
@click.option("--root", type=str, help="Root directory to clean")
@click.option("--dry-run", is_flag=True, help="Perform a dry run without deleting files")
def clean(root: str, dry_run: bool):
    base_path = get_base_path(root)

    print_info("Cleaning...")
    cleaned = run_clean(base_path, dry_run=dry_run)
    if not cleaned:
        print_info("Nothing to clean.")
    else:
     report(cleaned, base_path, dry_run)

    print_success("Done")

@cli.command()
@click.option("--root", type=str, help="Root directory to initialize")
def init(root: str):
    base_path = get_base_path(root)

    print_info("Initializing...")
    created = prepare_workspace(base_path)

    if created:
        print_success("Created .ponyclean/ directory with config files.")
    else:
        print_info("Config already exists, nothing to do.")