---
name: chapter-committer
description: 作为唯一写入口提交人工批准的章节，并回写摘要、事件、正史、人物状态、线索状态和门禁。用于章节状态已为 HUMAN_APPROVED 且 commit_manifest.yaml 完整时；无明确 --approved 时必须拒绝。
---

# 章节定稿提交

## 前置条件

- `draft.md` 非空。
- 连续性、剧情和文风审校已通过。
- 作者完成最终定稿。
- `commit_manifest.yaml` 的章节 ID 正确且状态为 `HUMAN_APPROVED`。
- 所有新增事实都附有章节证据或批准依据。

## 预检

```powershell
.tools\uv\uv.exe run scripts\validate_project.py --root .
```

## 提交

```powershell
.tools\uv\uv.exe run scripts\commit_chapter.py CH001 --approved --root .
```

该入口会：

1. 把草稿写入 `final.md`。
2. 追加章节摘要和事件。
3. 应用已批准的正史、人物和线索变化。
4. 把章节门禁更新为 `CANON_COMMITTED`。
5. 写入变更日志并重新运行三类机械校验。

## 禁止

- 没有 `--approved` 时拒绝。
- 不接受重复事件或正史 ID。
- 不接受不存在的人物或线索。
- 不允许其他 Skill 直接模拟该提交。
