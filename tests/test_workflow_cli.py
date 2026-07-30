from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import TypeAdapter
from scripts.workflow_models import (
    CanonEntry,
    ClueEntry,
    ClueStatus,
    CommitManifest,
    WorkflowStage,
)

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = WORKSPACE_ROOT / "tests" / "fixtures" / "minimal_project"
SCRIPTS_ROOT = WORKSPACE_ROOT / "scripts"
CANON_LIST_ADAPTER = TypeAdapter(list[CanonEntry])
CLUE_LIST_ADAPTER = TypeAdapter(list[ClueEntry])
MANIFEST_ADAPTER = TypeAdapter(CommitManifest)
STATUS_MAP_ADAPTER = TypeAdapter(dict[str, WorkflowStage])


def run_script(name: str, arguments: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_ROOT / name), *arguments],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    target = tmp_path / "project"
    return shutil.copytree(FIXTURE_ROOT, target)


def test_project_validation_reports_ready_when_fixture_is_complete(project_root: Path) -> None:
    result = run_script("validate_project.py", ("--root", str(project_root)))

    assert result.returncode == 0
    assert "PROJECT_OK" in result.stdout


def test_canon_validation_rejects_duplicate_ids(project_root: Path) -> None:
    canon_path = project_root / "novel" / "bible" / "canon.yaml"
    entries = CANON_LIST_ADAPTER.validate_json(canon_path.read_text(encoding="utf-8"))
    entries.append(entries[0])
    _ = canon_path.write_bytes(CANON_LIST_ADAPTER.dump_json(entries, indent=2))

    result = run_script("validate_canon.py", ("--root", str(project_root)))

    assert result.returncode == 1
    assert "CANON_DUPLICATE_ID" in result.stdout


def test_timeline_validation_rejects_missing_cause(project_root: Path) -> None:
    event_path = project_root / "novel" / "state" / "events.jsonl"
    event = {
        "id": "EVT_CH001_99",
        "story_time": {"date": "0001-01-01", "start": "09:00", "end": "09:05"},
        "narrative_position": {"chapter": "CH001", "scene": 1},
        "location": "fog_harbor",
        "participants": ["char_hero"],
        "summary": "依赖不存在的前置事件",
        "causes": ["EVT_MISSING"],
        "effects": [],
        "knowledge_changes": [],
    }
    _ = event_path.write_text(
        json.dumps(event, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    result = run_script("validate_timeline.py", ("--root", str(project_root)))

    assert result.returncode == 1
    assert "TIMELINE_MISSING_CAUSE" in result.stdout


def test_clue_validation_rejects_paid_off_clue_without_payoff(project_root: Path) -> None:
    clue_path = project_root / "novel" / "state" / "clues.yaml"
    clues = CLUE_LIST_ADAPTER.validate_json(clue_path.read_text(encoding="utf-8"))
    clues[0] = clues[0].model_copy(update={"status": ClueStatus.PAID_OFF})
    _ = clue_path.write_bytes(CLUE_LIST_ADAPTER.dump_json(clues, indent=2))

    result = run_script("validate_clues.py", ("--root", str(project_root)))

    assert result.returncode == 1
    assert "CLUE_PAYOFF_REQUIRED" in result.stdout


def test_context_assembler_filters_secret_unknown_to_pov(project_root: Path) -> None:
    result = run_script("assemble_context.py", ("--root", str(project_root), "CH001"))

    context = (project_root / "novel" / "chapters" / "CH001" / "context.md").read_text(
        encoding="utf-8"
    )
    assert result.returncode == 0
    assert "港口每天午夜封航" in context
    assert "港务长就是失踪的守灯人" not in context
    assert "不得让主角提前知道守灯人的身份" in context


def test_committer_requires_approval_then_writes_state(project_root: Path) -> None:
    chapter_dir = project_root / "novel" / "chapters" / "CH001"
    final_path = chapter_dir / "final.md"

    rejected = run_script("commit_chapter.py", ("--root", str(project_root), "CH001"))

    assert rejected.returncode == 2
    assert final_path.read_text(encoding="utf-8").strip() == ""

    accepted = run_script(
        "commit_chapter.py",
        ("--root", str(project_root), "CH001", "--approved"),
    )
    status = STATUS_MAP_ADAPTER.validate_json(
        (project_root / "novel" / "state" / "workflow_status.yaml").read_text(encoding="utf-8")
    )
    clues = CLUE_LIST_ADAPTER.validate_json(
        (project_root / "novel" / "state" / "clues.yaml").read_text(encoding="utf-8")
    )

    assert accepted.returncode == 0
    assert final_path.read_text(encoding="utf-8") == chapter_dir.joinpath("draft.md").read_text(
        encoding="utf-8"
    )
    assert "EVT_CH001_01" in (project_root / "novel" / "state" / "events.jsonl").read_text(
        encoding="utf-8"
    )
    assert status["CH001"] is WorkflowStage.CANON_COMMITTED
    assert clues[0].status is ClueStatus.PLANTED


def test_committer_validates_pending_state_before_writing(project_root: Path) -> None:
    chapter_dir = project_root / "novel" / "chapters" / "CH001"
    manifest_path = chapter_dir / "commit_manifest.yaml"
    events_path = project_root / "novel" / "state" / "events.jsonl"
    final_path = chapter_dir / "final.md"
    manifest = MANIFEST_ADAPTER.validate_json(manifest_path.read_text(encoding="utf-8"))
    invalid_event = manifest.events[0].model_copy(update={"causes": ("EVT_UNKNOWN",)})
    invalid_manifest = manifest.model_copy(update={"events": (invalid_event,)})
    _ = manifest_path.write_bytes(MANIFEST_ADAPTER.dump_json(invalid_manifest, indent=2))
    events_before = events_path.read_text(encoding="utf-8")
    final_before = final_path.read_text(encoding="utf-8")

    result = run_script(
        "commit_chapter.py",
        ("--root", str(project_root), "CH001", "--approved"),
    )

    assert result.returncode == 1
    assert "TIMELINE_MISSING_CAUSE" in result.stdout
    assert events_path.read_text(encoding="utf-8") == events_before
    assert final_path.read_text(encoding="utf-8") == final_before
