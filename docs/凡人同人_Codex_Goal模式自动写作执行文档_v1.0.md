# 《凡人同人》Codex `/goal` 模式自动写作执行文档

> 文档版本：v1.3  
> 适用项目：`D:\codes\bookMaker\projects\凡人同人`  
> 工作区根目录：`D:\codes\bookMaker`  
> 当前项目阶段：`IDEA`  
> 执行方式：一个阶段对应一个 `/goal`；阶段内自动循环，阶段边界由作者验收  
> Subagents：节制启用；默认 0—1 个，同时活跃不得超过 3 个  

---

## 0. 如何使用本文档

本文档是 `/goal` 的长期执行合同，不是需要一次性粘贴进输入框的超长 Prompt。

Codex 官方说明中，`/goal` 的目标文本最多 4,000 字符；复杂要求应写进文件，再让目标指向该文件。因此实际运行时只需：

1. 在 `D:\codes\bookMaker` 打开 Codex。
2. 保持同一个任务，便于复用上下文和目标状态。
3. 找到本文档中当前阶段的“直接启动 Prompt”。
4. 将该 Prompt 原样输入 `/goal`。
5. 等 Codex生成阶段成果和验收包。
6. 作者只在阶段边界选择“批准、附条件批准或退回”。
7. 批准后使用下一阶段 Prompt，不允许 Codex自行跨越人工门禁。

查看或控制目标：

```text
/goal
/goal edit
/goal pause
/goal resume
/goal clear
```

首次启动前运行：

```powershell
cd D:\codes\bookMaker
.\.tools\uv\uv.exe run scripts\validate_project.py --root "D:\codes\bookMaker\projects\凡人同人"
```

预期结果：

```text
PROJECT_OK
```

---

## 1. 自动化模型

### 1.1 外层循环由作者控制

作者负责：

- 阅读独立决策研究报告后，决定主题、关键反转、生死、感情结论和最终语言；
- 批准立项正史、人物基线、大纲和当前章节卡；
- 批准文风问题 ID 的修复；
- 批准章节定稿和正史提交；
- 在验收包证据不足时退回阶段。

作者不需要：

- 逐条告诉 Codex下一步读哪个文件；
- 自行搜索互联网、整理项目证据或从零比较方案；
- 手工重复运行校验命令；
- 在阶段内部监督每次修改；
- 为机械错误逐次编写新 Prompt；
- 每写一个场景都单独确认。

### 1.2 内层循环由 Codex 自动执行

每个阶段内部固定采用：

```text
读取权威状态
  → 识别本阶段唯一目标
  → 扫描待决断问题
  → 若存在，则委派独立决策研究 Agent
  → 等待并固化独立研究报告
  → 选择匹配 Skill
  → 生成最小变更
  → 运行机械校验
  → 执行语义审查
  → 有证据的问题进入有限修复
  → 重新验证
  → 写入验收包
  → 停在作者门禁
```

这对应 Loop Engineering 的核心：设计可重复的调查、行动、验证、记录和停止循环，而不是依赖作者不断补 Prompt。

### 1.3 为什么不能一条 `/goal` 直接写完 430 章

现有 Skill 明确规定：

- 章节卡必须经过作者确认才能写正文；
- `prose-editor` 只能修复作者批准的问题 ID；
- `chapter-committer` 只能提交作者批准的章节；
- 新正史不能由模型自行批准；
- 审校默认只读；
- 正文写作必须逐场景，到场景退出结果立即停止。

因此，本系统实现的是“阶段内无人值守、阶段边界作者裁决”，而不是绕过作者权力的无限生成。

---

## 2. Loop Engineering 在本项目中的落地

| Loop Engineering 组成 | 本项目实现 |
|---|---|
| Goal | 当前阶段的 `/goal` 目标 |
| Harness | `AGENTS.md`、13 个小说 Skill、脚本、Schema、权限和文件结构 |
| Discovery | 读取 `workflow_status.yaml`、上游验收包、当前正文与状态 |
| Action | 由匹配 Skill 写入本阶段允许文件 |
| Verification | 项目脚本、专项校验、报告检查、章节审校 |
| State | `novel/state/`、章节目录、报告和变更日志 |
| Evidence | `novel/reports/goal/<阶段>-closeout.md` |
| Recovery | 最多三次且策略必须变化的有限重试 |
| Stop rule | 通过验收、遇到作者决策、重复失败或越界风险时停止 |
| Human gate | 作者在阶段边界批准、附条件批准或退回 |

### 2.1 自动循环的质量原则

1. 不能用“模型认为不错”代替证据。
2. 机械正确性由脚本和结构化文件证明。
3. 语义正确性由证据化审校报告和作者验收共同证明。
4. 每次重试必须说明新的失败假设和不同的修复方法。
5. 同一问题最多尝试三轮；第三轮仍失败则 `BLOCKED`。
6. 阶段没有完整验收包时，不得声称完成。
7. 不能通过删除规则、放宽约束或跳过审校获得绿色结果。
8. 用户验收之前，Codex只能给出 `READY_FOR_HUMAN_REVIEW`，不能自称 `APPROVED`。

### 2.2 Subagent 节制调度合同

本文件构成作者对有限 subagent 使用的明确授权，但不授权无限派发。主 Agent必须先判断委派收益是否高于上下文准备、等待、汇总和复核成本。

#### 并发硬上限

- 任意时刻同时处于运行状态的 subagent 不得超过 3 个；主 Agent不计入该数字。
- 启动新 subagent 前必须检查当前活跃数量；已有 3 个时只能等待、结束或复用现有 Agent。
- 默认使用 0—1 个；两项任务确实互不依赖时可使用 2 个；只有三个边界清晰且可并行的只读任务都能显著节省时间时才使用 3 个。
- 不得为了“占满额度”派发 Agent，也不得把一个小任务人为拆成多个 Agent。
- 所有 subagent 禁止继续派发下级 Agent。

#### 适合委派

| 类型 | 适用条件 | 典型输出 |
|---|---|---|
| 独立决策研究 DRA | 存在需要作者裁决的语义或创作问题 | 带项目与互联网证据的首选方案 |
| 广泛调研 | 需要跨多个项目文件或互联网来源建立证据全景 | 路径、来源、锚点、冲突和简短摘要 |
| 独立设计构思 | 复杂情节存在多条可行因果路线，需要避免主 Agent思路固化 | 相互独立的候选结构、收益、代价和失败模式 |
| 独立只读评审 | 候选产物复杂，主 Agent自审容易遗漏且没有写入需求 | 有证据的问题清单、反例和验收建议 |
| 伏笔／知识核验 | 线索跨章种植、推进、误导或兑现 | 线索生命周期、读者认知与角色认知冲突 |
| 时间线／因果核验 | 涉及移动、伤势、物品、知识获得、回忆或时间能力 | 事件顺序、因果前置和最小修复建议 |
| 批量只读整理 | 多个互不依赖的卷、人物或线索分区可以独立扫描 | 按固定 Schema 返回的分区结果 |

使用优先级固定为：

1. 独立评审；
2. 广泛调研；
3. 复杂设计的独立发散构思；
4. 大规模只读整理；
5. 普通任务不派发。

#### 不应委派

- 一次文件读取、一次搜索或主 Agent数分钟内即可完成的检查；
- 有严格前后依赖、必须连续推理的小任务；
- 正文起草、正文润色、章节提交、正史提交或正式状态更新；
- 多个 Agent 同时审查同一小段内容却没有不同职责；
- 为同一结论反复派发 Agent，直到得到想要的答案；
- 没有清晰输入、停止条件和输出格式的开放式“帮我看看”；
- 主 Agent无能力或无计划复核的工作。

#### 调度判定

派发前必须同时满足：

1. 任务边界可以用一段简短 Prompt 准确定义。
2. 子任务与其他进行中任务不存在写入冲突或结论依赖。
3. 预期节省的调查或核验时间明显高于协调成本。
4. 返回结果可以用路径、来源、问题 ID 或固定 Schema 验证。
5. 主 Agent知道收到结果后如何合并、采纳或拒绝。

任一条件不满足则由主 Agent直接完成。

#### 生命周期与写入纪律

1. 优先复用仍适合该职责的已有 Agent；需要真正独立判断时才启动新线程。
2. 主 Agent派发后继续做不依赖结果的只读工作，或等待关键结果；不得并行写入同一小说项目。
3. Subagent 默认只读，只通过返回消息交付结果；项目文件由主 Agent或对应写作 Skill 单入口修改。
4. 收到结果后先验证证据，再提炼进当前上下文，不把大段原始日志灌回主任务。
5. Agent完成后不再占用并发额度；需要追问时优先向原 Agent发送一次聚焦追问。
6. 同一子任务最多一次初始委派和一次追问；仍不清楚则主 Agent接管或标记阻塞。

#### 阶段建议配额

