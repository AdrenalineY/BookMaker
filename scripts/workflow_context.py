from __future__ import annotations

from pathlib import Path
from typing import assert_never

from pydantic import TypeAdapter

from workflow_io import load_json, load_jsonl
from workflow_models import (
    CanonEntry,
    CanonStatus,
    ChapterCard,
    ChapterSummary,
    CharacterEntry,
    ClueEntry,
)

CHAPTER_ADAPTER = TypeAdapter(ChapterCard)
CANON_ADAPTER = TypeAdapter(tuple[CanonEntry, ...])
CHARACTER_ADAPTER = TypeAdapter(tuple[CharacterEntry, ...])
CLUE_ADAPTER = TypeAdapter(tuple[ClueEntry, ...])
SUMMARY_ADAPTER = TypeAdapter(ChapterSummary)


def assemble_context(root: Path, chapter_id: str) -> Path:
    novel = root / "novel"
    chapter_dir = novel / "chapters" / chapter_id
    card = load_json(chapter_dir / "chapter_card.yaml", CHAPTER_ADAPTER)
    canon = load_json(novel / "bible" / "canon.yaml", CANON_ADAPTER)
    characters = load_json(novel / "characters" / "characters.yaml", CHARACTER_ADAPTER)
    clues = load_json(novel / "state" / "clues.yaml", CLUE_ADAPTER)
    summaries = load_jsonl(novel / "state" / "chapter_summaries.jsonl", SUMMARY_ADAPTER)

    canon_by_id = {entry.id: entry for entry in canon}
    clue_by_id = {entry.id: entry for entry in clues}
    related_characters = tuple(entry for entry in characters if entry.id == card.pov)
    visible_canon: list[CanonEntry] = []
    protected_facts: list[str] = []
    for reference in card.canon_refs:
        entry = canon_by_id.get(reference)
        if entry is None:
            continue
        match entry.status:
            case CanonStatus.SECRET:
                if card.pov in entry.known_by:
                    visible_canon.append(entry)
                else:
                    protected_facts.append(f"{entry.id}：该真相对当前 POV 保密")
            case CanonStatus.RETIRED:
                protected_facts.append(f"{entry.id}：已退休设定，不得继续使用")
            case CanonStatus.CANON | CanonStatus.PLANNED | CanonStatus.RUMOR | CanonStatus.UNKNOWN:
                visible_canon.append(entry)
            case unreachable:
                assert_never(unreachable)

    sections = [
        f"# {chapter_id} 上下文包",
        "## 最高层创作简报",
        (novel / "brief" / "project_brief.md").read_text(encoding="utf-8").strip(),
        (novel / "brief" / "premise.md").read_text(encoding="utf-8").strip(),
        "## 当前卷目标",
        (novel / "outline" / "volume_01.md").read_text(encoding="utf-8").strip(),
        "## 当前章节卡",
        card.model_dump_json(indent=2),
        "## 当前 POV 人物",
        "\n".join(entry.model_dump_json(indent=2) for entry in related_characters)
        or "未找到人物卡",
        "## 可用正史",
        "\n".join(entry.model_dump_json(indent=2) for entry in visible_canon)
        or "本章没有已授权正史条目",
        "## 相关线索",
        "\n".join(
            f"- {clue.id}：状态 {clue.status.value}；真相仅供规划，不得越过知识边界"
            for clue_id in card.clue_refs
            if (clue := clue_by_id.get(clue_id)) is not None
        )
        or "本章没有线索引用",
        "## 最近记忆",
        "\n".join(f"- {item.chapter_id}：{item.summary}" for item in summaries[-3:])
        or "尚无已提交章节摘要",
        "## 负信息与禁止事项",
        "\n".join(f"- {item}" for item in (*card.must_avoid, *protected_facts)) or "无",
        "## 文风规约",
        (novel / "brief" / "style_bible.yaml").read_text(encoding="utf-8").strip(),
        "## 输出边界",
        f"只处理 {chapter_id} 当前指定场景；不得新增改变主线的正史事实。",
    ]
    target = chapter_dir / "context.md"
    _ = target.write_text(
        "\n\n".join(sections) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return target
