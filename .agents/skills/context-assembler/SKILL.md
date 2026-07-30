---
name: context-assembler
description: 为指定章节或场景构造有限、相关、分层的上下文包。用于写作前召回项目简报、卷目标、章节卡、POV 人物、相关正史、线索、最近记忆、文风和负信息；会过滤当前 POV 不应知道的 SECRET。
---

# 上下文组装

## 运行

```powershell
.tools\uv\uv.exe run scripts\assemble_context.py CH001 --root .
```

输出到 `novel/chapters/CH001/context.md`。

## 组装顺序

1. 项目简报和核心创意。
2. 当前卷目标。
3. 已批准章节卡。
4. 当前 POV 人物状态和语言指纹。
5. `canon_refs` 指向且当前可见的正史。
6. `clue_refs` 指向的线索状态。
7. 最近三章摘要。
8. Style Bible。
9. 禁止事项、未知事实、退休设定和退出位置。

## 边界

- 不无差别载入整本小说。
- `SECRET` 只有当前 POV 在 `known_by` 中才可显示真相。
- `RETIRED` 只作为负信息出现。
- 上下文包是可再生文件，不是新的权威数据源。
- 发现缺失引用时停止写作，先交给相应管理 Skill。
