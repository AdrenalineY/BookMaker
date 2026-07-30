# G01 Closeout：正史与时间线候选基线

## 1. Stage identity

- Stage：`G01`
- Stage name：正史与时间线候选基线
- Started from：G00 Author gate `APPROVED`
- Scope：仅 G01
- Completed at：2026-07-30
- Verdict：`READY_FOR_HUMAN_REVIEW`
- Author gate：`PENDING`

本阶段没有调用 `chapter-committer`，没有把 CH000 提交到正式正史、事件或工作流状态；没有进入 G02。

## 2. Input hashes

### 权威输入

| 输入 | SHA-256 |
|---|---|
| `AGENTS.md` | `db9823e176275065f11f05116874bb888127cb4f0959234876c9b2bb0a7ea53d` |
| `docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md` | `c075513db4eecf6d0e12c6c04ce0d3b5f158dd19406a8652d52f51908801866a` |
| `novel/reports/goal/G00-closeout.md`（含 Author gate） | `932aa6477f738e38067d2d8cfa4bf595bcfbc4ddbd8da5d9f93976dc0a65b6cf` |
| `novel/reports/goal/G00-decision-packet.md` | `f76cdcf59675d645e8ed0de19b3e09b7ecc88350e019f6cacbb35337d9109257` |
| `novel/reports/decisions/DEC-G00-EIGHT-DECISIONS-research.md` | `5eac0cacf38b15403f18faa4ee1df6994acb4c7d35489b07301e59b19b894a3f` |
| `source/凡人_轮回韩立同人设定集与长篇大纲_v1.1增补版.md` | `ddec1e0ec09d393eddbe17f6b53d0bb02bfde740bb53625aa9bc762a9751d587` |
| `novel/state/workflow_status.yaml` | `ef82f925c1473bafdbae8ef0568f54c3cc6839b7c95f1c57c1196cbbfccf4d35` |
| `novel/schemas/commit-manifest.schema.json` | `2cbefdee9218fc7252bb8da970cf9419d9e8d653b61eefb66b2759ca91e8249d` |

### 阶段起始项目快照

- File count：36
- Aggregate SHA-256：`01aedf1ef71f82c6cc740f87a81071407ce4041af9c5cf57e0de32dec597e975`
- 起始校验：`PROJECT_OK`、`CANON_OK`、`TIMELINE_OK`

## 3. Output inventory and hashes

| 产物 | SHA-256 | 作用 |
|---|---|---|
| `novel/brief/premise.md` | `965efe7f10477584d0156c7a80a424a32c162eefde2f6701492265a7b44242f0` | 回写 G00 八项批准决定并分离原著事实/项目选择 |
| `novel/brief/project_brief.md` | `40a304ae41ed8590996fc41c250f43dc8c424a505175324617a1c88e12b4c588` | 冻结项目合同；把长期大罗明确列为 B 级强推定 |
| `novel/brief/style_bible.yaml` | `c7c3037800615ecdf2211f9d5ee3a2e49d11b7e26fa447181b5209885dac3243` | JSON 兼容 YAML；回写 POV、篇幅、发布、结局与原创边界 |
| `novel/bible/timeline_rules.yaml` | `1cbc4f020aaa281b3caef4a9436333173dcbac6f3a7ce110d9b00da29fdc0ec9` | 双时间线、因果账本、角色知识与能力边界候选 |
| `novel/chapters/CH000/draft.md` | `759531dd28b43e6d4997a276b6cfb3dd0c72a18557f253294b2f67cc30df29cf` | 项目基线摘要；明确非小说正文 |
| `novel/chapters/CH000/commit_manifest.yaml` | `4e6b101479438e5f08af8b5fef1779f81a45c8c9545f3bcf774ddb5977297dac` | 待作者批准的 CH000 正史/事件候选 |
| `novel/reports/canon/G01-anchor-research.md` | `61ce68528b6ac8fad495007286730cbaa0f5dded655e4dbf2d12e80851b5fcc7` | 广泛调研与证据缺口记录 |
| `novel/reports/canon/G01-independent-review-01.md` | `97764a492b52bfe5dfbbc77d8a2f35105f35e89c7cb2a80d88432d61d119d096` | 首轮独立 FAIL 证据 |
| `novel/reports/canon/G01-independent-review-02.md` | `426d1bfe1b40a8764d03847f6d3b8f3f1aec93a05881824d2d104a1867c1e163` | 修复后终审 FAIL 证据 |
| `novel/reports/canon/G01-independent-review-03.md` | `3394025d86accbf89834cf4bcfbfef77b9782a9b3d72cc0a620c668d35d1f035` | 第三次全新独立终审 PASS |

写入均位于 G01 allowlist：

- `novel/brief/`
- `novel/bible/timeline_rules.yaml`
- `novel/chapters/CH000/`
- `novel/reports/canon/`
- `novel/reports/goal/G01-closeout.md`

## 4. Candidate summary

### CH000

- `chapter_id`：`CH000`
- 状态：`STYLE_PASSED`
- Author approval：未记录
- Events：17
- Canon changes：29
- Character updates：0
- Clue updates：0
- 小说正文：无

### 正史分级

