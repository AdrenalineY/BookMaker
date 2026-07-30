---
name: timeline-manager
description: 检查或维护小说的客观时间、叙述顺序、角色认知时间和因果前置。用于事件排序、人物移动、物品出现、伤势恢复、知识获得、回忆或时间能力自洽性审查；默认只生成报告，不修改正文。
---

# 时间线管理

## 权威输入

- `novel/state/events.jsonl`
- `novel/state/character_state.yaml`
- `novel/state/knowledge_state.yaml`
- `novel/bible/timeline_rules.yaml`
- 用户指定章节

## 工作流

1. 运行 `.tools/uv/uv.exe run scripts/validate_timeline.py --root .`。
2. 区分故事时间、叙述位置、认知时间和因果时间。
3. 检查重复事件 ID、失效原因引用和结果早于原因。
4. 语义检查同一人物同时出现在两地、移动耗时、物品获得时机和知识泄露。
5. 为每项问题给出事件证据、章节证据、严重程度和最小修复方案。

## 输出

写入 `novel/reports/timeline/<chapter-id>.md`。正式事件只由 `$chapter-committer` 写入。
