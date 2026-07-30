from __future__ import annotations

import tomllib
from pathlib import Path

from pydantic import TypeAdapter

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ADAPTER = TypeAdapter(dict[str, object])
SKILL_NAMES = (
    "novel-orchestrator",
    "novel-init",
    "canon-manager",
    "character-manager",
    "timeline-manager",
    "clue-manager",
    "outline-planner",
    "chapter-planner",
    "context-assembler",
    "scene-writer",
    "continuity-reviewer",
    "prose-editor",
    "chapter-committer",
)
SCHEMA_NAMES = (
    "canon.schema.json",
    "event.schema.json",
    "clue.schema.json",
    "chapter-card.schema.json",
    "commit-manifest.schema.json",
    "character-state.schema.json",
)


def test_all_repo_skills_have_complete_machine_metadata() -> None:
    for name in SKILL_NAMES:
        skill_root = WORKSPACE_ROOT / ".agents" / "skills" / name
        skill_text = skill_root.joinpath("SKILL.md").read_text(encoding="utf-8")
        metadata_text = skill_root.joinpath("agents", "openai.yaml").read_text(encoding="utf-8")

        assert f"name: {name}" in skill_text
        assert "description:" in skill_text
        assert "TODO" not in skill_text
        assert "interface:" in metadata_text
        assert "$" + name in metadata_text


def test_optional_review_agents_are_present_but_disabled_by_default() -> None:
    config = tomllib.loads(
        WORKSPACE_ROOT.joinpath(".codex", "config.toml").read_text(encoding="utf-8")
    )
    agent_files = tuple(WORKSPACE_ROOT.joinpath(".codex", "agents").glob("*.toml"))

    assert config["agents"]["enabled"] is False
    assert len(agent_files) == 5
    for path in agent_files:
        agent = tomllib.loads(path.read_text(encoding="utf-8"))
        assert agent["sandbox_mode"] == "read-only"


def test_published_schemas_are_valid_json_schema_documents() -> None:
    schema_root = WORKSPACE_ROOT / "novel" / "schemas"
    for name in SCHEMA_NAMES:
        schema = SCHEMA_ADAPTER.validate_json(
            schema_root.joinpath(name).read_text(encoding="utf-8")
        )

        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["title"]
