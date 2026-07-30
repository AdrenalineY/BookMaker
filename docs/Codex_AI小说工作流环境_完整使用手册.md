# Codex AI 小说工作流环境：完整使用手册

> 适用工作区：`D:\codes\bookMaker`  
> 基线文档：`docs/AI写小说的主流工作流程与工程化实践_2026版_CodexSkills增补版.md`  
> 环境版本：0.1.0  
> 文档日期：2026-07-29

## 1. 这套环境已经具备什么

本工作区已经落地一套可直接被 Codex Desktop、Codex CLI 或 IDE 扩展识别的文件型小说工程。它不是“一条提示词写整本书”，而是把长篇创作拆成四层：

1. **Codex Skills**：规定每类任务的流程、输入、输出和审批边界。
2. **小说项目文件**：保存正史、人物、大纲、章节、事件、线索和当前状态。
3. **确定性脚本**：处理格式、重复 ID、失效引用、因果、线索生命周期、上下文组装和章节提交。
4. **模型与作者**：模型负责创意、语义分析、写作和候选修订；作者保留价值判断、正史审批和最终定稿权。

当前完成的功能包括：

- 1 个总控 Skill 和 12 个专职 Skill；
- 故事圣经、人物、宏观大纲、章节卡、场景卡和状态库；
- 正史、时间线和线索机械校验；
- 按 POV 知识权限过滤秘密的上下文组装；
- 逐场景草稿工作流；
- 连续性审校和两阶段文笔编辑；
- 带人工批准门禁的唯一章节提交入口；
- 章节摘要、事件、人物、线索、正史和门禁回写；
- 6 份 JSON Schema；
- 5 个可选只读审校代理配置，默认关闭；
- 一套可运行的“雾港”最小示例和新项目模板；
- 自动化测试、严格类型检查和代码质量检查。

## 2. 核心设计原则

### 2.1 写作生成，状态确定

正文可以具有创造性，但 ID、状态、依赖、时间、人物知识和线索生命周期必须由结构化文件与脚本管理。

### 2.2 审校只读，修改串行

连续性、人物、时间线、线索和文笔可以从不同角度审查；但同一个章节只能由一个修改入口串行处理。正式定稿和状态回写只允许通过 `chapter-committer`。

### 2.3 正史必须显式批准

AI 可以提出设定，但不能自行把建议变成正史。状态含义如下：

| 状态 | 含义 |
|---|---|
| `CANON` | 正文或人工审批已经确认 |
| `PLANNED` | 计划采用，但尚未进入正文 |
| `RUMOR` | 世界内角色相信，不保证客观真实 |
| `SECRET` | 客观真实，但只有指定角色知道 |
| `RETIRED` | 已废弃，禁止继续使用 |
| `UNKNOWN` | 作者刻意留白 |

### 2.4 大方向稳定，局部滚动

- 全书保留核心戏剧问题、关键转折和结局逻辑；
- 当前卷保存较完整卷纲；
- 未来 10 至 20 章保存章节级规划；
- 未来 3 至 5 章保存较详细计划；
- 只锁定当前章的可执行章节卡和场景卡。

### 2.5 上下文有限且带负信息

写作时不把全书全部塞给模型。上下文包只读取当前场景所需资料，并明确：

- 当前 POV 不知道什么；
- 哪个真相不能提前揭示；
- 哪些设定已经退休；
- 哪些人物、物品不能在场；
- 哪些表达方式需要避免；
- 场景必须在何处停止。

## 3. 工作区结构

```text
bookMaker/
├── AGENTS.md                         # 项目级最高操作纪律
├── pyproject.toml                    # Python、测试、类型和格式配置
├── uv.lock                           # 可复现 Python 依赖锁
├── .codex/
│   ├── config.toml                   # Codex 项目配置，Subagents 默认关闭
│   └── agents/                       # 5 个可选只读审校代理
├── .agents/
│   └── skills/                       # 13 个仓库级小说 Skill
├── scripts/                          # 确定性校验、查询、组装和提交工具
├── novel/
│   ├── brief/                        # 创作简报、核心创意、Style Bible
│   ├── bible/                        # 正史、时间规则、地点和阵营
│   ├── characters/                   # 人物卡和有向关系
│   ├── outline/                      # 全书大纲、卷纲、章节矩阵、情节线
│   ├── chapters/                     # 每章卡片、草稿、定稿、审校、提交清单
│   ├── state/                        # 事件、摘要、人物、线索、物品和门禁
│   ├── reports/                      # 各类审校报告
│   └── schemas/                      # JSON Schema
├── tests/
│   ├── fixtures/minimal_project/     # 最小端到端测试项目
│   └── test_*.py                     # 行为与环境契约测试
└── docs/
    ├── AI写小说的主流工作流程与工程化实践_2026版_CodexSkills增补版.md
    └── Codex_AI小说工作流环境_完整使用手册.md
```

