---
name: character-manager
description: 维护人物卡、有向关系、角色知识、伤势、位置、物品、目标和语言指纹。用于创建或审查人物、检查人物是否失真、确认角色在某章知道什么，以及准备章节提交后的状态变化；正式回写必须经过批准。
---

# 人物状态管理

## 权威输入

- `novel/characters/characters.yaml`
- `novel/characters/relationships.yaml`
- `novel/state/character_state.yaml`
- `novel/state/knowledge_state.yaml`
- `novel/state/items.yaml`

## 工作流

1. 识别目标人物和当前章节。
2. 查询当前目标、错误信念、压力策略、语言指纹和知识边界。
3. 比较章节开场与结尾的状态变化。
4. 检查角色行动是否基于其已有信息和可用资源。
5. 对关系使用有方向的边，分别记录 A 对 B 与 B 对 A。
6. 输出状态差异或变更提案；经批准后交给 `$chapter-committer`。

## 保护项

- 不让角色说出尚未获知的信息。
- 不用性格标签代替可观察行为。
- 不在人物卡中悄悄决定重大生死、背叛或价值转向。
- 不因润色改变人物的选择和关系结论。
