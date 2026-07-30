from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SEARCH_PATTERNS = ("*.md", "*.yaml", "*.jsonl", "*.csv")


@dataclass(frozen=True, slots=True)
class SearchHit:
    path: Path
    line_number: int
    line: str


def query_story_state(root: Path, keyword: str) -> tuple[SearchHit, ...]:
    novel = root / "novel"
    needle = keyword.casefold()
    hits: list[SearchHit] = []
    for pattern in SEARCH_PATTERNS:
        for path in sorted(novel.rglob(pattern)):
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if needle in line.casefold():
                    hits.append(
                        SearchHit(
                            path=path.relative_to(root),
                            line_number=line_number,
                            line=line.strip(),
                        )
                    )
    return tuple(hits)
