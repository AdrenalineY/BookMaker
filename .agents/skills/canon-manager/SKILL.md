---
name: canon-manager
description: 管理小说正史、设定依赖和变更提案。用于查询某项设定、检查章节是否违反正史、分析新增规则的影响、处理 CANON/PLANNED/RUMOR/SECRET/RETIRED/UNKNOWN 状态；默认只报告，不直接修改正文或正史。
---

# 正史设定管理

## 权威输入

- `novel/bible/canon.yaml`
- `novel/state/world_state.yaml`
- `novel/state/knowledge_state.yaml`
- 用户指定的章节和正文证据

## 工作流

1. 用 `scripts/query_story_state.py` 检索 ID、同义词和依赖。
2. 读取正文证据，区分明确事实与模型推断。
3. 检查受影响人物、事件、线索、物品和大纲节点。
4. 运行 `scripts/validate_canon.py`。
5. 输出冲突、影响、证据和最小修复方案。
6. 新设定先形成 `PLANNED` 变更提案。
7. 只有作者批准后，才把变更交给 `$chapter-committer`。

## 禁止

- 不把角色传闻当客观事实。
- 不让 `SECRET` 自动进入当前 POV 上下文。
- 不改写已有 `CANON` 以迁就新草稿。
- 不直接编辑定稿章节。

## 输出

写入 `novel/reports/canon/`，每项问题包含 ID、两侧证据、严重程度、影响范围和建议动作。
