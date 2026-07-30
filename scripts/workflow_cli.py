from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from workflow_io import DataFileError
from workflow_validation import ValidationReport

CONSOLE = Console()


def emit_report(report: ValidationReport) -> None:
    if report.is_valid:
        CONSOLE.print(f"{report.name.upper()}_OK")
        return
    for issue in report.issues:
        CONSOLE.print(f"{issue.code}\t{issue.location}\t{issue.message}")
    raise typer.Exit(code=1)


def emit_data_error(error: DataFileError) -> None:
    CONSOLE.print(f"DATA_ERROR\t{error}")
    raise typer.Exit(code=1) from error


def normalized_root(root: Path) -> Path:
    return root.resolve()
