#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.11,<3", "rich>=14,<15", "typer>=0.16,<1"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Run: uv run scripts/validate_clues.py --root .
# ──────────────────

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from workflow_cli import emit_data_error, emit_report, normalized_root
from workflow_io import DataFileError
from workflow_validation import validate_clues


def main(
    root: Annotated[Path, typer.Option(help="小说工作区根目录")] = Path(),
) -> None:
    try:
        emit_report(validate_clues(normalized_root(root)))
    except DataFileError as error:
        emit_data_error(error)


if __name__ == "__main__":
    typer.run(main)
