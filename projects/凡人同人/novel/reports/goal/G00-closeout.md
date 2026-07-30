# G00 Closeout

- Stage: `G00`
- Goal: 冻结立项决策和执行基线；只分析八项立项问题，不推进正史、人物、大纲或正文。
- Started from: `workflow_status.yaml` 中 `PROJECT: IDEA`、`CH001: IDEA`；项目内不存在上游 Goal closeout 或 Author gate。
- Input hashes:
  - `AGENTS.md`: `db9823e176275065f11f05116874bb888127cb4f0959234876c9b2bb0a7ea53d`
  - `docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md`: `c075513db4eecf6d0e12c6c04ce0d3b5f158dd19406a8652d52f51908801866a`
  - `novel/state/workflow_status.yaml`: `ef82f925c1473bafdbae8ef0568f54c3cc6839b7c95f1c57c1196cbbfccf4d35`
  - `source/凡人_轮回韩立同人设定集与长篇大纲_v1.1增补版.md`: `ddec1e0ec09d393eddbe17f6b53d0bb02bfde740bb53625aa9bc762a9751d587`
  - `novel/brief/premise.md`: `df63fa73cff45b05259bf84941a03833285f6b501527cd7fd7743d2f38bb8806`
  - `novel/brief/project_brief.md`: `9be527f88936ed14b84309f3d2ea0db31e94d79b8b17afdc701c17e67c98bdc8`
  - `novel/brief/style_bible.yaml`: `2bf7bb1dac4f5379038998e2bc5cf9ba724587a798bf488688a0ecb6bc452ca5`
- Skills used:
  - `novel-orchestrator`: 启动门禁、阶段识别、DRA 触发和收束。
  - `chapter-committer`: 仅读取合同并确认本阶段禁止调用；未执行。
  - `scene-writer`: 仅读取合同并确认本 Goal 禁止调用；未执行。
  - `teammode`: 检查 Agent 工具面；MultiAgentV2 不可用，采用用户明确授权的 Codex App 独立 DRA 线程回退。
- Subagents used:
  - `Decision Research Agent` -> 独立读取项目、检索互联网、比较八项立项决策并逐项推荐 -> thread `019fb318-59dd-7531-af73-076a8b2c7429`
- Peak active subagents: `1`
- Delegation benefit: G00 合同强制使用新的独立 DRA；其独立外部核验覆盖版权、平台与 AI 标识，收益明显高于协调成本。
- Complex-design trigger: `NOT_TRIGGERED`。G00 是决策研究阶段，不生成复杂情节候选。
- Independent ideation reports: `NONE`
- Independent review report: `NONE`
- Decision IDs:
  - `DEC-G00-TITLE`
  - `DEC-G00-LENGTH`
  - `DEC-G00-OPENING`
  - `DEC-G00-POV`
  - `DEC-G00-WORDCOUNT`
  - `DEC-G00-PUBLISHING`
  - `DEC-G00-ENDING`
  - `DEC-G00-ORIGINALS`
- DRA task/thread references: `019fb318-59dd-7531-af73-076a8b2c7429`
- Decision research reports: `novel/reports/decisions/DEC-G00-EIGHT-DECISIONS-research.md`
- Subagent pre/post project hash comparison:
  - Algorithm: 对 `projects/凡人同人` 全部文件按相对路径排序，拼接 `path<TAB>SHA-256` 后再计算 SHA-256。
  - Pre file count: `33`
  - Pre aggregate: `3e2a3c19d5969c69df7ff695a500a3281e243cc3223f26417bb7303af59d4d1c`
  - Post file count: `33`
  - Post aggregate: `3e2a3c19d5969c69df7ff695a500a3281e243cc3223f26417bb7303af59d4d1c`
  - Verdict: `MATCH`；DRA 未修改项目文件，也未递归委派。
- Allowed writes:
  - `novel/reports/goal/G00-closeout.md`
  - `novel/reports/goal/G00-decision-packet.md`
  - `novel/reports/decisions/DEC-G00-*-research.md`
- Actual writes:
  - `novel/reports/goal/G00-closeout.md`
  - `novel/reports/goal/G00-decision-packet.md`
  - `novel/reports/decisions/DEC-G00-EIGHT-DECISIONS-research.md`
- Forbidden areas checked:
  - `source/`: 未修改。
  - `novel/brief/`: 未修改。
  - `novel/bible/`: 未修改。
  - `novel/characters/`: 未修改。
  - `novel/outline/`: 未修改。
  - `novel/chapters/`: 未修改；未生成或填写任何 `draft.md`、`final.md`。
  - `novel/state/`: 未修改；`workflow_status.yaml` 保持 `IDEA`。
  - 未执行 Git commit、push、reset 或 checkout。

## Acceptance results