| 阶段情形 | 建议并发 |
|---|---:|
| 普通章节规划、简单修订 | 0—1 |
| 单个待决断问题或章节语义验收 | 1 个 DRA |
| 复杂情节、大纲或关键章节设计 | 2 个隔离构思 Agent；结束后再用 1 个新评审 Agent |
| 伏笔、知识与时间线联合审计 | 2 个不同视角的评审 Agent；必要时再串行使用 1 个综合评审/DRA |
| 大规模跨卷、跨人物或跨线索调研 | 2 个分区调查 Agent + 1 个独立评审 Agent |

“建议并发”不是最低数量。能够由一个 Agent 高质量完成时，不得为了并行而使用两个。

### 2.3 复杂设计的独立构思与评审闭环

Subagent 在复杂创作中的价值不是替主 Agent写成品，而是打破单一路径依赖，并从不同约束视角暴露问题。

#### 复杂设计触发条件

出现以下任一条件，必须启动本节闭环：一般使用 `1 个独立构思 Agent → 主 Agent综合 → 1 个新评审 Agent`；同时影响两条以上人物／情节线，或同时涉及伏笔与时间结构时，升级为 `2 个隔离构思 Agent → 主 Agent综合 → 1 个新评审 Agent`。

- 一个选择会影响未来 5 章以上、两个以上人物弧或两个以上情节线；
- 设计重大转折、身份揭示、牺牲、背叛、重逢、能力突破或卷级高潮；
- 同一戏剧目标存在至少两条都符合正史的因果路线；
- 新伏笔需要跨 10 章以上种植、推进和兑现；
- 一个反转同时依赖客观真相、角色认知和读者认知；
- 涉及回忆、时间跳跃、轮回能力、跨时代暗手或复杂事件先后；
- 方案改变已批准节点、关键人物选择或长期资源曲线；
- 主 Agent已经连续两轮只在同一思路上做局部变体。

普通过场、明确的承上启下章节或已有唯一执行路线时，不启动发散设计。

#### A. 广泛调研

复杂设计前如证据分散，可先使用 1—2 个只读 Agent：

- `Project Researcher`：跨 brief、bible、characters、outline、state 和已定稿正文定位项目证据；
- `External Researcher`：调查题材惯例、平台规则、历史文化或其他当前外部事实。

两个 Agent 必须分工不同，不得重复搜索相同材料。它们只返回事实与不确定性，不直接选择最终情节。
广泛调研 Agent 全部只读，不得写项目文件或继续派发下级 Agent。

#### B. 隔离式独立构思

最多同时启动 2 个构思 Agent。两者使用相同硬约束，但不得看到对方方案或主 Agent的偏好：

- `Causal Designer`：优先检查目标、选择、阻力、代价、状态变化和下一步压力；
- `Character & Reader Designer`：优先检查人物欲望、错误信念、情绪转折、信息差和读者预期；
- `Clue & Timeline Designer`：当伏笔或时间结构是核心时，替换上述一个角色，专注种植／兑现、公平证据、因果前置和知识边界。

每个构思 Agent 最多返回 2 个实质不同的方案。方案必须包含：

```markdown
- Premise:
- Causal chain:
- Character choice:
- Cost:
- Clue actions:
- Timeline dependencies:
- Reader knowledge change:
- End-state delta:
- Main risk:
- Reversibility:
```

禁止只改变场景装饰、角色名称或战斗形式却声称是不同方案。

构思 Agent 使用：

```text
你是独立情节构思 Agent，职责视角为 <Causal / Character & Reader / Clue & Timeline>。
项目根：D:\codes\bookMaker\projects\凡人同人
设计问题：<中性问题>
必须读取：<权威文件>
硬约束：<正史、人物、卷目标、线索和时间规则>

请独立提出最多 2 个因果骨架实质不同的方案。每个方案必须说明选择、阻力、代价、状态变化、伏笔动作、时间依赖、读者认知变化、风险和可逆性。不要猜测其他 Agent 的方案，不迎合主 Agent偏好，不写项目文件，不生成正文，不派发其他 Agent。
```

#### C. 主 Agent综合

所有构思 Agent结束后，由主 Agent独立完成：

1. 去重，不把相同因果骨架包装成多个方案。
2. 对照已批准正史、人物、线索、时间线和卷目标。
3. 保留最多 3 个真正不同的候选路线。
4. 选择或组合一个候选，说明采用与拒绝每项建议的理由。
5. 生成单一“综合候选”，但此时不写 `APPROVED` 或正式正史。

最终综合、创作责任和文件写入不得交给 subagent。

#### D. 新 Agent 独立评审

综合候选完成后，使用 1 个未参与构思的新 Agent 做只读评审。评审 Agent只读取综合候选、硬约束和权威文件，不读取主 Agent的选择理由或已拒绝方案，以减少确认偏误。

评审必须检查：

- 因果链是否存在跳步或靠巧合推进；
- 人物关键选择是否由其目标和压力产生；
- 代价是否真实改变后续状态；
- 伏笔是否有公平证据、生命周期和兑现范围；
- 客观真相、角色认知与读者认知是否混淆；
- 时间、移动、伤势、物品、知识和能力条件是否自洽；
- 反转是否依赖临时新增规则；
- 是否破坏已批准的大纲或正史。

评审只返回 `PASS / PASS_WITH_ISSUES / REJECT`、问题 ID、证据和最小建议，不改写候选。

新评审 Agent 使用：

```text
你是未参与本轮构思的独立评审 Agent。
项目根：D:\codes\bookMaker\projects\凡人同人
评审对象：<综合候选路径或内容>
必须读取：<正史、人物、线索、时间线、上游目标>

请只读检查因果、人物选择、真实代价、伏笔公平性、角色／读者认知、时间与移动、伤势／物品／知识获得、能力条件和既有合同。只返回 PASS / PASS_WITH_ISSUES / REJECT，以及带证据的问题 ID、严重程度和最小建议。不得重写候选，不读取已拒绝方案或主 Agent取舍理由，不写文件，不派发其他 Agent。
```

#### E. 伏笔与时间线双轨评审

对高风险章节、五章复盘或卷级收束，优先同时启动两个不同职责的只读 Agent：

1. `Clue & Knowledge Reviewer`：依据 `$clue-manager` 和知识状态，检查线索生命周期、提前泄露、读者公平性和角色知情边界。
2. `Timeline & Causality Reviewer`：依据 `$timeline-manager`，检查事件顺序、移动耗时、物品／伤势／知识获得时机和原因早于结果。

主 Agent再依据 `$continuity-reviewer` 汇总交叉问题。只有两个评审结论冲突或存在跨域致命问题时，才串行启动第 3 个新综合评审；若问题需要作者裁决，则不启动综合评审，改为串行启动一个新的 DRA。

双轨评审使用：

```text
你是独立只读 <Clue & Knowledge / Timeline & Causality> Reviewer。
项目根：D:\codes\bookMaker\projects\凡人同人
审查范围：<章节或章节区间>
必须读取：<对应状态、规则、正文和大纲>

仅按分配视角审查，不覆盖另一评审的职责。每项发现必须包含问题 ID、正文证据、冲突的权威证据、严重程度、最小修复建议和是否需要作者决策。没有证据时标记疑问，不改正文或状态，不派发其他 Agent。
```

#### 固定记录

由主 Agent将构思与评审结果提炼保存为：

```text
projects/凡人同人/novel/reports/design/<阶段ID>-ideation.md
projects/凡人同人/novel/reports/design/<阶段ID>-review.md
```

记录必须包含 Agent 任务引用、输入隔离方式、候选差异、主 Agent取舍、评审问题和最终处理。原始大段输出不直接复制进项目。

### 2.4 独立决策研究 Agent（DRA）

本项目把专门处理“待决断问题”的独立 subagent 称为 `Decision Research Agent`，简称 `DRA`。它不是写作 Skill，也不是第二个作者，而是作者作出阶段决策之前的独立调查与方案评估者。

#### 触发条件

出现以下任一情况，主 Agent 必须启动一个新的 DRA，不能直接把裸问题交给作者：

- 两个或多个方案都不违反硬规则，但会产生不同长期影响；
- 主题、结局、重大反转、生死、感情结论、POV、篇幅或发布策略需要选择；
- 项目文件彼此冲突，且无法按权威顺序机械消解；
- 新增、删除或改变原著硬锚点；
- 把 `PLANNED`、`UNKNOWN` 或 `RUMOR` 升级为正式 `CANON`；
- 调整已批准的大纲、角色关键选择、线索兑现方式或卷级目标；
- 第三轮自动修复仍失败，需要选择回退、降级或改道方案；
- 任何原本需要作者凭经验自行研究后才能回答的问题。
- 当前阶段验收暴露了两个以上都可成立的语义方案，需要作者在主题、情节、人物、文风或市场适配之间取舍。

以下不属于待决断问题，由主 Agent 在 allowlist 内直接处理：

- 格式、Schema、重复 ID、缺少引用和路径错误；
- 有唯一正确答案的校验失败；
- 不改变语义的排版和机械修复；
- 已有作者决定能够直接推出的执行细节；
- 可逆、低风险且不影响后续故事合同的局部实现选择。