`.yaml` 文件采用 **JSON 兼容 YAML**：文件扩展名保留为 `.yaml`，内容使用 JSON 的大括号和数组语法。JSON 是 YAML 的有效子集，这样既保留 YAML 资产语义，又能在没有额外解析器的情况下进行确定性校验。

## 4. 首次使用

### 4.1 进入工作区

```powershell
Set-Location 'D:\codes\bookMaker'
```

### 4.2 检查工具

工作区已经把 `uv` 安装在 `.tools\uv\uv.exe`，不会污染全局 PATH：

```powershell
.tools\uv\uv.exe --version
.tools\uv\uv.exe run python --version
```

第一次执行可能建立 `.venv`，并按 `uv.lock` 准备依赖。

### 4.3 验证环境

```powershell
.tools\uv\uv.exe run scripts\validate_project.py --root .
.tools\uv\uv.exe run pytest
.tools\uv\uv.exe run ruff check .
.tools\uv\uv.exe run basedpyright
```

正确结果应包含：

```text
PROJECT_OK
```

以及全部测试通过。

### 4.4 让 Codex 识别 Skills

Codex 会从仓库的 `.agents/skills/` 自动发现 Skill。新开一个 Codex 任务后，可以：

- 在 CLI 或 IDE 中输入 `/skills` 查看；
- 输入 `$` 后选择 Skill；
- 直接写 `$novel-orchestrator` 显式调用；
- 用自然语言描述匹配任务，让 Codex按 Skill 的 `description` 自动选择。

若刚创建的 Skill 没有出现，重启 Codex 或重新打开任务。

## 5. 13 个 Skills 的能力、用法与原理

### 5.1 `novel-orchestrator`

**能力**：读取当前门禁，判断下一项唯一动作，调用专职 Skill，汇总阻塞项和审批项。

**用法**：

```text
$novel-orchestrator 检查当前项目状态，告诉我下一步只做什么。
```

**原理**：总控不保存领域细节，也不直接改正文。它通过 `workflow_status.yaml` 和校验结果做状态机路由，防止创作步骤乱序。

### 5.2 `novel-init`

**能力**：从内置模板创建新的 `novel/` 目录。

**用法**：

```powershell
.tools\uv\uv.exe run scripts\init_novel_project.py 'D:\codes\my-new-novel'
```

也可对 Codex 说：

```text
$novel-init 在 D:\codes\my-new-novel 初始化一个小说项目，不要覆盖已有文件。
```

**原理**：只复制 `.agents/skills/novel-init/assets/novel-template/`。若目标已有 `novel/`，脚本以退出码 2 拒绝，避免误覆盖。

### 5.3 `canon-manager`

**能力**：查询正史、分析新设定影响、检查章节冲突、形成变更提案。

**用法**：

```text
$canon-manager 查询“午夜封航”的状态、依赖、知情角色和正文证据。
$canon-manager 分析“雾铃可以修改名字”会影响哪些设定，不要提交。
$canon-manager 检查 CH001 是否违反正史。
```

**原理**：模型判断语义冲突，`validate_canon.py` 检查重复 ID、缺失依赖和无证据 `CANON`。正式变更只能进入章节提交清单。

### 5.4 `character-manager`

**能力**：维护人物目标、错误信念、语言指纹、有向关系、位置、伤势、物品和知识。

**用法**：

```text
$character-manager 检查许砚在 CH001 开始时知道什么，不能知道什么。
$character-manager 比较许砚在 CH001 前后的目标和情绪变化。
```

**原理**：长期人物设定放在 `characters/`，最近定稿后的可变状态放在 `state/`。这种分离避免人物卡被每章临时状态污染。

### 5.5 `timeline-manager`

**能力**：检查客观时间、叙述位置、认知时间、因果前置、移动和物品时机。

**用法**：

```powershell
.tools\uv\uv.exe run scripts\validate_timeline.py --root .
```

```text
$timeline-manager 审查 CH001 的事件顺序、移动和知识获得时机。
```