- H01—H31：31/31 可追溯。
- H08：瓶灵孕育与首次真正逆转时空保留为 A 候选。
- H09：三类力量均被涉及为 A 候选；精确耦合机制为 `UNKNOWN`。
- H14：法宝/功力/可调用战力归零为 A 候选；其余底蕴保留度为 `UNKNOWN`。
- H27：轮回殿最终跨域能力为 A 候选；形成机制为 `PLANNED`。
- H31：自身牺牲参与击杀为 A 候选；克制开放尾声为 G00 已批准 D 级项目合同。
- “长期停留大罗巅峰”：B 级强推定；不得冒充原著单句。

### 时间与知识

- 第一次时间线、穿越点、远古第二阶段、现世交汇、终战五段已建立。
- ISO 日期仅为跨时空因果账本序号，不是仙界绝对历法。
- 现世韩立出生只依赖远古历史已被改变，不依赖轮回殿建立。
- 寻回甘九真与现世韩立出生的相对先后保持 `UNKNOWN`，两者分别汇入正式交汇。
- 29/29 候选均有公开/知情矩阵记录。
- `known_by` 只含稳定人物名或角色组；否定知识不作为 `learns` 伪增量。

## 5. Validation results

### 强制校验

| 校验 | 结果 |
|---|---|
| `scripts/validate_project.py --root projects/凡人同人` | `PROJECT_OK` |
| `scripts/validate_canon.py --root projects/凡人同人` | `CANON_OK` |
| `scripts/validate_timeline.py --root projects/凡人同人` | `TIMELINE_OK` |
| CH000 `CommitManifest` Pydantic 解析 | PASS |
| CH000 candidate canon dependency/evidence audit | PASS |
| CH000 candidate timeline cause audit | PASS |
| JSON-compatible YAML parse | PASS |

### 仓库补充校验

| 校验 | 结果 |
|---|---|
| pytest | 10 passed |
| ruff | All checks passed |
| basedpyright | 0 errors、0 warnings、0 notes |

### Negative boundary

- 正式 `canon.yaml` 未改变：SHA-256 `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`
- 正式 `events.jsonl` 未改变：SHA-256 `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`
- `workflow_status.yaml` 未改变：SHA-256 `ef82f925c1473bafdbae8ef0568f54c3cc6839b7c95f1c57c1196cbbfccf4d35`
- `PROJECT=IDEA`，`CH001=IDEA`
- `CH001/draft.md`：0 bytes
- `CH001/final.md`：1 byte（既有换行）
- G02 命名产物：0
- CH000 未达到 `HUMAN_APPROVED`
- 未调用 `chapter-committer`
- 未启动 C001-W，未调用 `scene-writer`

## 6. Subagent usage record

任一时刻活跃 subagent 数不超过 1，均只读、无项目写入、无下级派发。

| Role | Thread | 网络 | Verdict / 结果 | 零写入证据 |
|---|---|---|---|---|
| Project + External Researcher | `019fb334-9d0e-7c01-bd09-d5d322f4bb6f` | 必要官方来源检索 | `RESEARCHED_WITH_GAPS` | 36 files；aggregate 前后均 `01aedf1e…597e975` |
| Independent Canon + Timeline Reviewer 01 | `019fb347-ff3a-7653-b9b4-b39325f7e050` | 无 | `FAIL`：2 MAJOR、1 MINOR | 39 files；aggregate 前后均 `b5470e2a…17d0b4e2` |
| Independent Final Reviewer 02 | `019fb356-c055-7f02-b610-c1471382f72a` | 无 | `FAIL`：1 MAJOR、1 MINOR | 40 files；aggregate 前后均 `83241f50…629407ad` |
| Independent Final Reviewer 03 | `019fb366-69b0-7ea3-b1a4-2f6b40ee2e95` | 无 | `PASS`：无 actionable findings | 41 files；aggregate 前后均 `788fd7e0…38fd637c` |

失败报告原样保留；修复后使用新的独立 Reviewer，不把旧 FAIL 改写成 PASS。

## 7. DRA and pending decisions

- 本阶段新增 `DECISION_ID`：0
- 待作者裁决的内容问题：0
- DRA：未触发。原因是 G01 没有新增待决断问题；所有证据不足项均按合同保持 `UNKNOWN/PLANNED`，没有要求作者在本阶段选择具体方案。
- 当前唯一门禁：作者是否批准 G01 候选进入 G02。这是阶段 Author gate，不是新增内容决策。

保留但不阻塞 G01 的已披露未知：

1. 关键付费原著章节未由调研 Agent 独立读取全文；A 类候选以项目源设定及其章节索引为直接证据。
2. 战力归零后的记忆、道心、百艺、肉身与神魂精确保留度。
3. 幽冥阶段/正式建殿、弥罗节点/寻女节点的精确绝对顺序。
4. 六道轮回盘来源、铸造、六道胚与完整能力树。
5. 终战后轮回韩立意识状态。

## 8. Next-stage handoff

若且仅若作者明确批准 G01：

1. 在本 closeout 追加 G01 Author gate。
2. 进入 G02。
3. G02 使用 `chapter-committer` 把已批准的 CH000 从 `STYLE_PASSED` 提升到提交所需门禁并执行正式提交。
4. G02 提交前再次校验 manifest、输入 Hash 与正式状态。

作者若附条件批准或退回，只修复 G01，不得进入 G02。

## 9. Author gate

- Decision：`PENDING`
- Allowed responses：
  - 明确批准 G01；
  - 附条件批准 G01；
  - 退回 G01，并给出需修复的问题。

在 Author gate 变为 `APPROVED` 前，禁止提交 CH000，禁止进入 G02。