#### 独立性要求

1. 每次研究使用新 Agent 线程；同一阶段紧密相关的问题可以形成一个决策包。
2. DRA 使用最小上下文启动，不继承主 Agent 的初步推荐、偏好性措辞或隐藏推理。
3. 主 Agent 只提供中性问题、候选选项、项目路径、硬约束和输出格式。
4. DRA 必须自行读取项目证据并独立搜索互联网，不能只复述主 Agent 的摘要。
5. DRA 对项目文件只读，不得编辑任何文件、推进状态、调用 `chapter-committer` 或再派发 subagent。
6. DRA 不得替作者批准方案；它必须选择一个推荐方案并标明置信度、风险与可逆性。
7. 主 Agent 不得改写 DRA 的推荐结论。若主 Agent发现证据错误，只能追加独立的“编排风险备注”，并把冲突一起交给作者。
8. 没有获得 DRA 最终结果之前，主 Agent不得跨越受该问题影响的工作。
9. DRA 只通过 Agent 返回消息交付结果；由主 Agent在完整性检查后保存报告。
10. DRA 运行期间主 Agent不得并行写入该小说项目，必须等待 DRA 返回后再继续。

技术限制：Codex subagent 会继承主任务的权限模式，因此这里的“只读”是强制工作流合同，不是独立沙箱。主 Agent必须在启动任意 subagent 前记录 `projects/凡人同人` 内全部文件的相对路径和 SHA-256，并在全部 subagent 返回、主 Agent恢复写入之前重新比对。若 subagent 产生任何文件变化，立即将阶段标记为 `BLOCKED`，列出变化并交给作者处理；对应 Agent 的结果不得作为有效证据。

#### 研究证据要求

- 至少引用一个项目内权威文件，并给出文件路径和具体章节或字段。
- 对可由外部资料验证的问题，至少使用两个相互独立的互联网来源。
- 事实性问题优先使用原始资料、官方文档、出版社或平台规则；搜索摘要和其他 AI 回答不能作为证据。
- 区分“项目事实、外部事实、推断、创作建议”，不得把推断写成原著事实。
- 每个互联网来源记录标题、URL、发布或更新时间、访问日期及其支持的具体主张。
- 只做必要摘要，不复制原著或其他受版权保护材料的长段文字。
- 如果无法访问互联网或关键来源不可核验，DRA 必须返回 `BLOCKED`，主 Agent不得伪造研究结论。
- 阶段门禁研究必须额外给出 `APPROVE`、`APPROVE_WITH_CONDITIONS` 或 `REJECT` 的独立验收建议。

#### 固定委派 Prompt

主 Agent启动 DRA 时使用以下合同，并替换占位符：

```text
你是本阶段唯一的独立决策研究 Agent（DRA）。任务是对 <DECISION_ID：中性问题> 进行独立调查、判断并给出一个首选方案。

项目根：D:\codes\bookMaker\projects\凡人同人
必须读取：<项目权威文件路径>
候选选项：<选项；若不完整，可补充>
硬约束：<正史、作者已批准决定、阶段边界>

必须独立完成：
1. 读取项目原始文件，不以主 Agent摘要代替证据；
2. 搜索互联网，事实性主张优先使用官方或原始来源，并交叉核验；
3. 区分项目事实、外部事实、推断和创作建议；
4. 比较各方案的正史一致性、叙事收益、长期成本、受众或平台适配、风险与可逆性；
5. 明确选择一个推荐方案，给出置信度和触发改判的条件；
6. 返回固定格式的 Markdown 报告。

边界：只读，不编辑项目文件，不推进工作流状态，不调用 chapter-committer，不派发其他 agent，不代表作者批准，不接受主 Agent预设结论。互联网不可用或关键证据不足时返回 BLOCKED。
```

#### 固定报告格式

研究结果由主 Agent原样保存到：

```text
projects/凡人同人/novel/reports/decisions/<DECISION_ID>-research.md
```

报告必须包含：

```markdown
# <DECISION_ID> Independent Decision Research

- Question:
- Agent thread / task:
- Research status: RESEARCHED / BLOCKED
- Confidence: HIGH / MEDIUM / LOW
- Gate recommendation: APPROVE / APPROVE_WITH_CONDITIONS / REJECT
- Access date:

## Neutral framing
## Project evidence
## Internet evidence
## Options considered
## Comparative assessment
## Independent recommendation
## Risks and reversibility
## Conditions that would change the recommendation
## Source list
```

#### 决策闭环

```text
主 Agent识别待决断问题
  → 冻结受影响的写入
  → 启动一个新的只读 DRA
  → 等待 DRA 最终报告
  → 主 Agent校验项目路径、URL 格式和必填证据完整性
  → 原样固化 DRA 推荐
  → 把报告纳入当前阶段 closeout
  → 作者在阶段边界批准、修改、延后或拒绝
  → 下一 Goal 记录 Author gate 后执行
```

例行阶段验收不自动等于“待决断问题”。如果验收项能够直接根据已批准合同和证据判定，本阶段可以不启动 DRA；只有出现本节触发条件时才强制使用 DRA。若本阶段此前已经为阻塞问题启动 DRA，可以让同一 DRA 一并给出阶段验收建议，避免重复派发。其他 subagent 仅按 2.2 节的收益判断、只读边界和并发上限使用。

---

## 3. 权威顺序

发生冲突时按以下顺序处理：

1. 作者在当前阶段给出的明确批准或否决；
2. `D:\codes\bookMaker\AGENTS.md`；
3. 本执行文档；
4. 对应工作区 Skill；
5. 已提交正文 `final.md` 及其事件、人物和线索状态；
6. 已批准的项目简报、正史、人物卡和大纲；
7. 源设定文档；
8. DRA 独立研究报告中的证据与推荐；
9. 尚未批准的计划、草稿和模型推断。

DRA 报告是“决策证据”，不是故事权威。它不能覆盖作者决定、原著硬锚点或已提交正文。

本项目的立项源文档：

```text
projects/凡人同人/source/凡人_轮回韩立同人设定集与长篇大纲_v1.1增补版.md
```

源文档中的等级解释：

- `A·原著明示`：不得改写结果，只能补过程；
- `B·强推定`：可调整细节，不得破坏稳定结论；
- `C·原著留白`：允许较大创作空间；
- `D·同人建议`：只是项目提案，必须经过作者批准。

---

## 4. 全局任务边界

### 4.1 所有阶段必须遵守

- 使用 UTF-8 读写中文文件。
- Windows 下使用 PowerShell 原生命令，不使用 `rg`。
- 可按 2.2 节节制派发 DRA、证据调查、互联网研究和独立核验 subagent；同时活跃数最多 3 个，全部不得修改项目文件或继续派发下级 Agent。
- 不修改源设定文档。
- 不修改根目录的 Skill、脚本、Schema 或工作流实现，除非作者另开修复任务。
- 不执行 Git commit、push、reset、checkout 或删除历史。
- DRA 和明确承担互联网资料研究的只读 subagent 可以访问互联网；网络资料只能作为研究或决策证据，不能直接写成原著事实或正式正史。
- 任一阶段触发 DRA 时，自动允许主 Agent写入 `novel/reports/decisions/<DECISION_ID>-research.md`；这不扩大该阶段的其他 allowlist。
- 任一阶段触发 2.3 节复杂设计闭环时，自动允许主 Agent写入 `novel/reports/design/<阶段ID>-ideation.md` 和 `<阶段ID>-review.md`；subagent 自身仍不得写文件。
- 不直接模仿在世作者的具体文风，只执行抽象 Style Bible。
- 不复制原著长段文字；专名和必要设定引用除外。
- 不把模型推断写成原著事实。
- 不把 `SECRET` 暴露给无权知晓的 POV。
- 不提前进入下一阶段。

### 4.2 状态与提交边界

- 初始提案使用 `PLANNED`、`UNKNOWN`、`RUMOR` 或 `SECRET`。
- 作者批准前不得产生正式 `CANON`。
- CH001 以后，正文产生的正式事实只能由 `$chapter-committer` 写入状态库。
- `draft.md` 是工作文本，`final.md` 只由 `$chapter-committer` 生成。
- `context.md` 是可再生上下文，不是权威数据。
- 审校报告只记录问题，不自动成为正史。
- Git 提交与小说“章节提交”是两件事；本文中的“提交章节”仅指 `$chapter-committer`。

### 4.3 阶段启动通用检查

每个 Goal 开始时必须：

1. 读取 `AGENTS.md`。
2. 读取本文档的全局合同和当前阶段。
3. 读取 `projects/凡人同人/novel/state/workflow_status.yaml`。
4. 读取上游阶段验收包。
5. 验证作者是否明确批准上游阶段。
6. 扫描是否存在未关闭的待决断问题；若存在，检查对应 DRA 报告及作者决定。
7. 扫描 2.3 节复杂设计触发条件，并写出本阶段 subagent 计划：是否委派、构思与评审角色、预期收益、输入隔离和最大并发；默认从 0 个开始。
8. 运行：

