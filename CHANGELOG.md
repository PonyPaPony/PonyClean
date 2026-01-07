# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/).

---

## [0.2.1] - 2026-01-07

### Fixed
- Fixed configuration semantics: `clean.toml` is now the only source of clean rules
- Removed incorrect file-based default config fallback

### Changed
- Refactored resolver logic for clarity and safety
- Improved protection of critical directories (`venv`, `.git`, `.ponyclean`)
---

## [0.2.0] – 2026-01-07

### Added
- New `cclean init` command to explicitly create configuration files.
- Built-in default cleanup rules used when no config is present.
- Hard safety exclusions for protected directories:
  - `venv`
  - `.venv`
  - `.git`
  - `.ponyclean`
- Dry-run mode now reliably previews all actions without side effects.

### Changed
- Configuration files are now stored in `.ponyclean/` instead of `data/`.
- Cleanup behavior no longer creates any files automatically.
- `cclean run` now uses safe defaults instead of doing nothing when config is missing.

### Fixed
- Prevented accidental cleanup of virtual environments and site-packages.
- Fixed UX issue where running the cleaner could pollute the project directory.
- Improved separation between configuration initialization and cleanup logic.

### Security
- Introduced mandatory protection against destructive operations inside virtual environments.
- Cleanup traversal now enforces directory-level safety guards before applying rules.

---

## [0.1.0] – Initial Release

### Added
- Initial implementation of PonyClean CLI.
- Basic cleanup command for removing common Python project artifacts.
- Support for custom cleanup rules via configuration files.
- `--dry-run` flag to preview cleanup actions.
- Simple reporting of removed or matched files.

### Known Issues
- Configuration files were created automatically on run.
- Cleanup traversal did not exclude virtual environments by default.
- Safety guarantees were not yet enforced.

---

