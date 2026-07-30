---
name: novel-orchestrator
description: 小说创作工作流总控。用于开始或继续小说项目、判断当前质量门禁、回答“下一步做什么”、安排立项到章节定稿的完整流程；只调度专职 Skill 和汇总证据，不直接写正文或提交正史。
---

# 小说工作流总控

## 启动检查

1. 读取根目录 `AGENTS.md`。
2. 读取 `novel/state/workflow_status.yaml`。
3. 确认当前目标是立项、大纲、章节规划、写作、审校还是提交。
4. 运行 `.tools/uv/uv.exe run scripts/validate_project.py --root .`。
5. 若存在机械错误，先停止创作并路由到对应管理 Skill。

## 门禁路由

| 当前状态 | 下一步 |
|---|---|
| `IDEA` | 使用 `$canon-manager`、`$character-manager` 和 `$outline-planner` 完成立项资产 |
| `OUTLINE_APPROVED` | 使用 `$chapter-planner` 生成章节卡和场景卡 |
| `CHAPTER_PLANNED` | 使用 `$context-assembler`，经作者确认后再使用 `$scene-writer` |
| `DRAFTED` | 使用 `$continuity-reviewer`，再做剧情、人物和文笔审校 |
| `CONTINUITY_PASSED` / `STORY_PASSED` | 使用 `$prose-editor` 诊断，等待作者选择问题 ID |
| `STYLE_PASSED` | 等待作者人工定稿并生成 `commit_manifest.yaml` |
| `HUMAN_APPROVED` | 使用 `$chapter-committer` 进行唯一一次状态提交 |
| `CANON_COMMITTED` | 更新滚动大纲，进入下一章 |

## 纪律

- 每次只推进一个门禁。
- 写正文前必须有已批准章节卡和上下文包。
- 审校默认只读；不得让多个入口修改同一章。
- 未经作者明确批准，不得把 `PLANNED` 升级为 `CANON`。
- Subagents 默认禁用；除非作者明确要求，不得派发。
- 机械校验结果优先于模型推测，正文证据优先于摘要推断。

## 输出

返回当前状态、阻塞项、下一项唯一动作、需要作者批准的决策和将写入的文件。