```powershell
.\.tools\uv\uv.exe run scripts\validate_project.py --root "D:\codes\bookMaker\projects\凡人同人"
```

9. 记录本阶段权威输入的 SHA-256。
10. 列出本阶段允许写入和禁止写入的文件。
11. 若上游未批准、输入 Hash 漂移、DRA 研究缺失或项目校验失败，停止创作并输出 `BLOCKED`。

---

## 5. 验收包规范

每个阶段必须生成：

```text
projects/凡人同人/novel/reports/goal/<阶段ID>-closeout.md
```

内容固定为：

```markdown
# <阶段ID> Closeout

- Stage:
- Goal:
- Started from:
- Input hashes:
- Skills used:
- Subagents used: <role -> purpose -> task/thread reference；未使用则写 NONE>
- Peak active subagents:
- Delegation benefit:
- Complex-design trigger:
- Independent ideation reports:
- Independent review report:
- Decision IDs:
- DRA task/thread references:
- Decision research reports:
- Subagent pre/post project hash comparison:
- Allowed writes:
- Actual writes:
- Forbidden areas checked:

## Acceptance results

| Check | Evidence | Verdict |
|---|---|---|

## Automatic loop history

| Round | Failure hypothesis | Action | New evidence |
|---|---|---|---|

## Unresolved decisions

## Risks and deviations

## Next-stage handoff

- Next stage:
- Required author decision:
- Files the next stage may trust:

## Verdict

READY_FOR_HUMAN_REVIEW 或 BLOCKED
```

禁止在作者批准前写 `APPROVED`、`OKAY` 或 `CANON_COMMITTED`。

若本阶段使用过任意 subagent，closeout 必须证明：

- 峰值同时活跃数不超过 3；
- 每个 Agent 都有独立、必要且互不冲突的职责；
- 所有 Agent 均只读且没有递归委派；
- 主 Agent对返回结果进行了证据复核；
- 省下的调查或核验成本足以覆盖协调成本；
- 前后文件 Hash 一致。未使用 subagent 时写明 `NONE`，不需要为了填满报告而补派 Agent。

若本阶段命中 2.3 节复杂设计触发条件，closeout 还必须证明：

- 使用了至少 1 个未参与主 Agent方案的独立构思 Agent；
- 高复杂度情形使用了 2 个彼此隔离、视角不同的构思 Agent；
- 主 Agent完成了去重、取舍和单一候选综合；
- 使用了 1 个未参与构思的新评审 Agent；
- 评审覆盖因果、人物、代价、伏笔、知识和时间线；
- 构思与评审记录已写入 `novel/reports/design/`；
- 未把 subagent 方案直接标记为 `APPROVED`、`CANON` 或正文。

若本阶段出现待决断问题，closeout 还必须证明：

- 每个问题都有唯一 `DECISION_ID`；
- 每个 ID 都有独立 DRA 报告；
- 报告包含项目证据、互联网证据和明确推荐；
- 全部 subagent 返回前后的项目文件 Hash 一致，证明没有 Agent 修改工作区；
- 主 Agent没有在报告完成前越过受影响边界；
- 作者能够在一个阶段验收消息中逐项接受、修改、延后或拒绝。

作者的批准应在下一阶段开始时追加到上游验收包：

```markdown
## Author gate

- Decision: APPROVED / APPROVED_WITH_CONDITIONS / REJECTED
- Decision resolutions: <DECISION_ID -> ACCEPT_RECOMMENDATION / OVERRIDE / DEFER / REJECT>
- Conditions:
- Recorded from: 当前用户消息
```

---

## 6. 阶段总览

| 阶段 | 目标 | 主要 Skill | 作者验收内容 |
|---|---|---|---|
| G00 | 冻结立项决策和执行基线 | `novel-orchestrator` + DRA | 八项立项决策 |
| G01 | 正史与时间线候选基线 | `canon-manager`、`timeline-manager` | 原著锚点和原创边界 |
| G02 | 人物、关系、知识和初始状态 | `character-manager` | 人物弧、关系和语言指纹 |
| G03 | 全书结构、情节线和伏笔账本 | `outline-planner`、`clue-manager` | 十卷结构与主要回收 |
| G04 | 当前卷和未来五章滚动窗口 | `outline-planner` | 第一卷执行方向 |
| Cnnn-P | 当前章节规划 | `chapter-planner` | 章节卡与场景卡 |
| Cnnn-W | 当前章节写作和审校 | `context-assembler`、`scene-writer`、审校 Skills | 正文候选和问题清单 |
| Cnnn-R | 可选的获批问题修复 | `prose-editor` | 修订后的最终候选 |
| Qnnn | 每五章周期复盘 | 管理与审校 Skills | 节奏、状态和滚动调整 |
| Vnn | 分卷收束 | `outline-planner`、管理 Skills | 卷目标完成度与下卷方向 |

### 6.1 十三个小说 Skill 的固定路由

`/goal` 不得因为 Skill 名称相近而自由替换职责。固定路由如下：

| Skill | 调用阶段 | 负责内容 | 不能做什么 |
|---|---|---|---|
| `novel-init` | 仅新项目或初始化修复任务 | 复制空白模板、建立目录和基础状态 | 本项目已经初始化，正常写作 Goal 不得重复运行 |
| `novel-orchestrator` | 每个阶段开始和结束 | 判断当前门禁、识别待决断问题、触发 DRA、选择后续 Skill、检查阶段是否可关闭 | 不写正文，不直接改正史、人物或线索 |
| `canon-manager` | G01、Cnnn-W、Qnnn、Vnn | 管理正史候选、依赖、冲突和变更提案 | 不自行批准新正史，不提交章节 |
| `character-manager` | G02、Cnnn-W、Qnnn、Vnn | 人物卡、关系、知识、位置、伤势、物品、目标和语言指纹 | 不替作者决定关键人物选择 |
| `timeline-manager` | G01、Cnnn-W、Qnnn、Vnn | 客观时间、叙述顺序、认知时间和因果前置 | 不用时间设定绕过正史限制 |
| `clue-manager` | G03、Cnnn-W、Qnnn、Vnn | 线索的种植、推进、误导、兑现和作废 | 不把计划中的线索写成已经发生 |
| `outline-planner` | G03、G04、Qnnn、Vnn | 全书结构、分卷闭环、情节线和滚动窗口 | 不直接生成正文或跳过章节卡 |
| `chapter-planner` | Cnnn-P | 章节卡、场景卡和可验证状态变化 | 不写 `draft.md`，不批准自己的计划 |
| `context-assembler` | Cnnn-W | 构造当前章有限、相关、分层的上下文包 | 不把 `context.md` 当成正史，不泄露 POV 无权知道的信息 |
| `scene-writer` | Cnnn-W | 按已批准场景卡逐场景写 `draft.md` | 不越过场景退出条件，不写 `final.md` |
| `continuity-reviewer` | Cnnn-W、Qnnn、Vnn | 只读检查连续性、知识边界、世界规则和伏笔时机 | 不修改草稿或正式状态 |
| `prose-editor` | Cnnn-W 诊断、Cnnn-R 修复 | 先生成问题 ID，再只修复作者批准的 ID | 不改变事实、顺序、POV、线索时机和人物决定 |
| `chapter-committer` | G02 提交 CH000；后续 Cnnn-P 提交上一章 | 唯一负责生成 `final.md` 并回写正式状态 | 没有 `HUMAN_APPROVED` 时不得运行 |

路由规则：

1. 每个 Goal 先由 `novel-orchestrator` 判断门禁并扫描待决断问题；有问题时先触发 DRA，再调用表中本阶段允许的 Skill。
2. 扫描 2.3 节复杂设计触发条件；命中时先完成独立构思、主 Agent综合和新 Agent评审，再由对应规划 Skill 形成正式候选。
3. “审校 Skill”默认只读；只有原写作 Skill 可在阶段预算内修复机械性问题。
4. `chapter-committer` 是正文与正式状态的唯一写入口，不得用通用文件编辑替代。
5. Skill 合同与本阶段 allowlist 同时生效；任一方禁止的写入都视为禁止。
6. 本项目已完成初始化，因此 `novel-init` 只作为结构完整性检查依据，不进入 G00 以后的正常写作链。

Subagent 不计入十三个小说 Skill。DRA 负责独立研究和推荐，其他 Agent 只承担明确的广泛调研、独立构思或只读评审；它们都不获得小说资产写权限。

各阶段的重点使用：

| 阶段 | Subagent 使用 |
|---|---|
| G00 | 1 个 DRA；必要时增加 1 个广泛调研 Agent |
| G01 | 1 个广泛调研 Agent，候选完成后 1 个新正史／时间线评审 Agent |
| G02 | 候选完成后 1 个人物／知识边界评审 Agent |
| G03 | 必须 2 个隔离构思 Agent，之后 1 个新评审 Agent |
| G04 | 命中复杂设计条件时 1—2 个构思 Agent，之后 1 个新评审 Agent |
| Cnnn-P | 普通章 0 个；关键转折、揭示、伏笔或时间结构章使用独立构思与评审闭环 |
| Cnnn-W | 高风险章并发 2 个评审 Agent：伏笔／知识、时间线／因果 |
| Qnnn | 固定并发 2 个不同视角的只读评审 Agent |
| Vnn | 固定并发 2 个卷级评审 Agent；新卷方向复杂时再串行执行构思与评审 |

