from __future__ import annotations

from enum import StrEnum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, RootModel


class FrozenModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class CanonStatus(StrEnum):
    CANON = "CANON"
    PLANNED = "PLANNED"
    RUMOR = "RUMOR"
    SECRET = "SECRET"
    RETIRED = "RETIRED"
    UNKNOWN = "UNKNOWN"


class ClueStatus(StrEnum):
    PLANNED = "PLANNED"
    PLANTED = "PLANTED"
    PROGRESSING = "PROGRESSING"
    PAID_OFF = "PAID_OFF"
    ABANDONED = "ABANDONED"


class WorkflowStage(StrEnum):
    IDEA = "IDEA"
    BIBLE_APPROVED = "BIBLE_APPROVED"
    OUTLINE_APPROVED = "OUTLINE_APPROVED"
    CHAPTER_PLANNED = "CHAPTER_PLANNED"
    DRAFTED = "DRAFTED"
    CONTINUITY_PASSED = "CONTINUITY_PASSED"
    STORY_PASSED = "STORY_PASSED"
    STYLE_PASSED = "STYLE_PASSED"
    HUMAN_APPROVED = "HUMAN_APPROVED"
    CANON_COMMITTED = "CANON_COMMITTED"


class Evidence(FrozenModel):
    chapter: str
    location: str


class CanonEntry(FrozenModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    status: CanonStatus
    statement: str = Field(min_length=1)
    dependencies: tuple[str, ...] = ()
    known_by: tuple[str, ...] = ()
    evidence: tuple[Evidence, ...] = ()


class StoryTime(FrozenModel):
    date: str
    start: str
    end: str


class NarrativePosition(FrozenModel):
    chapter: str
    scene: int = Field(ge=1)


class KnowledgeChange(FrozenModel):
    character: str
    learns: tuple[str, ...] = ()


class EventEntry(FrozenModel):
    id: str = Field(min_length=1)
    story_time: StoryTime
    narrative_position: NarrativePosition
    location: str
    participants: tuple[str, ...] = ()
    summary: str
    causes: tuple[str, ...] = ()
    effects: tuple[str, ...] = ()
    knowledge_changes: tuple[KnowledgeChange, ...] = ()


class ClueMoment(FrozenModel):
    chapter: str
    change: str


class PlannedPayoff(FrozenModel):
    chapter_range: str


class ClueEntry(FrozenModel):
    id: str = Field(min_length=1)
    truth: str
    status: ClueStatus
    planted: ClueMoment | None = None
    progress: tuple[ClueMoment, ...] = ()
    planned_payoff: PlannedPayoff | None = None
    payoff: ClueMoment | None = None
    known_by: tuple[str, ...] = ()
    reader_knows: tuple[str, ...] = ()
    must_not_reveal_before: str | None = None


class VoiceProfile(FrozenModel):
    sentence_length: str
    avoid: tuple[str, ...] = ()


class CharacterEntry(FrozenModel):
    id: str
    name: str
    role: str
    goals: tuple[str, ...] = ()
    knowledge: tuple[str, ...] = ()
    voice: VoiceProfile


class CharacterState(FrozenModel):
    character_id: str
    location: str
    physical: str
    emotional: str
    inventory: tuple[str, ...] = ()
    goals: tuple[str, ...] = ()
    knowledge: tuple[str, ...] = ()


class ChapterCard(FrozenModel):
    chapter_id: str
    title: str
    status: WorkflowStage
    pov: str
    time: str
    locations: tuple[str, ...]
    goal: str
    opening_state: str
    ending_state: str
    canon_refs: tuple[str, ...] = ()
    clue_refs: tuple[str, ...] = ()
    must_include: tuple[str, ...] = ()
    must_avoid: tuple[str, ...] = ()


class CharacterUpdate(FrozenModel):
    character_id: str
    location: str
    emotional: str
    goals: tuple[str, ...] = ()
    knowledge_add: tuple[str, ...] = ()


class ClueUpdate(FrozenModel):
    clue_id: str
    status: ClueStatus
    chapter: str
    change: str


class CommitManifest(FrozenModel):
    chapter_id: str
    status: WorkflowStage
    summary: str
    events: tuple[EventEntry, ...] = ()
    canon_changes: tuple[CanonEntry, ...] = ()
    character_updates: tuple[CharacterUpdate, ...] = ()
    clue_updates: tuple[ClueUpdate, ...] = ()


class ChapterSummary(FrozenModel):
    chapter_id: str
    summary: str


class WorkflowStatusMap(RootModel[dict[str, WorkflowStage]]):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