**原理**：事件记录原因 ID 和结果。脚本检查重复事件、失效原因引用及结果早于原因；模型再处理移动耗时、伤势恢复等语义问题。

### 5.6 `clue-manager`

**能力**：管理线索从计划、种植、推进到兑现或作废的生命周期。

**用法**：

```powershell
.tools\uv\uv.exe run scripts\validate_clues.py --root .
```

```text
$clue-manager 列出第一卷所有尚未推进或可能提前泄露的线索。
```

**原理**：`clues.yaml` 分别记录真相、角色认知、读者认知、种植、推进和兑现。脚本拒绝没有种植记录的已推进线索，以及没有兑现记录的 `PAID_OFF`。

### 5.7 `outline-planner`

**能力**：建立全书大纲、卷级闭环、情节线账本、章节矩阵和滚动计划。

**用法**：

```text
$outline-planner 根据简报和人物卡，为第一卷生成因果大纲；不要写正文。
$outline-planner 复盘最近五章是否重复同一种章节功能。
```

**原理**：每个节点必须写“人物选择造成的结果”，而不是事件清单；已经定稿的正文可以反作用于未来计划。

### 5.8 `chapter-planner`

**能力**：把大纲拆成章节卡、场景卡和章节前后状态。

**用法**：

```text
$chapter-planner 为 CH002 生成章节卡和 3 个场景卡，只做规划。
```

**原理**：章节不是“一些事情”，而是状态转换。若结尾与开头的目标、信息、关系、资源和风险完全相同，章节需要合并或重做。

### 5.9 `context-assembler`

**能力**：为指定章节生成有限上下文，并过滤当前 POV 不应知道的秘密。

**用法**：

```powershell
.tools\uv\uv.exe run scripts\assemble_context.py CH001 --root .
```

输出：

```text
novel/chapters/CH001/context.md
```

**原理**：章节卡通过 `canon_refs` 和 `clue_refs` 声明相关对象。`SECRET` 只有 POV 出现在 `known_by` 时才展示真相；`RETIRED` 只作为禁止信息出现。

### 5.10 `scene-writer`

**能力**：按场景卡逐场景写草稿。

**用法**：

```text
$scene-writer 读取 CH001 的上下文包，只写 CH001_S01；到 exit_result 停止。
```

**原理**：将大胆创作与严格审校分开。每次只生成一个场景，出现更好的局部结果时可以调整后续场景，而不用重写整章。

### 5.11 `continuity-reviewer`

**能力**：只读检查事实、时间、人物、物品、知识、规则和伏笔。

**用法**：

```text
$continuity-reviewer 审校 CH001，只输出问题、证据和最小修复方案，不要修改正文。
```

**原理**：硬一致性错误先于语言润色。每项问题必须引用草稿证据和权威数据证据，避免“感觉不对”式审校。

### 5.12 `prose-editor`

**能力**：先诊断文笔问题，再只修复作者批准的问题 ID。

**用法**：

```text
$prose-editor 诊断 CH001，不要改正文。
$prose-editor 只修复 STYLE_CH001_02，保护事实、POV、线索时机和人物决定。
```

**原理**：无目标反复润色会把文本改得安全、平均。两阶段流程要求每次修改有证据、有边界、有停止条件。

### 5.13 `chapter-committer`

**能力**：唯一入口提交定稿并回写全部状态。

**用法**：

```powershell
.tools\uv\uv.exe run scripts\commit_chapter.py CH001 --approved --root .
```

**原理**：必须同时满足命令行 `--approved` 与清单状态 `HUMAN_APPROVED`。提交前把所有输出装入内存，写临时文件后逐个原子替换，并在完成后重新校验正史、时间线和线索。

## 6. 9 个脚本

| 脚本 | 能力 | 成功标志 |
|---|---|---|
| `init_novel_project.py` | 复制新小说模板，拒绝覆盖 | `INIT_OK` |
| `validate_project.py` | 组合检查目录、正史、时间线、线索 | `PROJECT_OK` |
| `validate_canon.py` | 检查重复 ID、依赖、CANON 证据 | `CANON_OK` |
| `validate_timeline.py` | 检查事件 ID、原因引用、因果顺序 | `TIMELINE_OK` |
| `validate_clues.py` | 检查线索生命周期 | `CLUES_OK` |
| `query_story_state.py` | 跨 Markdown、YAML、JSONL、CSV 查询 | 返回文件和行号 |
| `assemble_context.py` | 生成章节上下文包并过滤秘密 | `CONTEXT_OK` |
| `commit_chapter.py` | 提交章节和状态，要求双重批准 | `COMMIT_OK` |
| `export_schemas.py` | 从 Pydantic 数据模型重建 Schema | `SCHEMA_OK` |