### 6.2 执行顺序

执行顺序：

```text
G00
→ G01
→ G02
→ G03
→ G04
→ C001-P
→ C001-W
→ 作者批准 CH001
→ C002-P（先提交 CH001，再规划 CH002）
→ C002-W
→ …
→ Q005
→ …
→ V01
→ 下一卷
```

上述任一阶段出现待决断问题时，在阶段内部插入：

```text
识别 DECISION_ID
→ 独立 DRA 研究
→ 固化研究报告
→ 继续不受影响的工作
→ 在原阶段边界由作者裁决
```

---

## 7. G00：立项决策冻结

### 7.1 目标

把现有三个立项文件中的待定项、源文档内部矛盾和推荐默认值整理成一次作者决策包。此阶段只分析，不推进正史、人物、大纲或正文。

### 7.2 允许写入

```text
projects/凡人同人/novel/reports/goal/G00-closeout.md
projects/凡人同人/novel/reports/goal/G00-decision-packet.md
projects/凡人同人/novel/reports/decisions/DEC-G00-*-research.md
```

### 7.3 禁止写入

```text
projects/凡人同人/source/
projects/凡人同人/novel/brief/
projects/凡人同人/novel/bible/
projects/凡人同人/novel/characters/
projects/凡人同人/novel/outline/
projects/凡人同人/novel/chapters/
projects/凡人同人/novel/state/
```

### 7.4 阶段任务

1. 核对源文档和三个立项文件。
2. 至少处理以下决策：
   - 正式书名；
   - 420 章或 430 章；
   - 3—5 章序章或 8 章序卷；
   - POV；
   - 目标总字数与单章字数；
   - 发布平台和更新频率；
   - 牺牲式结局与开放尾声；
   - 原创角色、宗门和穿越落点是否沿用。
3. 为八项决策建立唯一 `DECISION_ID`，用中性措辞描述问题与候选项。
4. 启动一个全新的只读 DRA，让它独立读取项目文件、搜索互联网、比较八项决策并逐项选择一个推荐方案。
5. 主 Agent校验 DRA 报告的项目路径、来源 URL 格式和必填证据完整性，但不得改写推荐结论。
6. 为每项汇总：项目证据、互联网证据、选项、影响、DRA 推荐、置信度和不可逆程度。
7. 列出源文档中的 A/B/C/D 权威边界。
8. 不替作者作最终选择。

### 7.5 验收规范

- 八项决策均有明确选项。
- 八项决策均有 `DECISION_ID`、独立研究记录和明确的 DRA 推荐。
- DRA 至少读取项目权威文件，并为可外部验证的判断提供两个独立互联网来源。
- 420/430 与序章长度冲突被显式指出。
- 推荐值、项目事实、外部事实和推断分开。
- 没有修改任何项目权威文件。
- 验收包包含输入 Hash 和下一阶段边界。

### 7.6 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 G00“立项决策冻结”。项目根为 projects/凡人同人。必须为全部八项待决断问题启动一个新的只读 DRA，由其独立读取项目、搜索互联网并逐项给出推荐；仅在收益明确时再使用只读证据或核验 Agent，同时活跃 subagent 总数不得超过 3 个，禁止任何 subagent 写项目或继续委派。只允许生成 decision research、G00 决策包和 closeout，不修改 source、brief、bible、characters、outline、chapters、state，不进入 G01。完成验收后停在作者门禁。
```

---

## 8. G01：正史与时间线候选基线

### 8.1 启动前提

作者已经批准 G00，并在启动 Prompt 中给出八项决定。

### 8.2 目标

将源设定拆成原著硬锚点、强推定、留白和同人提案；形成可审查的正史候选、时间线规则和 CH000 立项基线提交候选。

CH000 是“项目基线记录”，不计入小说正文和章节编号。

### 8.3 允许写入

```text
projects/凡人同人/novel/brief/
projects/凡人同人/novel/bible/timeline_rules.yaml
projects/凡人同人/novel/chapters/CH000/
projects/凡人同人/novel/reports/canon/
projects/凡人同人/novel/reports/timeline/
projects/凡人同人/novel/reports/goal/G01-closeout.md
```

`novel/bible/canon.yaml` 在作者批准前保持现状；正式候选放入 CH000 的 `commit_manifest.yaml`。

### 8.4 阶段任务

1. 启动 1 个广泛调研 Agent，独立扫描源文档、三个立项文件和必要的互联网原始来源，整理原著锚点、冲突、证据位置与不确定性；不得直接决定正史。
2. 将 G00 作者决定回写三个立项文件。
3. 为源文档中的原著锚点建立稳定 ID。
4. 记录依赖、公开程度、角色认知和证据位置。
5. 原创方案默认保持 `PLANNED` 或 `UNKNOWN`。
6. 建立两条时间线、不可错位事件和时间能力边界。
7. 生成 CH000：
   - `draft.md`：项目基线摘要；
   - `commit_manifest.yaml`：待作者批准的正史变化；
   - 状态最高只能为 `STYLE_PASSED`。
8. 启动 1 个未参与调研整理的新评审 Agent，按正史等级、时间因果和知识边界审查 CH000 候选。
9. 运行正史、时间线和项目校验。

### 8.5 验收规范

- 每项原著锚点都能追溯到源文档章节。
- A/B/C/D 没有混写。
- 轮回韩立和现世韩立被定义为“一时二生”。
- 掌天瓶遗失、父女分离、甘如霜牺牲、终战成祖等硬边界未改变。
- 没有把同人建议提前写成正式 CANON。
- CH000 清单可解析且未标记 `HUMAN_APPROVED`。
- 广泛调研与独立评审由不同 Agent 完成，外部资料没有覆盖项目权威顺序。
- `validate_canon.py`、`validate_timeline.py` 和 `validate_project.py` 通过。

### 8.6 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 G01。先用 1 个只读广泛调研 Agent 扫描项目和必要互联网来源；主 Agent使用 $canon-manager、$timeline-manager 形成 CH000 候选后，再用 1 个未参与整理的新评审 Agent审查正史等级、时间因果和知识边界。出现待决断问题时使用 DRA。活跃 subagent≤3，全部不得写项目或继续委派。只写 G01 allowlist，不提交 CH000，不进入 G02，完成后停在作者门禁。
```

---

## 9. G02：人物、关系与初始状态

### 9.1 启动前提

作者明确批准 G01 的 CH000 正史候选。

### 9.2 目标

先通过唯一提交入口提交 CH000，再建立主要人物、关系、语言指纹、知识边界和开书初始状态。

### 9.3 允许写入

```text
projects/凡人同人/novel/chapters/CH000/
projects/凡人同人/novel/bible/canon.yaml
projects/凡人同人/novel/characters/
projects/凡人同人/novel/state/character_state.yaml
projects/凡人同人/novel/state/knowledge_state.yaml
projects/凡人同人/novel/state/items.yaml
projects/凡人同人/novel/state/workflow_status.yaml
projects/凡人同人/novel/state/chapter_summaries.jsonl
projects/凡人同人/novel/state/change_log.jsonl
projects/凡人同人/novel/reports/characters/
projects/凡人同人/novel/reports/goal/G02-closeout.md
```

### 9.4 阶段任务

1. 记录 G01 作者批准。
2. 将 CH000 清单改为 `HUMAN_APPROVED`。
3. 使用 `$chapter-committer` 提交 CH000。
4. 建立至少以下人物：
   - 轮回韩立；
   - 甘如霜；
   - 甘九真／蛟三；
   - 古或今；
   - 陈抟；
   - 弥罗仙尊；
   - 现世韩立；
   - 已获作者保留的主要原创人物。
5. 为每人记录目标、错误信念、压力策略、知识边界和语言指纹。
6. 关系必须使用有方向的边。
7. 初始状态只写开书时能够成立的内容。
8. 人物基线候选完成后，启动 1 个新的 `Character & Knowledge Reviewer`，独立检查人物动机、关系方向、知识边界、人格独立和未批准重大决定。

### 9.5 验收规范

- CH000 为 `CANON_COMMITTED`，且项目校验通过。
- 人物行动逻辑与源文档一致。
- 轮回韩立没有开局大罗战力或仙器库。
- 甘九真、南宫婉和现世韩立的人格独立被保护。
- 古或今和陈抟拥有独立目标与合理威胁机制。
- 感情主线只围绕甘如霜。
- 人物卡不偷偷决定尚未批准的背叛、生死或爱情。
- 人物与知识边界经过一个未参与写入的新 Agent独立评审。

