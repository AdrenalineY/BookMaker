# 小说项目操作规则

文档和小说资料主要使用中文，所有文本文件以 UTF-8 读写。Windows 环境使用 PowerShell 原生命令，不使用 `rg`。

## 权威数据源

- `novel/bible/` 保存世界观和正史；`CANON` 不得被草稿或旧大纲覆盖。
- `novel/characters/` 保存人物长期设定；`novel/state/` 保存最近定稿后的当前状态。
- `novel/outline/` 只有标记为 `APPROVED` 的计划具有约束力。
- 已进入 `final.md` 的正文事实优先于尚未执行的大纲；`RETIRED` 内容不得继续使用。
- `.yaml` 使用 JSON 兼容 YAML 语法并保持 UTF-8，便于脚本确定性解析。

## 修改纪律

- 未经作者明确批准，不得把 `PLANNED` 升级为 `CANON`。
- 不得直接覆盖已经定稿的 `final.md`。
- 正文修改前先生成问题报告；文笔编辑只修复作者批准的问题 ID。
- 审校只读，正式修改串行执行；章节和状态只能由 `chapter-committer` 提交。
- Subagents 默认禁用。除非作者在当前任务中明确要求，不得派发 Subagent。
- 敏感内容、关键反转、人物生死、主题结论和最终语言定稿必须由作者确认。

## 章节流程

1. `$chapter-planner` 建立章节卡和场景卡。
2. `$context-assembler` 组装有限上下文。
3. `$scene-writer` 逐场景写入 `draft.md`。
4. `$continuity-reviewer`、剧情检查和 `$prose-editor` 只读审校。
5. 作者批准定稿和 `commit_manifest.yaml`。
6. `$chapter-committer` 回写正文、摘要、事件、人物、线索和正史。
7. `$outline-planner` 更新未来三至五章滚动计划。

## 校验命令

```powershell
.tools\uv\uv.exe run scripts\validate_project.py --root .
.tools\uv\uv.exe run pytest
.tools\uv\uv.exe run ruff check .
.tools\uv\uv.exe run basedpyright
```

## git 管理

若没有用户明确说明推送产物到 github，则不得自行推送 commit
