Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and the project adheres to semantic versioning.

[Unreleased]

🚀 Added

Introduced cli_ritual_cheatsheet_builder.py for generating ritual cheat sheets.

Added bbc_book_config.json for BBC‑style book configuration.

Added Conda recipe (meta.yaml) for Tiangan package distribution.

Added build.sh and run_test.py for Conda build/test integration.

Added CLI tests to run_test.py.

Added multi‑architecture Docker workflow (docker-multiarch.yml).

Added release automation workflow (release.yml).

Added GitHub Actions workflow for Conda package builds.

Added Anaconda upload step to Conda build workflow.


🧱 Changed

Updated Dockerfile.conda to align with new build and packaging processes.

Updated Conda build workflow (build-conda-package.yml) with:

Corrected tag filters.

Improved naming.

Removal of debugging artifacts.

Recipe‑based build structure.

Updated README with:

New badges and improved formatting.

Updated deployment instructions.

Added Tiangan module section.

Updated links (including AI Studio app).

Improved section headers with icons.

Refactored project structure to remove React dependencies.


🧹 Removed

Deleted outdated Conda build workflows.

Removed redundant or outdated versions of:

meta.yaml

build-conda.sh

build-conda-package.yml

Removed unnecessary README content and duplicate badges.


🛠 Fixed

Corrected tag filter logic in Conda package workflow.

Cleaned up workflow names and removed unnecessary newlines.


🔧 Maintenance

Merged PR #1 (dbugpro/dbugpro-patch-1).

Cleaned repository structure and removed unused files.

[0.1.0] – Initial Release

Project initialized with React + Vite (later removed).

Added early README structure and project metadata.