常见查询：

```powershell
.tools\uv\uv.exe run scripts\query_story_state.py CANON_PUBLIC --root .
.tools\uv\uv.exe run scripts\query_story_state.py 许砚 --root .
.tools\uv\uv.exe run scripts\query_story_state.py 雾铃 --root .
```

重建 Schema：

```powershell
.tools\uv\uv.exe run scripts\export_schemas.py --root .
```

## 7. 数据文件如何协作

### 7.1 创作简报

`novel/brief/` 是最高层约束：

- `project_brief.md`：题材、受众、规模、边界、成功标准；
- `premise.md`：一句话梗概、核心戏剧问题、主题和读者承诺；
- `style_bible.yaml`：POV、叙述距离、语调、句法和禁用模式。

### 7.2 故事圣经

`novel/bible/canon.yaml` 中每项设定有：

- 唯一 ID；
- 生命周期状态；
- 可执行陈述；
- 依赖；
- 知情角色；
- 正文或审批证据。

### 7.3 人物系统

- `characters.yaml`：长期稳定的人物卡和语言指纹；
- `relationships.yaml`：有方向的人物关系；
- `character_state.yaml`：最近定稿后的当前位置、情绪、目标、物品和知识；
- `knowledge_state.yaml`：秘密和认知边界；
- `items.yaml`：物品归属与位置。

### 7.4 大纲系统

- `master_outline.md`：全书宏观节点；
- `volume_01.md`：当前卷闭环；
- `chapter_matrix.csv`：章节功能和情节线覆盖；
- `thread_ledger.yaml`：长期主线、人物弧线、关系线和反派线。

### 7.5 章节目录

每章目录包含：

| 文件 | 作用 |
|---|---|
| `chapter_card.yaml` | 章节目标、状态变化、引用和禁区 |
| `scene_cards.yaml` | 场景目标、阻力和退出结果 |
| `context.md` | 自动生成的临时上下文包 |
| `draft.md` | 可修改草稿 |
| `review.md` | 连续性、剧情、人物和文笔审校结论 |
| `commit_manifest.yaml` | 作者批准后要回写的所有状态 |
| `final.md` | 已定稿正文，不得直接覆盖 |

### 7.6 状态库

- `events.jsonl`：客观事件和因果；
- `chapter_summaries.jsonl`：温记忆；
- `character_state.yaml`：人物当前状态；
- `world_state.yaml`：世界当前状态；
- `knowledge_state.yaml`：角色知识；
- `clues.yaml`：线索生命周期；
- `workflow_status.yaml`：质量门禁；
- `change_log.jsonl`：正式提交记录。

## 8. 章节质量门禁

```text
IDEA
  -> BIBLE_APPROVED
  -> OUTLINE_APPROVED
  -> CHAPTER_PLANNED
  -> DRAFTED
  -> CONTINUITY_PASSED
  -> STORY_PASSED
  -> STYLE_PASSED
  -> HUMAN_APPROVED
  -> CANON_COMMITTED
```

最重要的边界：

- `CHAPTER_PLANNED` 前不写正文；
- `DRAFTED` 后先修硬一致性，再修剧情和语言；
- `HUMAN_APPROVED` 只能由作者给出；
- `CANON_COMMITTED` 只能由 `chapter-committer` 产生。

## 9. 初学者逐步学习路径

不要第一天就尝试自动写完一章。按下面七级学习，每一级只增加一个新概念。

### 第 0 级：只读观察

目标：理解文件是记忆，Skill 是流程。

练习：

```powershell
.tools\uv\uv.exe run scripts\validate_project.py --root .
.tools\uv\uv.exe run scripts\query_story_state.py 雾铃 --root .
```

在 Codex 中：

```text
$novel-orchestrator 只读说明当前示例项目处于什么阶段，不修改文件。
```

通过标准：能解释 `brief`、`bible`、`outline`、`chapters` 和 `state` 的区别。

### 第 1 级：修改创作简报

目标：学会最高层约束。

练习：

1. 编辑 `project_brief.md` 中的类型、读者承诺和内容边界。
2. 编辑 `premise.md` 的一句话梗概。
3. 运行项目校验。

通过标准：能指出哪些决定属于作者，哪些允许 AI 提供候选。

### 第 2 级：建立一条设定和一个人物

