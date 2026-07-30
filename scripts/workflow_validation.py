from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import assert_never

from pydantic import TypeAdapter

from workflow_io import load_json, load_jsonl
from workflow_models import CanonEntry, CanonStatus, ClueEntry, ClueStatus, EventEntry

CANON_ADAPTER = TypeAdapter(tuple[CanonEntry, ...])
CLUE_ADAPTER = TypeAdapter(tuple[ClueEntry, ...])
EVENT_ADAPTER = TypeAdapter(EventEntry)

REQUIRED_PATHS = (
    "novel/brief/project_brief.md",
    "novel/brief/premise.md",
    "novel/brief/style_bible.yaml",
    "novel/bible/canon.yaml",
    "novel/bible/timeline_rules.yaml",
    "novel/characters/characters.yaml",
    "novel/characters/relationships.yaml",
    "novel/outline/master_outline.md",
    "novel/outline/volume_01.md",
    "novel/outline/chapter_matrix.csv",
    "novel/outline/thread_ledger.yaml",
    "novel/state/events.jsonl",
    "novel/state/chapter_summaries.jsonl",
    "novel/state/character_state.yaml",
    "novel/state/world_state.yaml",
    "novel/state/knowledge_state.yaml",
    "novel/state/clues.yaml",
    "novel/state/items.yaml",
    "novel/state/workflow_status.yaml",
    "novel/state/change_log.jsonl",
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    location: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    name: str
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        return not self.issues


def check_canon_entries(entries: tuple[CanonEntry, ...]) -> ValidationReport:
    ids = {entry.id for entry in entries}
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for entry in entries:
        if entry.id in seen:
            issues.append(ValidationIssue("CANON_DUPLICATE_ID", entry.id, "正史 ID 重复"))
        seen.add(entry.id)
        issues.extend(
            ValidationIssue(
                "CANON_MISSING_DEPENDENCY",
                entry.id,
                f"依赖不存在：{dependency}",
            )
            for dependency in entry.dependencies
            if dependency not in ids
        )
        match entry.status:
            case CanonStatus.CANON:
                if not entry.evidence:
                    issues.append(
                        ValidationIssue(
                            "CANON_EVIDENCE_REQUIRED",
                            entry.id,
                            "CANON 条目必须有正文或人工批准证据",
                        )
                    )
            case (
                CanonStatus.PLANNED
                | CanonStatus.RUMOR
                | CanonStatus.SECRET
                | CanonStatus.RETIRED
                | CanonStatus.UNKNOWN
            ):
                pass
            case unreachable:
                assert_never(unreachable)
    return ValidationReport(name="canon", issues=tuple(issues))


def validate_canon(root: Path) -> ValidationReport:
    path = root / "novel" / "bible" / "canon.yaml"
    entries = load_json(path, CANON_ADAPTER)
    return check_canon_entries(entries)


def check_timeline_events(
    events: tuple[EventEntry, ...],
    source: str,
) -> ValidationReport:
    event_by_id = {event.id: event for event in events}
    issues: list[ValidationIssue] = []
    if len(event_by_id) != len(events):
        issues.append(ValidationIssue("TIMELINE_DUPLICATE_ID", source, "事件 ID 重复"))
    for event in events:
        event_start = datetime.fromisoformat(f"{event.story_time.date}T{event.story_time.start}")
        for cause_id in event.causes:
            cause = event_by_id.get(cause_id)
            if cause is None:
                issues.append(
                    ValidationIssue(
                        "TIMELINE_MISSING_CAUSE",
                        event.id,
                        f"原因事件不存在：{cause_id}",
                    )
                )
                continue
            cause_start = datetime.fromisoformat(
                f"{cause.story_time.date}T{cause.story_time.start}"
            )
            if cause_start > event_start:
                issues.append(
                    ValidationIssue(
                        "TIMELINE_CAUSE_AFTER_EFFECT",
                        event.id,
                        f"原因 {cause_id} 晚于结果事件",
                    )
                )
    return ValidationReport(name="timeline", issues=tuple(issues))


def validate_timeline(root: Path) -> ValidationReport:
    path = root / "novel" / "state" / "events.jsonl"
    events = load_jsonl(path, EVENT_ADAPTER)
    return check_timeline_events(events, str(path))


def check_clue_entries(
    clues: tuple[ClueEntry, ...],
    source: str,
) -> ValidationReport:
    issues: list[ValidationIssue] = []
    if len({clue.id for clue in clues}) != len(clues):
        issues.append(ValidationIssue("CLUE_DUPLICATE_ID", source, "线索 ID 重复"))
    for clue in clues:
        match clue.status:
            case ClueStatus.PLANNED:
                pass
            case ClueStatus.PLANTED | ClueStatus.PROGRESSING:
                if clue.planted is None:
                    issues.append(
                        ValidationIssue(
                            "CLUE_PLANT_REQUIRED",
                            clue.id,
                            "已种植或推进的线索必须记录种植位置",
                        )
                    )
            case ClueStatus.PAID_OFF:
                if clue.payoff is None:
                    issues.append(
                        ValidationIssue(
                            "CLUE_PAYOFF_REQUIRED",
                            clue.id,
                            "PAID_OFF 线索必须记录兑现位置",
                        )
                    )
            case ClueStatus.ABANDONED:
                pass
            case unreachable:
                assert_never(unreachable)
    return ValidationReport(name="clues", issues=tuple(issues))


def validate_clues(root: Path) -> ValidationReport:
    path = root / "novel" / "state" / "clues.yaml"
    clues = load_json(path, CLUE_ADAPTER)
    return check_clue_entries(clues, str(path))


def validate_project(root: Path) -> ValidationReport:
    issues = [
        ValidationIssue("PROJECT_MISSING_PATH", relative, "缺少必需文件")
        for relative in REQUIRED_PATHS
        if not (root / relative).is_file()
    ]
    if issues:
        return ValidationReport(name="project", issues=tuple(issues))
    reports = (
        validate_canon(root),
        validate_timeline(root),
        validate_clues(root),
    )
    for report in reports:
        issues.extend(report.issues)
    return ValidationReport(name="project", issues=tuple(issues))
