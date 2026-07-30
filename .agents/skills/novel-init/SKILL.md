---
name: novel-init
description: 初始化新的文件型小说项目。用于“新建小说”“创建小说工作区”“复制空白模板”或检查项目是否具备 brief、bible、characters、outline、chapters、state、reports 和 schemas 目录；拒绝覆盖已有小说目录。
---

# 初始化小说项目

## 新建

1. 确认目标目录不含 `novel/`。
2. 运行：

```powershell
.tools\uv\uv.exe run scripts\init_novel_project.py <目标目录>
```

3. 进入目标目录，依次填写：
   - `novel/brief/project_brief.md`
   - `novel/brief/premise.md`
   - `novel/brief/style_bible.yaml`
4. 将示例 `CH001` 内容替换为新项目内容。
5. 运行 `scripts/validate_project.py`。

## 规则

- 不覆盖已有 `novel/`。
- `.yaml` 文件使用 JSON 兼容 YAML，保存为 UTF-8。
- 初始设定只能标记为 `PLANNED`、`UNKNOWN`、`RUMOR` 或 `SECRET`。
- 只有作者审批或正文证据才能产生 `CANON`。
- 初始化不生成整本正文，不替作者决定主题、关键反转和结局。

## 模板

复制源位于 `assets/novel-template/`。完成后输出目标路径、待填写清单和首次校验结果。
