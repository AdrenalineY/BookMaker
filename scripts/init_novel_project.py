#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.11,<3", "rich>=14,<15", "typer>=0.16,<1"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Run: uv run scripts/init_novel_project.py 目标目录
# ──────────────────

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console


def main(
    target: Annotated[Path, typer.Argument(help="新小说项目根目录")],
) -> None:
    workspace = Path(__file__).resolve().parents[1]
    template = workspace / ".agents" / "skills" / "novel-init" / "assets" / "novel-template"
    destination = target.resolve() / "novel"
    if destination.exists():
        Console().print(f"INIT_REFUSED\t目标已存在：{destination}")
        raise typer.Exit(code=2)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _ = shutil.copytree(template, destination)
    Console().print(f"INIT_OK\t{destination}")


if __name__ == "__main__":
    typer.run(main)