| Check | Evidence | Verdict |
|---|---|---|
| 从首个未批准阶段开始 | `workflow_status.yaml` 为 `IDEA`，且无既有 Goal closeout/Author gate | PASS |
| 基线项目校验 | `.\.tools\uv\uv.exe run scripts\validate_project.py --root "D:\codes\bookMaker\projects\凡人同人"` 输出 `PROJECT_OK`，exit `0` | PASS |
| 八项决策有唯一 ID 和明确选项 | `G00-decision-packet.md` 的八行决策表 | PASS |
| 八项均有独立 DRA 推荐 | `DEC-G00-EIGHT-DECISIONS-research.md`，Research status `RESEARCHED` | PASS |
| DRA 独立读取项目并检索互联网 | 报告的 Project evidence、Internet evidence 和 Source list | PASS |
| 至少两个独立互联网来源 | 著作权法、网信办标识办法、起点官方页面等 6 个来源 | PASS |
| 420/430 与 3—5/8 冲突显式指出 | decision packet 的“冲突与联动” | PASS |
| 项目事实、外部事实、推断和创作建议分开 | DRA 各决策 Rationale 与 Internet evidence | PASS |
| A/B/C/D 边界明确 | DRA 报告与 decision packet 的权威边界表 | PASS |
| 未修改项目权威文件 | G00 写入前 Git 状态无相关变更；写入后 `git status --porcelain --untracked-files=all -- projects/凡人同人` 仅列出 3 个 G00 allowlist 报告 | PASS |
| 验收包含输入 Hash 和下一阶段边界 | 本 closeout 的 Input hashes 与 Next-stage handoff | PASS |

## Automatic loop history

| Round | Failure hypothesis | Action | New evidence |
|---|---|---|---|
| 0 | 项目可能已有批准阶段或机械错误 | 读取状态、库存并运行基线校验 | 无阶段报告；`PROJECT_OK`；确定 G00 |
| 1 | DRA 可能越过只读合同 | 启动前后对 33 个项目文件计算聚合 Hash | 前后聚合 Hash 完全一致 |
| 2 | DRA 线程引用可能记录错误 | 主 Agent核对 Codex task 返回和会话 ID，在研究报告追加编排备注 | 实际 DRA thread 固定为 `019fb318-59dd-7531-af73-076a8b2c7429` |

## Unresolved decisions

作者必须逐项裁决以下八项：

1. `DEC-G00-TITLE`
2. `DEC-G00-LENGTH`
3. `DEC-G00-OPENING`
4. `DEC-G00-POV`
5. `DEC-G00-WORDCOUNT`
6. `DEC-G00-PUBLISHING`
7. `DEC-G00-ENDING`
8. `DEC-G00-ORIGINALS`

其中 `DEC-G00-PUBLISHING` 的 DRA 推荐为附条件方案：授权或平台明确权利审核前保持私有，正式上传与签约当日重新核验权利、平台和 AI 标识规则。

## Risks and deviations

- DRA 使用 Codex App 独立任务线程，而非不可用的 MultiAgentV2；这是工具面回退，仍满足“新线程、独立读取、只读、无递归委派”。
- DRA 原始报告误记了 Agent thread 字段；主 Agent只追加编排备注并保留其推荐。
- `DEC-G00-PUBLISHING` 涉及法律与平台时效性；报告是决策研究，不是法律意见。真正发布和签约前必须重新核验。
- G00 不触发复杂情节设计闭环；没有为填满配额额外派发 Agent。

## Next-stage handoff

- Next stage: `G01`
- Required author decision:
  - 对八个 `DECISION_ID` 分别给出 `ACCEPT_RECOMMENDATION`、`OVERRIDE`、`DEFER` 或 `REJECT`。
  - 只有阻塞 G01 的全部决策均已明确解决，且作者明确批准 G00，才允许启动 G01。
- Files the next stage may trust after Author gate:
  - `novel/reports/goal/G00-decision-packet.md`
  - `novel/reports/decisions/DEC-G00-EIGHT-DECISIONS-research.md`
  - `novel/reports/goal/G00-closeout.md`
- G01 boundary after approval:
  - 先向本 closeout 追加 `## Author gate`。
  - 只使用 `canon-manager`、`timeline-manager` 和 G01 合同允许的只读调研/评审 Agent。
  - 只生成 CH000 正史候选；不得提交 CH000，不得进入 G02。

## Verdict

READY_FOR_HUMAN_REVIEW

## Author gate

- Decision: APPROVED
- Decision resolutions:
  - `DEC-G00-TITLE` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-LENGTH` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-OPENING` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-POV` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-WORDCOUNT` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-PUBLISHING` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-ENDING` -> `ACCEPT_RECOMMENDATION`
  - `DEC-G00-ORIGINALS` -> `ACCEPT_RECOMMENDATION`
- Conditions:
  - G01 不得扩大阶段边界。
  - `DEC-G00-PUBLISHING` 的推荐条件继续有效：授权或平台明确权利审核前保持私有；正式上传与签约当日重新核验权利、平台和 AI 标识规则。
- Recorded from: 当前用户消息“裁决 G00 的全部八项 DECISION_ID：ACCEPT_RECOMMENDATION。批准 G00。允许进入 G01，不得扩大 G01 边界。”