### 9.6 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 G02。先用 $chapter-committer 提交获批 CH000，再用 $character-manager 完成人物基线；候选完成后启动 1 个新的只读 Character & Knowledge Reviewer 独立检查动机、关系、知识与人格边界。出现待决断问题时使用 DRA。活跃 subagent≤3，全部不得写项目或继续委派。只写 G02 allowlist，不进入 G03，完成后停在作者门禁。
```

---

## 10. G03：全书结构、情节线与伏笔账本

### 10.1 启动前提

作者批准 G02 人物基线。

### 10.2 目标

把源文档的十卷方案转为因果驱动、可滚动调整的项目大纲，同时建立情节线和伏笔生命周期。

### 10.3 允许写入

```text
projects/凡人同人/novel/outline/
projects/凡人同人/novel/state/clues.yaml
projects/凡人同人/novel/reports/clues/
projects/凡人同人/novel/reports/outline/
projects/凡人同人/novel/reports/goal/G03-closeout.md
```

### 10.4 阶段任务

1. 本阶段属于高复杂度设计，先同时启动 2 个隔离构思 Agent：
   - `Causal Designer`：设计十卷因果骨架、转折和代价；
   - `Clue & Timeline Designer`：设计伏笔生命周期、历史回声、跨时代暗手和时间依赖。
2. 主 Agent去重并综合为一个全书候选。
3. 再启动 1 个未参与构思的新评审 Agent，按因果、人物、伏笔、知识和时间线完整审查；若审查后仍需要作者选择，结束该评审线程，再串行启动一个新的 DRA。
4. 明确触发、中点、低谷、高潮和结局。
5. 将详细卷表统一到作者批准的总章数。
6. 为每卷写目标、选择、阻力、代价、状态变化和卷末压力。
7. 建立五条核心推进线：
   - 底蕴恢复；
   - 轮回大道；
   - 轮回盘锻造；
   - 历史回声；
   - 跨时代暗手。
8. 建立角色弧和反派独立行动线。
9. 建立承诺、推进和兑现表。
10. 建立线索生命周期，不提前写成已种植。
11. 所有大纲保持候选状态，作者批准前不得写 `APPROVED`。

### 10.5 验收规范

- 十卷结构覆盖完整结局。
- 后一个重要事件尽量由前一个选择造成。
- 每卷至少推进两条核心线。
- 古或今、陈抟和轮回殿内部威胁拥有独立行动。
- 轮回盘从前期雏形逐步成长。
- 历史回声不是“主角创造一切”。
- 线索均有计划种植、推进和兑现范围。
- 两个构思 Agent 的方案具有实质差异，主 Agent记录了取舍。
- 新评审 Agent 未参与构思，且评审覆盖因果、人物、伏笔、知识和时间线。
- `validate_clues.py` 与项目校验通过。

### 10.6 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 G03。先并发 2 个隔离构思 Agent：因果结构、伏笔与时间线；主 Agent综合后，再串行启动 1 个未参与构思的新评审 Agent。若仍需作者取舍，结束评审后再启动一个新的 DRA 检索项目与互联网。严格使用 $outline-planner、$clue-manager；同时活跃 subagent≤3，全部只读且不得继续委派。只写 G03 allowlist 和 design reports，不创建正文，不进入 G04，完成后停在作者门禁。
```

---

## 11. G04：当前卷与五章滚动窗口

### 11.1 启动前提

作者批准 G03 全书结构。

### 11.2 目标

将当前卷细化到可执行程度，并详细规划未来五章的功能窗口，但不生成正式章节卡或正文。

### 11.3 允许写入

```text
projects/凡人同人/novel/outline/master_outline.md
projects/凡人同人/novel/outline/volume_01.md
projects/凡人同人/novel/outline/chapter_matrix.csv
projects/凡人同人/novel/outline/thread_ledger.yaml
projects/凡人同人/novel/state/clues.yaml
projects/凡人同人/novel/reports/goal/G04-closeout.md
```

### 11.4 阶段任务

1. 记录 G03 作者批准，把获批大纲状态改为 `APPROVED`。
2. 细化第一卷的三幕、主要选择、代价和卷末状态。
3. 若五章窗口命中 2.3 节触发条件，先用 1 个独立构思 Agent 提供替代因果路线；同时涉及两条以上主线或伏笔与时间结构时，使用 2 个隔离构思 Agent。
4. 主 Agent综合窗口候选后，使用 1 个新评审 Agent检查章节功能重复、线索节奏、知识边界和时间依赖。
5. 规划 CH001—CH005：
   - 唯一章节功能；
   - 主情节变化；
   - 人物弧变化；
   - 线索动作；
   - 下一章压力。
6. 检查连续章节功能是否重复。
7. 只细化当前五章，未来章节保留宏观节点。

### 11.5 验收规范

- 第一卷目标可由章级变化逐步达成。
- CH001—CH005 没有重复同一种功能。
- 每章至少改变一种可记录状态。
- 开篇同时建立战力归零、资源落差和父女失散压力。
- 没有提前兑现后期轮回盘、轮回殿或终战能力。
- 当前窗口与全书大纲、人物和线索账本一致。
- 若命中复杂设计触发条件，存在独立构思、主 Agent取舍和新 Agent评审记录。

### 11.6 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 G04。使用 $outline-planner 细化第一卷和 CH001—CH005；若命中 2.3 节，使用 1—2 个隔离构思 Agent，主 Agent综合后再用 1 个新评审 Agent。若仍有待决断问题，结束评审后再启动新的 DRA 检索项目与互联网。活跃 subagent≤3，全部只读且不得继续委派。只写 G04 allowlist 和 design reports，不创建正文，不进入 C001-P，完成后停在作者门禁。
```

---

## 12. `Cnnn-P`：章节规划阶段

`nnn` 是三位数字章节号，例如 `C001-P`。

### 12.1 启动前提

- 当前滚动窗口已获作者批准。
- 若存在上一章，上一章正文候选已被作者明确批准提交。

### 12.2 自动处理上一章

从 CH002 开始，本阶段先处理上一章：

1. 记录作者对上一章的最终批准。
2. 把上一章 `commit_manifest.yaml` 改为 `HUMAN_APPROVED`。
3. 使用 `$chapter-committer` 提交上一章。
4. 运行项目、正史、时间线和线索校验。
5. 更新滚动大纲和最近摘要。
6. 提交失败则停止，不得规划当前章。

### 12.3 当前章任务

正式生成卡片前先扫描 2.3 节复杂设计触发条件：

- 普通功能章记录 `NOT_TRIGGERED`，不派发构思 Agent。
- 关键转折、重大揭示、伏笔兑现、时间能力、跨时代因果或多人物选择章，先使用 1 个独立构思 Agent；同时涉及两个以上高风险维度时使用 2 个隔离构思 Agent。
- 主 Agent综合后，使用 1 个未参与构思的新评审 Agent检查因果、人物、伏笔、知识和时间线，再生成正式卡片候选。

使用 `$chapter-planner` 生成：

- `chapter_card.yaml`；
- `scene_cards.yaml`；
- 章节引用的正史和线索 ID；
- 3—6 个因果节拍；
- 明确开场状态和结束状态；
- 每个场景的退出结果。

作者批准前，章节卡状态保持 `IDEA`。

### 12.4 允许写入

```text
上一章的提交相关文件（仅当作者已批准）
projects/凡人同人/novel/chapters/CHnnn/chapter_card.yaml
projects/凡人同人/novel/chapters/CHnnn/scene_cards.yaml
projects/凡人同人/novel/outline/
projects/凡人同人/novel/reports/goal/Cnnn-P-closeout.md
```

### 12.5 验收规范

- 上一章已成功 `CANON_COMMITTED`，或当前为 CH001。
- 当前章只有一个主要功能。
- POV、时间、地点和知识边界明确。
- 场景之间存在因果关系。
- 每个场景有可验证退出结果。
- 章节结束至少一种状态发生变化。
- 没有未定义正史或线索引用。
- 没有写 `draft.md` 或 `final.md`。
- 若命中复杂设计条件，独立构思、主 Agent取舍和新 Agent评审均有证据。

### 12.6 CH001 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 C001-P。先扫描 2.3 节；命中时使用 1—2 个隔离构思 Agent，主 Agent综合后再用 1 个新评审 Agent，然后由 $chapter-planner 生成卡片；未命中则直接规划。若仍需作者取舍，结束评审后再启动新的 DRA 检索项目与互联网。活跃 subagent≤3，全部只读且不得继续委派。章节状态保持 IDEA，不写正文，不进入 C001-W，完成后停在作者门禁。
```

