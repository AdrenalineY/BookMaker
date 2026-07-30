---
name: clue-manager
description: 管理线索与伏笔的种植、推进、误导、兑现和作废，并分离客观真相、角色认知和读者认知。用于检查伏笔遗漏、提前泄露、无铺垫反转、长期不推进或生命周期非法；批准前只报告。
---

# 线索与伏笔管理

## 权威输入

- `novel/state/clues.yaml`
- `novel/state/knowledge_state.yaml`
- `novel/outline/thread_ledger.yaml`
- 相关章节正文

## 工作流

1. 运行 `.tools/uv/uv.exe run scripts/validate_clues.py --root .`。
2. 核对状态流：`PLANNED → PLANTED → PROGRESSING → PAID_OFF`，或进入 `ABANDONED`。
3. 检查种植位置、推进记录、计划兑现范围和实际兑现证据。
4. 对比角色知道什么、读者知道什么、客观真相是什么。
5. 标记提前泄露、重复解释、无公平证据和作废后继续推进。
6. 输出变更提案；正式回写交给 `$chapter-committer`。

## 禁止

- 不为了制造神秘感无限新增线索。
- 不把误导写成作者欺骗。
- 不让回收依赖临时新增的规则。
