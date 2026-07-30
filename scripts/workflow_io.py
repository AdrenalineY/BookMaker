from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from pydantic import TypeAdapter, ValidationError
from typing_extensions import override

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class DataFileError(Exception):
    path: Path
    detail: str

    @override
    def __str__(self) -> str:
        return f"{self.path}: {self.detail}"


def load_json(path: Path, adapter: TypeAdapter[T]) -> T:
    try:
        return adapter.validate_json(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise DataFileError(path=path, detail=str(error)) from error
    except ValidationError as error:
        raise DataFileError(path=path, detail=str(error)) from error


def load_jsonl(path: Path, adapter: TypeAdapter[T]) -> tuple[T, ...]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise DataFileError(path=path, detail=str(error)) from error
    parsed: list[T] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            parsed.append(adapter.validate_json(line))
        except ValidationError as error:
            detail = f"第 {line_number} 行：{error}"
            raise DataFileError(path=path, detail=detail) from error
    return tuple(parsed)


def encode_json(value: T, adapter: TypeAdapter[T]) -> str:
    return adapter.dump_json(value, indent=2, ensure_ascii=False).decode("utf-8") + "\n"


def encode_jsonl(values: tuple[T, ...], adapter: TypeAdapter[T]) -> str:
    return "".join(
        adapter.dump_json(value, ensure_ascii=False).decode("utf-8") + "\n" for value in values
    )


def write_transaction(files: tuple[tuple[Path, str], ...]) -> None:
    staged: list[tuple[Path, Path]] = []
    active_target = Path()
    try:
        for target, content in files:
            active_target = target
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(f".{target.name}.tmp")
            _ = temporary.write_text(content, encoding="utf-8", newline="\n")
            staged.append((temporary, target))
        for temporary, target in staged:
            active_target = target
            _ = temporary.replace(target)
    except OSError as error:
        for temporary, _target in staged:
            _ = temporary.unlink(missing_ok=True)
        raise DataFileError(path=active_target, detail=str(error)) from error
