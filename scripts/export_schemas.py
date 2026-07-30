#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.11,<3", "rich>=14,<15", "typer>=0.16,<1"]
# ///
# ─── How to run ───
# 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Run: uv run scripts/export_schemas.py --root .
# ──────────────────

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import TypeAdapter
from rich.console import Console

from workflow_models import (
    CanonEntry,
    ChapterCard,
    CharacterState,
    ClueEntry,
    CommitManifest,
    EventEntry,
)


def main(
    root: Annotated[Path, typer.Option(help="小说工作区根目录")] = Path(),
) -> None:
    output = root.resolve() / "novel" / "schemas"
    output.mkdir(parents=True, exist_ok=True)
    adapters = (
        ("canon.schema.json", TypeAdapter(tuple[CanonEntry, ...])),
        ("event.schema.json", TypeAdapter(EventEntry)),
        ("clue.schema.json", TypeAdapter(tuple[ClueEntry, ...])),
        ("chapter-card.schema.json", TypeAdapter(ChapterCard)),
        ("commit-manifest.schema.json", TypeAdapter(CommitManifest)),
        ("character-state.schema.json", TypeAdapter(tuple[CharacterState, ...])),
    )
    for name, adapter in adapters:
        schema = adapter.json_schema()
        schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        schema["title"] = schema.get("title") or name.removesuffix(".schema.json")
        _ = output.joinpath(name).write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    Console().print(f"SCHEMA_OK\t{len(adapters)}\t{output}")


if __name__ == "__main__":
    typer.run(main)
