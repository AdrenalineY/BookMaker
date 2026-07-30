#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.11,<3", "rich>=14,<15", "typer>=0.16,<1"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Run: uv run scripts/query_story_state.py 关键词 --root .
# ──────────────────

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from workflow_cli import normalized_root
from workflow_query import query_story_state


def main(
    keyword: Annotated[str, typer.Argument(help="ID、人物名、地点或关键词")],
    root: Annotated[Path, typer.Option(help="小说工作区根目录")] = Path(),
) -> None:
    hits = query_story_state(normalized_root(root), keyword)
    console = Console()
    if not hits:
        console.print("QUERY_EMPTY")
        raise typer.Exit(code=1)
    for hit in hits:
        console.print(f"{hit.path}:{hit.line_number}\t{hit.line}")


if __name__ == "__main__":
    typer.run(main)