### 12.7 后续章节直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 C<当前章>-P。先提交上一章，再扫描 2.3 节；关键转折、揭示、伏笔兑现或时间结构章使用 1—2 个隔离构思 Agent，主 Agent综合后再用 1 个新评审 Agent，最后由 $chapter-planner 生成卡片。若仍需作者取舍，结束评审后再启动新的 DRA 检索项目与互联网。活跃 subagent≤3，全部只读且不得继续委派。不写正文，不进入写作阶段，完成后停在作者门禁。
```

---

## 13. `Cnnn-W`：章节写作与审校阶段

### 13.1 启动前提

作者明确批准当前章节卡和场景卡。

### 13.2 阶段内自动循环

1. 记录章节规划的作者批准。
2. 把章节卡状态改为 `CHAPTER_PLANNED`。
3. 使用 `$context-assembler` 生成 `context.md`。
4. 验证上下文不包含 POV 无权知道的 `SECRET`。
5. 使用 `$scene-writer` 逐场景写入 `draft.md`。
6. 每个场景到达退出结果后停止该场景，再检查：
   - POV；
   - 知识边界；
   - 正史；
   - 资源与能力；
   - 场景状态变化；
   - Style Bible。
7. 全章完成后，将状态更新为 `DRAFTED`。
8. 若本章涉及伏笔种植／兑现、重大信息差、时间能力、跨地点移动、伤势恢复或跨时代因果，同时启动：
   - `Clue & Knowledge Reviewer`；
   - `Timeline & Causality Reviewer`。
9. 等两个 Agent 返回并通过前后 Hash 检查后，主 Agent依据 `$continuity-reviewer` 汇总交叉问题。
10. 串行执行：
   - `$continuity-reviewer`；
   - `$timeline-manager`；
   - `$canon-manager`；
   - `$character-manager`；
   - `$clue-manager`；
   - `$prose-editor` 诊断阶段。
11. 连续性机械问题可由原写作 Skill 在不改变人物选择、反转和正史的前提下最小修复。
12. 正式文风问题只报告 ID；closeout 前由 DRA 独立评估并推荐批准集合，不得绕过作者批准自动修复。

### 13.3 修复预算

- 连续性和结构修复最多两轮。
- 文风诊断最多两轮，但本阶段不执行正式文风修复。
- 每轮必须减少明确问题。
- 没有改善则保留上一版并停止。
- 致命问题、正史变更或关键选择问题先建立 `DECISION_ID`，由 DRA 独立研究，再随 closeout 交给作者。

### 13.4 允许写入

```text
projects/凡人同人/novel/chapters/CHnnn/chapter_card.yaml
projects/凡人同人/novel/chapters/CHnnn/context.md
projects/凡人同人/novel/chapters/CHnnn/draft.md
projects/凡人同人/novel/chapters/CHnnn/review.md
projects/凡人同人/novel/chapters/CHnnn/commit_manifest.yaml
projects/凡人同人/novel/reports/canon/
projects/凡人同人/novel/reports/timeline/
projects/凡人同人/novel/reports/continuity/
projects/凡人同人/novel/reports/style/
projects/凡人同人/novel/reports/goal/Cnnn-W-closeout.md
```

禁止写 `final.md` 和正式状态库。

### 13.5 可能的阶段结果

#### A. 无待修问题

- `commit_manifest.yaml` 状态为 `STYLE_PASSED`；
- 作者可以直接验收正文候选；
- 批准后由下一章规划 Goal 先提交本章。

#### B. 存在文风问题 ID

- 状态为 `NEEDS_STYLE_FIX_APPROVAL`，记录在验收包中；
- DRA 独立评估问题 ID，推荐批准集合、修复顺序和保护条件；
- 作者在阶段边界选择批准的问题 ID；
- 下一阶段运行 `Cnnn-R`；
- 未获批准的问题不得修改。

#### C. 存在正史或关键决策问题

- 输出 `BLOCKED`；
- 不生成可提交清单；
- 先由 DRA 独立研究并给出推荐，再等待作者选择。

### 13.6 验收规范

- 所有场景达到卡片退出结果。
- 章节开场和结尾状态可比较。
- 致命连续性问题为零。
- 时间、地点、物品、伤势和知识边界无明确冲突。
- 轮回法则能力有条件、效果和代价。
- 战斗遵循侦查、准备、试探、底牌、收益判断和战后盘点。
- 没有新增长段原著文字或直接模仿具体作者措辞。
- 没有写入 `final.md` 或正式状态库。
- 所有剩余问题有 ID、证据、严重程度和最小建议。
- 高风险章节的伏笔／知识与时间线／因果由两个不同 Agent 独立评审，没有用同一 Agent重复同一视角。

### 13.7 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 C<章节号>-W。按 $context-assembler → $scene-writer 写草稿。若涉及伏笔／信息差／时间能力／移动／伤势／跨时代因果，并发 2 个只读评审 Agent：伏笔与知识、时间线与因果；主 Agent再按 $continuity-reviewer 等 Skills 汇总。需作者取舍或选择文风 ID 时，串行使用 DRA。活跃 subagent≤3，全部只读且不得继续委派。不写 final.md，不提交正史，不进入下一章，完成后停在作者门禁。
```

---

## 14. `Cnnn-R`：获批问题修复阶段

仅在 `Cnnn-W` 存在需要作者批准的问题 ID 时执行。

### 14.1 目标

只修复作者明确批准的问题 ID，再次执行全章验证，形成最终正文候选。

### 14.2 任务边界

- 使用 `$prose-editor` 的第二阶段。
- 锁定事实、顺序、线索时机、人物决定、POV 和术语。
- 每个 ID 只修改最小范围。
- 不处理作者未批准的问题。
- 不写 `final.md`，不提交正史。
- 最多两轮语言修订。

### 14.3 验收规范

- 每个获批 ID 有修改前后证据。
- 未获批位置没有语义变化。
- 全部机械校验重新通过。
- 连续性没有因润色回归。
- `commit_manifest.yaml` 为 `STYLE_PASSED`，不能为 `HUMAN_APPROVED`。

### 14.4 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 C<章节号>-R。只修复作者批准的 <ID 列表与条件>，使用 $prose-editor 并重跑审校。若出现新的待决断问题，必须启动一个新的只读 DRA，独立读取项目、检索互联网并推荐；否则不强制派发。其他 subagent 按 2.2 节节制使用，同时活跃总数≤3，全部只读且不得继续委派。不写 final.md，不提交正史，完成后停在作者门禁。
```

---

## 15. `Qnnn`：每五章周期复盘

在 CH005、CH010、CH015 等章节完成并提交后执行。

### 15.1 目标

校验最近五章是否形成因果推进，修正未来五章滚动窗口，但不改已定稿正文。

### 15.2 检查内容

- 同时启动 `Clue & Knowledge Reviewer` 与 `Timeline & Causality Reviewer`，分别完成独立只读复盘；
- 主 Agent汇总两份报告；仅报告冲突时串行使用 1 个新综合评审，产生作者选择时改为启动一个新的 DRA；
- 五章功能是否重复；
- 承诺、推进和兑现是否失衡；
- 人物目标、关系、伤势、资源和知识变化；
- 时间和移动是否自洽；
- 轮回大道与轮回盘是否按节奏推进；
- 历史回声与暗手是否过密或失踪；
- 古或今、陈抟和配角是否有独立行动；
- 下一五章是否仍服务当前卷目标。

### 15.3 允许写入

```text
projects/凡人同人/novel/outline/
projects/凡人同人/novel/reports/
projects/凡人同人/novel/state/clues.yaml
```

不得修改任何 `final.md`。

### 15.4 验收规范

- 最近五章的所有定稿事实优先于旧大纲。
- 未来窗口变化不追溯篡改已提交事实。
- 所有未兑现线索有明确下一动作。
- 下一五章每章有不同主要功能。
- 输出继续、调整或暂停当前卷的建议。
- 两个评审 Agent职责不同，伏笔／知识与时间线／因果均有独立证据。

### 15.5 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 Q<最近章节号>。最近五章已提交；并发 2 个只读评审 Agent：伏笔与知识、时间线与因果，主 Agent用管理与审校 Skills 汇总。报告仅冲突时串行启动新综合评审；出现作者取舍时改为启动新的 DRA，并检索必要的项目与互联网证据。活跃 subagent≤3，全部不得写项目或继续委派。只更新未来大纲、线索计划和报告，不修改 final.md，完成后停在作者门禁。
```

---

## 16. `Vnn`：分卷收束

在一卷最后一章提交后执行。

### 16.1 目标

确认本卷目标、人物弧、资源变化和伏笔兑现，生成下一卷进入条件。

先并发执行：

1. `Clue & Knowledge Reviewer`：审查全卷承诺、种植、推进、兑现、作废以及角色／读者认知。
2. `Timeline & Causality Reviewer`：审查事件、移动、资源、伤势、知识获得和卷级因果链。

主 Agent综合后，若下一卷存在多条可行方向，按 2.3 节使用 1—2 个隔离构思 Agent，再由一个未参与构思的新评审 Agent审查；已有两个卷级评审足以支撑唯一方向时，不重复派发。

### 16.2 验收规范

- 卷目标有正文和状态证据。
- 本卷关键选择产生下一卷压力。
- 遗留线索均有继续、延后或作废决定。
- 主要人物弧有可观察变化。
- 资源、伤势、物品、组织和知识状态一致。
- 下一卷只细化宏观目标，不直接生成整卷正文。
- 伏笔／知识与时间线／因果均有独立评审证据。
- 若下一卷方向命中复杂设计条件，存在独立构思、主 Agent综合和新 Agent评审记录。

