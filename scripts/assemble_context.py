#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.11,<3", "rich>=14,<15", "typer>=0.16,<1"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Run: uv run scripts/assemble_context.py CH001 --root .
# ──────────────────

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from workflow_cli import emit_data_error, normalized_root
from workflow_context import assemble_context
from workflow_io import DataFileError


def main(
    chapter_id: Annotated[str, typer.Argument(help="章节 ID，例如 CH001")],
    root: Annotated[Path, typer.Option(help="小说工作区根目录")] = Path(),
) -> None:
    try:
        target = assemble_context(normalized_root(root), chapter_id)
    except DataFileError as error:
        emit_data_error(error)
        return
    Console().print(f"CONTEXT_OK\t{target}")


if __name__ == "__main__":
    typer.run(main)