目标：学会“计划不等于正史”。

练习：

1. 在 `canon.yaml` 新增一个 `PLANNED` 条目；
2. 给它唯一 ID、依赖、限制和知情角色；
3. 在 `characters.yaml` 新增一名人物；
4. 运行 `validate_canon.py`。

通过标准：不会给未进入正文的设定写 `CANON`，不会把秘密暴露给未知角色。

### 第 3 级：规划一章，不写正文

目标：理解章节是状态转换。

练习：

```text
$chapter-planner 为 CH002 生成章节卡和场景卡。只做规划，结尾至少改变目标、信息、关系或资源之一。
```

人工检查：

- 开场和结尾状态是否不同；
- 节拍是否因果相连；
- 是否引用已有正史和线索；
- 是否明确必须避免的剧透。

通过标准：删除正文语气后，章节卡仍足以指导写作。

### 第 4 级：组装上下文

目标：理解“相关信息”比“大上下文”更重要。

练习：

```powershell
.tools\uv\uv.exe run scripts\assemble_context.py CH001 --root .
```

打开 `context.md`，确认：

- 有简报、卷目标、章节卡和 POV；
- 有可见的 `CANON_PUBLIC`；
- 没有向许砚暴露 `CANON_SECRET` 的真相；
- 有“不得让主角提前知道守灯人的身份”。

通过标准：能解释为什么上下文包里需要负信息。

### 第 5 级：只写一个场景

目标：学会写作与审校分离。

练习：

```text
$scene-writer 只写 CH001_S01。严格服从 context.md 和 scene_cards.yaml，在 exit_result 处停止。
```

检查场景是否存在：

- 明确目标；
- 可观察阻力；
- 人物选择；
- 状态变化；
- 场景退出结果。

通过标准：不会让模型擅自续写下一场，也不会在草稿中提交新正史。

### 第 6 级：只读审校和最小修复

目标：先找硬错误，再处理行文。

依次使用：

```text
$continuity-reviewer 审校 CH001，不要修改。
$prose-editor 诊断 CH001，不要修改。
```

作者选择一个问题 ID 后：

```text
$prose-editor 只修复 STYLE_CH001_02，其他内容保持不变。
```

通过标准：每次修改都有问题 ID、证据、保护项和最小范围。

### 第 7 级：完成一次提交闭环

目标：理解人工批准和状态回写。

1. 人工定稿 `draft.md`；
2. 检查 `review.md`；
3. 填写 `commit_manifest.yaml`；
4. 把状态设为 `HUMAN_APPROVED`；
5. 运行：

```powershell
.tools\uv\uv.exe run scripts\commit_chapter.py CH001 --approved --root .
```

6. 检查：
   - `final.md`；
   - `chapter_summaries.jsonl`；
   - `events.jsonl`；
   - `character_state.yaml`；
   - `clues.yaml`；
   - `workflow_status.yaml`；
   - `change_log.jsonl`。

通过标准：能解释为什么“正文定稿”和“状态提交”必须是同一个闭环。

## 10. 一章的标准操作流程

```text
读取当前卷目标
  ↓
更新章节卡
  ↓
检查人物、正史、时间线和线索
  ↓
组装上下文包
  ↓
人工批准场景卡
  ↓
逐场景写 draft.md
  ↓
连续性检查
  ↓
剧情与人物检查
  ↓
文笔诊断
  ↓
只修复获批问题
  ↓
作者最终定稿
  ↓
填写 commit_manifest.yaml
  ↓
chapter-committer 回写状态
  ↓
更新未来 3 至 5 章计划
```

## 11. 可选只读审校代理

`.codex/agents/` 提供：

- `canon_reviewer`
- `timeline_reviewer`
- `clue_reviewer`
- `character_reviewer`
- `prose_reviewer`

它们全部配置为 `sandbox_mode = "read-only"`，但当前 `.codex/config.toml` 设置：

```toml
[agents]
enabled = false
```

因此不会自动或手动派发。本项目遵守“除非作者明确要求，否则不派发 Subagent”。当作者以后希望尝试并行只读审校时，可手动把 `enabled` 改为 `true`，新开 Codex 任务后生效。即使启用，也不得让多个代理修改同一正文。

## 12. 如何创建自己的小说项目

推荐保留本仓库作为“工具和模板仓库”，把新小说建立在独立目录：

```powershell
Set-Location 'D:\codes\bookMaker'
.tools\uv\uv.exe run scripts\init_novel_project.py 'D:\codes\my-novel'
```

