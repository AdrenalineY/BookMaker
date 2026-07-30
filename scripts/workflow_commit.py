from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import assert_never

from pydantic import TypeAdapter

from workflow_io import (
    DataFileError,
    encode_json,
    encode_jsonl,
    load_json,
    load_jsonl,
    write_transaction,
)
from workflow_models import (
    CanonEntry,
    ChapterSummary,
    CharacterState,
    CharacterUpdate,
    ClueEntry,
    ClueMoment,
    ClueStatus,
    ClueUpdate,
    CommitManifest,
    EventEntry,
    WorkflowStage,
    WorkflowStatusMap,
)
from workflow_validation import (
    ValidationReport,
    check_canon_entries,
    check_clue_entries,
    check_timeline_events,
)

MANIFEST_ADAPTER = TypeAdapter(CommitManifest)
EVENT_ADAPTER = TypeAdapter(EventEntry)
CANON_ADAPTER = TypeAdapter(tuple[CanonEntry, ...])
CHARACTER_STATE_ADAPTER = TypeAdapter(tuple[CharacterState, ...])
CLUE_ADAPTER = TypeAdapter(tuple[ClueEntry, ...])
SUMMARY_ADAPTER = TypeAdapter(ChapterSummary)
STATUS_ADAPTER = TypeAdapter(WorkflowStatusMap)
STRING_MAP_ADAPTER = TypeAdapter(dict[str, str])


class ApprovalRequiredError(Exception):
    pass


def _apply_character_updates(
    states: tuple[CharacterState, ...],
    updates: tuple[CharacterUpdate, ...],
    path: Path,
) -> tuple[CharacterState, ...]:
    by_id = {state.character_id: state for state in states}
    for update in updates:
        current = by_id.get(update.character_id)
        if current is None:
            raise DataFileError(path=path, detail=f"人物状态不存在：{update.character_id}")
        knowledge = tuple(dict.fromkeys((*current.knowledge, *update.knowledge_add)))
        by_id[update.character_id] = current.model_copy(
            update={
                "location": update.location,
                "emotional": update.emotional,
                "goals": update.goals,
                "knowledge": knowledge,
            }
        )
    return tuple(by_id.values())


def _apply_clue_updates(
    clues: tuple[ClueEntry, ...],
    updates: tuple[ClueUpdate, ...],
    path: Path,
) -> tuple[ClueEntry, ...]:
    by_id = {clue.id: clue for clue in clues}
    for update in updates:
        current = by_id.get(update.clue_id)
        if current is None:
            raise DataFileError(path=path, detail=f"线索不存在：{update.clue_id}")
        moment = ClueMoment(chapter=update.chapter, change=update.change)
        match update.status:
            case ClueStatus.PLANNED | ClueStatus.ABANDONED:
                changed = current.model_copy(update={"status": update.status})
            case ClueStatus.PLANTED:
                changed = current.model_copy(update={"status": update.status, "planted": moment})
            case ClueStatus.PROGRESSING:
                changed = current.model_copy(
                    update={
                        "status": update.status,
                        "progress": (*current.progress, moment),
                    }
                )
            case ClueStatus.PAID_OFF:
                changed = current.model_copy(update={"status": update.status, "payoff": moment})
            case unreachable:
                assert_never(unreachable)
        by_id[update.clue_id] = changed
    return tuple(by_id.values())


def _raise_for_validation_issues(
    reports: tuple[ValidationReport, ...],
    novel: Path,
) -> None:
    issues = tuple(issue for report in reports for issue in report.issues)
    if not issues:
        return
    details = "; ".join(f"{issue.code}:{issue.location}" for issue in issues)
    raise DataFileError(path=novel, detail=f"提交前校验失败：{details}")


def commit_chapter(root: Path, chapter_id: str, approved: bool) -> None:
    if not approved:
        raise ApprovalRequiredError

    novel = root / "novel"
    chapter_dir = novel / "chapters" / chapter_id
    manifest = load_json(chapter_dir / "commit_manifest.yaml", MANIFEST_ADAPTER)
    if manifest.chapter_id != chapter_id or manifest.status is not WorkflowStage.HUMAN_APPROVED:
        raise ApprovalRequiredError

    draft = (chapter_dir / "draft.md").read_text(encoding="utf-8")
    if not draft.strip():
        raise DataFileError(path=chapter_dir / "draft.md", detail="草稿为空")

    events_path = novel / "state" / "events.jsonl"
    canon_path = novel / "bible" / "canon.yaml"
    character_path = novel / "state" / "character_state.yaml"
    clue_path = novel / "state" / "clues.yaml"
    summaries_path = novel / "state" / "chapter_summaries.jsonl"
    status_path = novel / "state" / "workflow_status.yaml"

    events = load_jsonl(events_path, EVENT_ADAPTER)
    canon = load_json(canon_path, CANON_ADAPTER)
    character_states = load_json(character_path, CHARACTER_STATE_ADAPTER)
    clues = load_json(clue_path, CLUE_ADAPTER)
    summaries = load_jsonl(summaries_path, SUMMARY_ADAPTER)
    status = load_json(status_path, STATUS_ADAPTER)

    known_event_ids = {event.id for event in events}
    if any(event.id in known_event_ids for event in manifest.events):
        raise DataFileError(path=events_path, detail="提交清单包含重复事件 ID")
    known_canon_ids = {entry.id for entry in canon}
    if any(entry.id in known_canon_ids for entry in manifest.canon_changes):
        raise DataFileError(path=canon_path, detail="提交清单包含重复正史 ID")

    updated_characters = _apply_character_updates(
        character_states,
        manifest.character_updates,
        character_path,
    )
    updated_clues = _apply_clue_updates(clues, manifest.clue_updates, clue_path)
    updated_events = (*events, *manifest.events)
    updated_canon = (*canon, *manifest.canon_changes)
    _raise_for_validation_issues(
        (
            check_canon_entries(updated_canon),
            check_timeline_events(updated_events, str(events_path)),
            check_clue_entries(updated_clues, str(clue_path)),
        ),
        novel,
    )

    updated_status = dict(status.root)
    updated_status[chapter_id] = WorkflowStage.CANON_COMMITTED
    summary = ChapterSummary(chapter_id=chapter_id, summary=manifest.summary)
    change_record = {
        "chapter_id": chapter_id,
        "committed_at": datetime.now(UTC).isoformat(),
        "event_count": str(len(manifest.events)),
        "canon_change_count": str(len(manifest.canon_changes)),
    }
    change_log_path = novel / "state" / "change_log.jsonl"
    change_log = change_log_path.read_text(encoding="utf-8")
    change_line = STRING_MAP_ADAPTER.dump_json(change_record, ensure_ascii=False).decode("utf-8")

    files = (
        (chapter_dir / "final.md", draft),
        (events_path, encode_jsonl(updated_events, EVENT_ADAPTER)),
        (canon_path, encode_json(updated_canon, CANON_ADAPTER)),
        (character_path, encode_json(updated_characters, CHARACTER_STATE_ADAPTER)),
        (clue_path, encode_json(updated_clues, CLUE_ADAPTER)),
        (summaries_path, encode_jsonl((*summaries, summary), SUMMARY_ADAPTER)),
        (status_path, encode_json(WorkflowStatusMap(updated_status), STATUS_ADAPTER)),
        (change_log_path, change_log + change_line + "\n"),
    )
    write_transaction(files)
