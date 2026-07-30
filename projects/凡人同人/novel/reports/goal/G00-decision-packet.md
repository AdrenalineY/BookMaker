# G00 立项决策包

- Stage: `G00`
- Project status: `IDEA`
- Prepared: `2026-07-30`
- Decision research: `novel/reports/decisions/DEC-G00-EIGHT-DECISIONS-research.md`
- DRA thread: `019fb318-59dd-7531-af73-076a8b2c7429`
- DRA gate recommendation: `APPROVE_WITH_CONDITIONS`
- Authority note: 本包是作者裁决材料，不构成作者批准、`CANON` 或正式状态。

## 需要作者逐项裁决

回复值只能是：

- `ACCEPT_RECOMMENDATION`
- `OVERRIDE`（同时提供作者方案和必须保护项）
- `DEFER`（同时说明延后到哪个阶段；阻塞下一阶段的事项不能延后）
- `REJECT`

| DECISION_ID | 中性问题 | 主要选项 | DRA 推荐 | 置信度 | 不可逆程度 |
|---|---|---|---|---|---|
| `DEC-G00-TITLE` | 正式书名采用哪一种？ | 当前工作标题、源暂定/备选、新标题 | 《一时二生：轮回韩立》；简介标明非官方同人 | MEDIUM | 发布前 LOW，发布后 HIGH |
| `DEC-G00-LENGTH` | 总章数按约 420 还是约 430？ | 420、430；390 为残留冲突 | 430 作为结构上限，不是凑章指标 | HIGH | G03 前 LOW，后期 HIGH |
| `DEC-G00-OPENING` | 大战采用 3—5 章短序章还是 8 章序卷？ | 3—5、8 | 4 章短序章，第 5 章进入远古落地 | HIGH | 发布后 HIGH |
| `DEC-G00-POV` | 正式 POV 合同是什么？ | 第三人称限知、全知、多 POV | 以轮回韩立为主的第三人称限知；仅极少量标记清楚的他人限知插章 | HIGH | HIGH |
| `DEC-G00-WORDCOUNT` | 总字数和单章字数如何冻结？ | 170—180 万、190—200 万、230—260 万 | 190—200 万；通常 4400—4700 字/章 | MEDIUM-HIGH | MEDIUM |
| `DEC-G00-PUBLISHING` | 平台、更新和授权边界是什么？ | 起点、番茄、其他社区、保持私有 | 授权核验前不公开；通过后首选起点，每周 6 更，至少 24 章合格存稿 | MEDIUM | 公开/签约后 HIGH |
| `DEC-G00-ENDING` | 牺牲式结局与开放尾声如何组合？ | 仅牺牲、牺牲+含混尾声、完整复活 | 牺牲+克制开放尾声；不确认人格完整延续或复活 | HIGH | HIGH |
| `DEC-G00-ORIGINALS` | 原创人物、宗门和落点是否沿用？ | 原样冻结、功能骨架+暂名、推翻重做 | 沿用功能骨架和暂名，保留改名/合并/删除权 | HIGH | MEDIUM |

## 冲突与联动

1. 源文档同时存在“约 390 章”“三阶段至 420 章”“详细卷表至 430 章”。DRA 推荐将 430 定义为上限，并在 G03 用场景预算验证，不允许凑章。
2. 源文档同时存在“3—5 章序章”和“第 1—8 章序卷”。DRA 推荐 4 章短序章，第 5 章进入“一颗下品灵石”。
3. 若接受 430 与 190—200 万字，平均 4400—4700 字/章在计算上自洽。
4. 若接受限知 POV，跨时代暗手不得由旁白提前确认成功；必要的他人 POV 必须少量、明确标记。
5. 若接受牺牲+开放尾声，开放性只能落在“是否进入轮回”，不能落在“是否完整复活”。
6. 若接受原创骨架，`沉星界`、`栖魂谷`、`沈归尘`、`宁小川`、`商九`、`闻烛` 仍只是工作名和 `PLANNED` 内容。

## 发布与权利条件

`DEC-G00-PUBLISHING` 的推荐带强制条件：

1. 在首次公开发布和平台签约当日重新核验权利、平台分类、AI 标识和合同规则。
2. 未取得覆盖预期使用方式的书面授权或平台明确权利审核结论前，保持私有。
3. “免费”“致敬”“非官方”、标注原作者和 AI 辅助创作都不是授权替代品。
4. 未取得相应授权前，不开启付费、签约分成、定向打赏、众筹、实体出版、音频/漫画/短剧/影视/游戏改编、周边、海外授权或再许可。

## A/B/C/D 权威边界

| 等级 | 处理规则 |
|---|---|
| A·原著明示 | 不得改写结果，只能补过程 |
| B·强推定 | 可调细节，不得破坏稳定结论 |
| C·原著留白 | 可大幅创作，但不能突破 A/B 边界 |
| D·同人建议 | 必须由作者批准，可改名、合并、删除 |

八项立项决策均属于 D 级项目合同；DRA 推荐不是作者批准。

## 作者回复模板

```text
裁决 G00 的待决断问题：

- DEC-G00-TITLE：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-LENGTH：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-OPENING：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-POV：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-WORDCOUNT：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-PUBLISHING：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-ENDING：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT
- DEC-G00-ORIGINALS：ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT

若为 OVERRIDE：
- 作者方案：
- 必须保护：

批准 G00。
该阶段所有阻塞性 DECISION_ID 已逐项裁决。
允许 G01 信任 G00 closeout 中列出的产物。
不得扩大 G01 边界。
```