然后把本仓库中的以下内容复制到新项目根目录：

- `AGENTS.md`
- `.agents/skills/`
- `.codex/`
- `scripts/`
- `pyproject.toml`
- `uv.lock`
- `.tools/uv/`，或在新项目中重新安装 `uv`

若只想在本仓库开始创作，可以直接替换 `novel/` 中的“雾港”示例。替换前建议先把示例复制到外部备份目录。

## 13. 常见问题

### 13.1 Skill 没有出现

确认路径为 `.agents/skills/<skill-name>/SKILL.md`，然后重启 Codex 或重新打开任务。运行：

```powershell
Get-ChildItem .agents\skills -Directory
```

### 13.2 中文乱码

- 用 UTF-8 打开和保存文件；
- PowerShell 读取时指定 `-Encoding utf8`；
- 不用旧版 ANSI 编辑器保存 YAML、JSONL 或 TOML。

### 13.3 `PROJECT_MISSING_PATH`

缺少必需文件。对照 `novel-init` 模板补齐，或重新初始化一个新目录。

### 13.4 `CANON_DUPLICATE_ID`

两个设定使用了同一 ID。保留一个权威条目，把另一项改为新 ID，并更新所有依赖引用。

### 13.5 `CANON_EVIDENCE_REQUIRED`

条目标记为 `CANON`，但没有正文或审批证据。若尚未定稿，降为 `PLANNED`；若正文已确认，补充证据位置。

### 13.6 `TIMELINE_MISSING_CAUSE`

事件的 `causes` 引用了不存在的事件 ID。补录前置事件或删除错误引用，不要只改提示文本。

### 13.7 `CLUE_PAYOFF_REQUIRED`

线索被标记为 `PAID_OFF`，但没有兑现章节和变化记录。补充 `payoff` 或把状态恢复到 `PROGRESSING`。

### 13.8 `APPROVAL_REQUIRED`

必须同时满足：

- 命令带 `--approved`；
- `commit_manifest.yaml` 的状态是 `HUMAN_APPROVED`；
- 章节 ID 与目录一致。

### 13.9 为什么不直接接数据库或 RAG

第一阶段的 Markdown、JSON 兼容 YAML、JSONL、CSV、Git 和脚本足以支持个人长篇。只有在以下情况再升级：

- 事件、人物状态和线索达到难以手工查询的规模；
- 普通文本查询明显变慢；
- 需要语义召回旧场景；
- 需要可视化事件图或时间线；
- 多个小说项目需要共享状态服务。

演进顺序建议：

```text
文件系统
  → SQLite
  → RAG / 知识图谱
  → MCP 服务与可视化界面
```

## 14. 当前系统边界

- 脚本能保证结构和部分因果正确，不能客观保证文学性。
- 多文件提交采用“全部预计算、临时文件、逐文件原子替换”，不等价于数据库的跨文件事务。
- 上下文组装目前使用显式 ID 和最近三章摘要，没有向量检索。
- 时间线脚本检查结构化因果；复杂移动、历法、时间回溯仍需要语义审校。
- 文笔编辑能执行 Style Bible，最终语言质量仍由作者判断。
- 当前示例很小，不能替代真实题材下的长篇压力测试。

## 15. 推荐的日常命令

开始工作：

```powershell
Set-Location 'D:\codes\bookMaker'
.tools\uv\uv.exe run scripts\validate_project.py --root .
```

查询：

```powershell
.tools\uv\uv.exe run scripts\query_story_state.py <关键词> --root .
```

写章前：

```powershell
.tools\uv\uv.exe run scripts\assemble_context.py <章节ID> --root .
```

提交前：

```powershell
.tools\uv\uv.exe run scripts\validate_project.py --root .
.tools\uv\uv.exe run pytest
```

作者批准后：

```powershell
.tools\uv\uv.exe run scripts\commit_chapter.py <章节ID> --approved --root .
```

## 16. 官方 Codex 机制参考

- 创建与使用 Codex Skills：<https://learn.chatgpt.com/docs/build-skills>
- `AGENTS.md`：<https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- Subagents：<https://learn.chatgpt.com/docs/agent-configuration/subagents>
- 配置参考：<https://learn.chatgpt.com/docs/config-file/config-reference>

本工作区的原则可概括为：

> **让 Skill 负责流程，让文件负责记忆，让脚本负责确定性，让模型负责创造与语义判断，让作者负责正史和最终作品。**