### 16.3 直接启动 Prompt

```text
/goal 严格依据 docs/凡人同人_Codex_Goal模式自动写作执行文档_v1.0.md 执行 V<卷号>。先并发 2 个只读评审 Agent：伏笔与知识、时间线与因果，主 Agent用卷级管理 Skills 汇总。若下一卷方向命中 2.3 节，再串行执行独立构思、主 Agent综合和新 Agent评审；仍需作者取舍时启动新的 DRA。活跃 subagent≤3，全部不得写项目或继续委派。不修改 final.md，不写下一卷正文，完成后停在作者门禁。
```

---

## 17. 作者验收回复模板

### 17.1 裁决待决断问题

```text
裁决 <阶段ID> 的待决断问题：

- <DECISION_ID-1>：ACCEPT_RECOMMENDATION
- <DECISION_ID-2>：OVERRIDE
  - 作者方案：…
  - 必须保护：…
- <DECISION_ID-3>：DEFER
  - 延后到：…

除上述明确裁决外，不得推定作者接受其他 DRA 推荐。
只有阻塞下一阶段的全部 DECISION_ID 均已 ACCEPT_RECOMMENDATION 或 OVERRIDE，才允许批准当前阶段。
```

### 17.2 批准普通阶段

```text
批准 <阶段ID>。

验收结论：APPROVED。
该阶段所有阻塞性 DECISION_ID 已逐项裁决。
允许下一阶段信任该阶段 closeout 中列出的产物。
不得扩大下一阶段边界。
```

### 17.3 附条件批准

```text
附条件批准 <阶段ID>。

必须先处理：
1. …
2. …

只允许修复上述问题。修复并重新生成 closeout 后再进入下一阶段。
```

### 17.4 退回

```text
退回 <阶段ID>。

问题：
1. …
2. …

不得进入下一阶段，不得修改阶段 allowlist 以外文件。
```

### 17.5 批准章节规划

```text
批准 CH<章节号> 的章节卡和场景卡。

允许进入 C<章节号>-W。
关键保护项：
1. …
2. …
```

### 17.6 批准文风问题

```text
批准 C<章节号>-W 中的以下问题 ID：

- STYLE-…
- STYLE-…

不批准：
- STYLE-…

只允许修复批准的 ID，然后重新执行章节审校。
```

### 17.7 批准章节定稿与提交

```text
批准 CH<章节号> 当前 draft.md 作为最终正文候选。

明确允许下一阶段将 commit_manifest.yaml 设为 HUMAN_APPROVED，
并使用 $chapter-committer 提交 CH<章节号>。

提交后才允许规划 CH<下一章节号>。
```

---

## 18. 失败、恢复与停止规则

### 18.1 自动修复

Codex可以自动处理：

- JSON 兼容 YAML 格式错误；
- 重复 ID；
- 缺少引用；
- 时间因果顺序错误；
- 当前章内明确的人物位置、物品、伤势或知识错误；
- 不改变语义的排版和文件格式问题。

### 18.2 必须先交给 DRA，再交给作者

- 两个来源都合理但互相冲突；
- 主题、结局、重大反转、生死或感情结论；
- 新增或废弃原著硬锚点；
- 改变人物关键选择；
- 把 PLANNED 升级为 CANON；
- 文风问题 ID 的正式修复；
- 章节最终批准；
- 任何超出阶段 allowlist 的变更。

处理顺序固定为：

```text
建立 DECISION_ID
→ DRA 独立研究并推荐
→ 主 Agent固化证据
→ 当前阶段 closeout
→ 作者在阶段边界裁决
```

章节最终批准仍只能由作者作出；DRA 可以审查风险并提出推荐，但不能代替作者授权 `HUMAN_APPROVED`。

### 18.3 有限重试

同一验收项最多三轮：

```text
第一轮：定位直接原因并最小修复
第二轮：更换失败假设或验证路径
第三轮：缩小问题、回退候选或形成阻塞证据
```

禁止三次重复同一种尝试。

第三轮仍失败时：

1. 停止编辑；
2. 保留最后一个可验证版本；
3. 在 closeout 中记录三轮证据；
4. Verdict 写 `BLOCKED`；
5. 为阻塞建立 `DECISION_ID`，先让新 DRA 独立研究，再把一个带推荐方案的明确问题交给作者。

### 18.4 防止伪进展

以下不算进展：

- 只增加字数；
- 重写但没有减少问题；
- 把问题从报告中删除而非修复；
- 放宽 Style Bible 或正史规则；
- 省略失败校验；
- 用新的未批准设定解释旧冲突；
- 声称“整体更流畅”但没有具体证据；
- 在没有作者批准时推进状态。
- 为简单任务派发多个 subagent；
- 同时运行超过 3 个 subagent；
- 用多个 Agent 重复验证同一结论，却没有不同职责或新增证据。

---

## 19. 每章作者验收清单

作者不必逐行检查全部工程文件，但至少确认：

### 章节规划阶段

- 本章是否有值得存在的唯一功能？
- 主角的目标和阻力是否清楚？
- 结尾状态是否与开场不同？
- 是否提前泄露或兑现了后期内容？
- 场景退出结果是否足够明确？

### 正文候选阶段

- 轮回韩立是否仍像谨慎、务实的韩立，而不是全知演说者？
- 资源、能力和胜利是否付出明确成本？
- 是否出现大段设定讲解或现代时间术语？
- 人物是否只知道自己应当知道的信息？
- 本章是否推动至少一条核心线？
- 结尾是否产生下一章压力？
- 是否接受 closeout 中列出的剩余风险？

### 提交授权

- 是否明确批准当前 `draft.md`？
- 是否明确允许设置 `HUMAN_APPROVED`？
- 是否明确允许 `$chapter-committer` 写入正式状态？

三项缺一，不得提交。

---

## 20. 推荐运行节奏

### 开书前

```text
G00 → 作者验收
G01 → 作者验收
G02 → 作者验收
G03 → 作者验收
G04 → 作者验收
```

### 每章

```text
Cnnn-P → 作者批准章节卡
Cnnn-W → 作者审阅正文候选
如有获批问题：Cnnn-R → 作者最终批准
下一章 C(n+1)-P 开始时提交上一章
```

### 每五章

```text
提交第 5 章
→ Q005
→ 作者批准未来窗口
→ C006-P
```

### 每卷

```text
提交卷末章
→ V01
→ 作者批准卷级结果和下一卷方向
→ 新卷五章窗口
```

---

## 21. 本文档采用的外部方法依据

Codex 官方文档说明：

- `/goal` 会把目标持续附着在当前任务中；
- 目标应写清 outcome、constraints 和 verification；
- 长指令应放入文件，再由不超过 4,000 字符的 `/goal` 指向；
- Goal mode 不会扩大原有权限，遇到需要决策的事项仍会暂停。
- Codex 可以按直接要求或项目指令启动 subagent，并把独立结果汇总回主任务。
- 适合优先委派读取、调查和总结类工作；并行写入同一项目会增加冲突，因此本项目的 subagent 全部严格只读。
- Subagent 继承主任务的权限模式，因此本项目用前后文件 Hash 证明所有 subagent 没有越过只读合同。
- Subagent 会增加模型与工具消耗，因此“默认 0—1、硬上限 3”是本项目为了控制协调成本制定的资源治理规则，不是 Codex 产品上限。

参考：

- [OpenAI：Long-running work](https://learn.chatgpt.com/docs/long-running-work)
- [OpenAI：Prompting 与 Goal mode](https://learn.chatgpt.com/docs/prompting#goal-mode)
- [OpenAI：Codex CLI slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- [OpenAI：Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI：Web search](https://learn.chatgpt.com/docs/web-search)

Loop Engineering 的应用依据：

- Addy Osmani 将可靠循环概括为调查、实施、验证和重复，并强调人类拥有外层裁决权。
- Loop Engineering 实践强调 discovery、verification、state、recovery、stop rules 和 human gates。
- 本项目优先把 subagent 用于广泛调研和独立评审；复杂设计采用隔离构思、主 Agent综合、新 Agent复审，伏笔与时间线采用不同视角的双轨核验。Subagent 不用于正文或状态写入；一个 Agent 足够时不扩编。

参考：

- [Addy Osmani：Loop Engineering](https://addyo.substack.com/p/loop-engineering)
- [Addy Osmani：Own the Outer Loop](https://addyo.substack.com/p/own-the-outer-loop)
- [Loop Engineering：A Practical Guide to Agent Loops](https://loopengineering.run/blog/what-is-loop-engineering)

---

## 22. 最终原则

这套流程追求的不是“让模型不停写”，而是：

```text
让 Codex 在明确边界内持续工作，
让机器证据关闭机械循环，
让审校证据暴露语义风险，
让作者只在真正需要判断的边界作决定。
```

任何阶段只要不能证明自己满足验收条件，就必须继续有限循环或安全停止，不能把“生成了很多内容”当作完成。
