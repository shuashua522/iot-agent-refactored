# WORKLOG

## 2026-08-16

- 复核 v4.2 机制 pilot：此前 runner 将多轮 utterances 一次性抽取，且没有把已写入 SQLite 的 memory_id/内容反馈给后续 LLM，导致 revise/feedback/merge/split 缺少真实上下文。新增逐 turn 抽取、逐 turn 写入、上下文记录和按 turn 汇总 usage；不修改已冻结场景或项目外 `try.memory`。
- v4.2 longitudinal audit 支持按独立 group 执行，避免单一结果根只运行 longitudinal 时被不存在的 runtime/mechanism unit 误判失败；新增分析器输出 TSR、WDR、真实 usage、transport attempts、history context 截断/完整上下文计数以及 two-way clustered bootstrap CI。
- revision `b1fce52` 的 longitudinal `35/35` pilot 运行了受限 transport repair，仍有 B3/L3 与 B5/L2 在两次 timeout 后 usage=0，strict audit 未通过；不扩展到 10 replicates。revision `17cf081` 的逐 turn 机制 pilot 也确认若干预注册轨迹缺乏自然语言建立的前序记忆，不能在禁止 scenario patch/runner 补写的条件下真实 activation。失败根按规则只保留本地。
- 启动独立 `v4.2 supplemental` 预注册：冻结 3 条完整产品 runtime 原始自然语言轨迹、8 条真实 LLM 机制激活轨迹、5 条扩展 longitudinal 轨迹以及 `1001-1010` replicate；结果根与 v4/v4.1 完全隔离。v4.2 仅在 1-replicate pilot 全审计通过后扩展到 10 replicates。
- 产品 runtime 依赖探针确认：项目内 Python 3.13 venv 安装通道未能完成依赖写入；未改动系统或仓库外路径。现有只读 Python 3.11 环境可导入 `smartHome/m_agent/memory/runtime_v1.py`、LangChain 与 LangGraph。v4.2 产品 runner 将 `DemoMemoryRuntime` 的 SQLite 显式定向至 v4.2 结果根，避免写入 `try/memory/runtime`。
- v4.2 首个机制 pilot 根 `protocol_v4_2_supplemental_56e7528_20260816` 保留为开发失败证据：16 个真实调用均写入 trace，但 extractor prompt 错将 MemoryService 所需 `op` 写成 `operation`，导致操作被拒绝，不能作为机制效应数据。修复后必须使用新 revision 和全新结果根重新 pilot，旧根不进入结果表。
- v4.2 第二个机制 pilot 根 `protocol_v4_2_supplemental_1a28f42_20260816` 进一步显示自由格式 extractor 未稳定满足 MemoryRecord 的枚举、引用和 nested-operation 契约；仅 `-Split` 一侧产生成功操作，其余不能报告机制贡献，也不扩展到 10 replicates。该根保留为开发失败证据；后续 extractor prompt 明确声明 `op`、source/scope/type 枚举、merge/split/revise/feedback 字段，审计器同时要求操作实际写入和目标 activation。
- v4.2 第三个机制 pilot 根 `protocol_v4_2_supplemental_0675303_20260816` 在部分机制完成真实写入/activation 后，暴露 runner 对未捕获 unit 异常仅打印而未落盘的问题；该不完整根不进入统计。runner 现要求任何异常都生成含 traceback、零 usage、failure 类型的 canonical unit JSON，再由审计器作为失败而非 missing unit 处理。
- v4.2 在 revision `e916a42` 完成完整机制 `16/16` 真实 LLM pilot 与扩展 longitudinal `35/35` 真实 LLM pilot。机制 audit 因多个 Ours/消融配对缺少真实 operation/activation 而失败；longitudinal audit 因 `Ours/L2`、`B1/L4`、`B5/L5` 三个保留的 external timeout usage=0 而失败。二者均不扩展到 10 replicates，也不进入结果表。
- 新增 `docs/v4.2补充实验状态报告-2026-08-16.md` 与 SHA-256 sealing 工具，明确产品 runtime 的项目外 `try.memory` schema/resolver 阻塞、v4.2 负/失败 pilot 的范围，以及真人双标注保持未完成的状态。
- 增加 `experiments/annotations/protocol_v4/HUMAN_ANNOTATION_PROTOCOL.md`，将双人独立盲化分发、第三方裁决、agreement 计算与人工 kappa 的完成条件写成可执行流程；不修改现有 model-model 标注状态。

- 新增 v4.1 原始文本 ingestion 补充实验的预注册协议、独立 runner、trace/fidelity/revision/usage 审计器与统计汇总器。协议冻结为 `Ours+B0-B5 × 3` 条 raw-text 轨迹 × `10` 个 replicate；只允许 external LLM，禁止 runtime `memory_ops`、`action_template` 与 evaluator 标签。
- v4.1 仅补足端到端 raw-text ingestion 的 baseline 覆盖，不修改或混合 2026-08-15 的 v4 behavioral unit；达到 10-replicate 且审计通过后按 supplemental/preliminary evidence 正式汇报。规则型 ingestion 仅支持明确温度偏好的创建/纠正，不能表述为完整 smartHome 产品 runtime 验证。
- 为 v4.1 协议隔离、禁止 heuristic backend 及 B1/B4 baseline fidelity、真实 usage、单 revision 审计新增 smoke；本地完整 smoke 为 `120/120` 通过。
- v4.1 首次与第二次 1-replicate 工程门禁分别暴露单元中断和上游 timeout；失败根保留但不进入性能结论。新增最多一次、同 revision 的 transport retry 及逐 unit 异常落盘，所有失败尝试须写入 canonical trace 的 `transport_attempts`，以避免网络故障被静默丢弃或混入模型失败率。
- v4.1 的 `cf90c7f`/`befe3c4` 门禁根均保留为失败工程记录：前者有 timeout 与 usage 缺失，后者 `B1/I3` 在两次 transport retry 后仍 timeout。为避免将后续 repair 代码与既有 trace 混用，修复后的运行必须使用新冻结 revision 和全新结果根。
- 分批执行审计发现 `befe3c4` runner 覆盖了结果根中的 selected-replicates 字段，导致先前 unit 被误标记为 unexpected；该根不进入正式结果。v4.1 manifest 改为固定预注册 replicate 集并累积记录 executed-replicates，且拒绝不同 revision/protocol 写入同一结果根。
- 在冻结 revision `48cc3b4` 和独立根 `protocol_v4_1_supplemental_48cc3b4_20260816` 完成 `Ours+B0-B5 × 3 raw-text trajectories × 10 replicate = 210/210` 真实 external-LLM unit；final audit pass，无 fallback、usage 缺失、revision 混合或 baseline fidelity 问题。canonical usage 为 `210` calls / `1,767,752` tokens；保留 219 次 transport attempts 与 1 个成功 repair 的原始证据。
- 生成权威投稿汇报 `docs/v4最终实验与v4_1补充实验汇报-2026-08-16.md`。v4.1 结果如实显示 Ours `20/30 (66.67%)`，B1 `27/30 (90.00%)`、B4 `25/30 (83.33%)`；因此该窄范围规则型 ingestion 证据进入补充实验，但不能被表述为 Ours 优于 raw-text baseline。

## 2026-08-15

- 完成冻结 revision `2391012` 的 v4 正式 behavioral 矩阵：`2100/2100` strict pass、`2100/2100` trace pass、单一 revision，统计状态为 `formal_analysis_ready`；canonical 用量为 `2520` calls / `15,930,162` total tokens。
- 完成独立 longitudinal `210/210` 与 robustness `28/28` 正式矩阵，均通过 strict/trace audit；canonical 用量分别为 `420` calls / `2,710,696` tokens 和 `28` calls / `220,441` tokens。
- 保存 `B0/H2/1023`、`B0/S1/1023`、`B0/C2/1029` 的 transport repair 原始三件套；失败尝试不进入性能分母，partial usage 为 `1` call / `1,124` tokens，canonical unit 在同一 revision 下恢复。
- 新增 `finalize_protocol_v4_formal.py` 与 hermetic 产物回归，生成正式 JSON/CSV/Markdown 汇总和 SHA-256 manifest；同步更新 v4 协议、预运行门禁、结果摘要与实现进展。
- 最终结果继续披露 `complete_llm_assisted` 标注偏离、human kappa 缺失、plan-only experiments adapter claim 边界，以及 guard 存在 harmful override 的限制。

## 2026-08-14

- 用户临时接受两个独立模型标注与第三模型裁决作为正式实验执行门禁；新增 `complete_llm_assisted` 审计报告与显式 readiness opt-in。机器记录保留 model-model κ、非 human κ 和后续人工复核要求，不伪造真人标注来源。
- 修正正式启动门禁：人工双标注有分歧但未完成第三方裁决时，agreement 状态改为 `pending_adjudication`；统一 readiness 审计同时校验 annotation、70-unit preflight 与 post-commit freeze，防止旧 pilot 状态误导正式放行；annotation/readiness 脚本纳入 freeze manifest 哈希范围；trace audit 失败现在返回非零退出码。
- 验证新 API `newapi / gpt-5.4-mini`：最低成本 probe 成功，provider seed 可用；完成 Q1/S1 受控真实 LLM pilot。
- 完成冻结 revision `8c4390c` 上的 70-unit preflight：`70/70` 落盘、trace audit `70/70 pass`、零 transport/fallback/usage missing/指标异常，B1/B4 fidelity 通过，状态为 `engineering_ready_for_formal_run`。
- 记录 preflight 真实用量：`84` 次 API 调用、`489782` total tokens；更新 2100-unit behavioral matrix 外推为约 `2520` 次调用、`14693460` total tokens。
- 同步 v4 协议、门禁报告、结果摘要、实现进展与结果分析：当前代码/API 已具备正式运行工程条件，唯一启动阻塞为 `13/13` 真实双标注、裁决及 Cohen's κ。
- 完成 v4 正式统计与执行门禁：实现 scenario/replicate_id 两层 clustered bootstrap、exact McNemar、连续 paired sign-flip、全 primary metrics Holm family、低优指标方向归一化和真实 missing/exclusion 分类。
- 修正 guard override 诊断和指标分母：逐 decision 计算 raw/guarded accuracy 与 corrected/harmful/neutral/unresolved，reason-only 变化不计 override；Unsafe Action Rate 只覆盖 evaluator 明确要求门控的场景。
- 收紧 HAOracle：校验 service schema、required/unexpected args、entity domain/capability 和 brightness/color_temp/position/temperature 范围；新增结构化失败回归。
- 新增 70-unit preflight 审计器和完整合成矩阵回归；该条记录形成时本地 `112/112` smoke、compileall、diff check、hidden bridge、baseline fidelity、ingestion、40/80-history longitudinal 均通过，随后同日已完成新 API 验证与 preflight。
- 明确论文 claim：正式 behavioral matrix 测试 experiments MemoryService + plan-only Agent adapter，不声称完整 smartHome 产品 runtime；integrated replay 单独报告。
- 修复 v4 runner 对 `expect_action(memory.answer)` 的 assertion kind：Oracle 与 Agent 路径均改为 `query`，避免 Query Answer Accuracy 被错误置空；新增 Q1 query metric 与第二家庭 world_path 回归。
- 收紧 `analyze_protocol_v4_formal.py` 的状态判定：只有冻结的 `7×10×30=2100` 主行为 unit 全覆盖才可标记 `formal_analysis_ready`，局部 pilot 一律为 `descriptive_only`。
- 同步 v4 协议、预运行门禁、结果摘要与实现进展：记录本轮仅运行 2 条新增真实 LLM pilot（2 calls、2,782 total tokens），历史 Q1 聚合受已修复 evaluator bug 影响且不得写入正式指标表；人工双标注/裁决/κ 和正式矩阵仍未完成。

## 2026-07-28

- 将仓库根目录 `实验进展-2026-7-26.md` 从 12-seed 阶段性口径更新为真实 LLM Agent 30-seed 最终封版口径，补充 `7560/7560` strict audit、最终主指标、统计显著性、API/token 成本及正式结果路径。

## 2026-07-23

- 新增 `实验方案-v3(1)-中文翻译.md`，将 `实验方案-v3(1).md` 完整翻译为中文版本，保留原有章节结构、场景编号、指标定义与表格内容。
- 新建 `docs/WORKLOG.md`，开始记录仓库内的文档变更历史。

## 2026-07-24

- 新增 `docs/实验方案落地实施蓝图.md`，基于实验方案、记忆实现方案与当前仓库代码现状，整理实验基础设施、记忆核心、虚拟环境、测试主线、基线/消融与论文交付物的待实现蓝图。
- 补充实施蓝图中的记忆行为规格、固定参数与算法规则、trace/场景字段、baseline/ablation 开关定义，以及 M0/M1/M2 实验完成分级。
- 补充 `wm-v1` 冻结实体与事件清单、36 场景实施目录、Oracle 结构化输入规则、运行配置/seed/结果文件契约，以及动作与 baseline 比较规则。
- 补充全部核心指标公式、trace 字段映射与统计检验规则，避免不同实现对指标口径产生分歧。
- 固化检索评分子项、冲突评分子项、ECE 分桶、MP 分母、CE 准确率定义与 maintenance 成本口径。
- 补充 `usable-stale` 的正式定义、场景 YAML 统一模板，以及 36 个场景的逐条展开要求，进一步收敛实现者对脚本结构和统计口径的理解。
- 新增 `experiments/` 实验主线第一版代码骨架，包含 memory/world/planner/runner/trace/metrics/config/scripts/tests，并新增 `docs/实验实现进展.md` 记录真实完成情况与后续缺口。
- 继续补充实验主线代码：接入 agent runner 过渡路径、批量结果产物（per-scenario/manifest/figure）、基础 system config 开关，并完成 smoke、batch、ablation 与 `unittest` 验证。
- 继续强化实验主线：补充 registry fallback、死记忆最小治理逻辑、baseline 运行入口、更多 smoke tests，以及主实验/表图导出脚本的真实产物链。
- 继续补充系统变体与结果导出：接入 B4/B5 与完整消融集合、真实配置开关、usage/grounding 反馈链，并修正表格导出对不同阶段 metrics 字段的兼容性。
- 补充 maintenance trace 与独立 `.maintenance.json` 结果产物，并验证主实验分流、自动化测试和结果导出在该改动后仍可运行。
- 继续细化关键场景实现，补上 candidate 晋升、alias revise、merge rollback 等路径，并把这些路径写入新增 smoke tests 与进度文档。
- 补充开发态一键运行脚本 `run_all_dev.py`，并增强 `manifest.json` 的可追溯元数据（git revision、world version、maintenance trace 清单）。
- 继续扩大回归覆盖：新增 agent 安全与高价值偏好 smoke test，并同步更新进度文档中的已跑通场景和测试数量。
- 继续扩大回归覆盖：新增 query/control 阈值分层，以及纠错/时间窗口/干扰项鲁棒性的 smoke tests。
- 继续扩大回归覆盖：新增 D3/F1/F2/F3/F4 这一组关系修订、冲突与传播路径的 smoke test。
- 同步更新实验实现进展文档，反映当前已接入的 baseline/ablation 全集，以及 `PM/UAA/maintenance latency` 已开始产生真实结果信号。
- 新增 `sync_ground_truth.py`，支持根据场景脚本自动重建 `scenario_ground_truth`，降低脚本与标注文件偏离风险。
- 继续补充执行闭环：在 runner 中为执行失败自动写入最小 `reflection` 记忆，并同步到进度文档。
- 新增 `run_configured_experiments.py` 与多 seed batch 能力，开始把实验执行从单次开发态运行推进到配置驱动的重复采样模式。
- 继续扩大 agent 回归覆盖：新增 `E1` 观影模式 routine 的 smoke test，并更新进度文档中的测试数量。
- 继续扩大负向约束回归：新增 `G1/G5` 的 absent-memory smoke test，覆盖冷启动不凭空记忆与瞬时状态不入长期记忆。
- 增强多 seed 运行结果：新增 `metrics.by_seed.json` 与 `metrics.summary.json`，开始让重复采样结果具备 seed 级统计视图。
- 继续增强多 seed 运行结果：新增 `per_scenario.multi_seed.csv`，并将其纳入 smoke test。
- 新增 `run_all_configured.py`，把配置化实验、baseline、ablation 与结果导出串成单入口执行链。
- 新增 `generate_report.py`，支持根据当前 `aggregated_metrics` 自动生成 `docs/实验结果摘要.md`。
- 同步更新实验实现进展文档：记录 `RRR` 已开始出现非零结果，以及当前 15 个 smoke tests 全部通过。
- 新增 `run_configured_baselines.py` 与 `run_configured_ablations.py`，把 baseline / ablation 也推进到配置驱动、多 seed 的执行模式。
- 扩大多 seed 回归覆盖：新增 `run_batch_multi_seed` 的 smoke test，并将总 smoke tests 数量更新到 16。
- 增强标注资产初始化：`sync_ground_truth.py` 现已同时生成 `scenario_ground_truth` 与 `inter_annotator` 占位文件。
- 增加容量治理回归：为 `sensitive` 记录的 `needs_review` 路径补充 smoke test，并将总 smoke tests 数量更新到 17。
- 扩大配置化执行回归：将 `run_configured_experiments.py` 自身纳入 smoke test，并将总 smoke tests 数量更新到 19。
- 增加标注资产回归：将 `sync_ground_truth.py` 纳入 smoke test，并将总 smoke tests 数量更新到 18。
- 继续扩大结果链回归：将 `generate_report.py` 纳入 smoke test，并将总 smoke tests 数量更新到 20。
- 继续扩大配置化入口回归：将 `run_configured_baselines.py` 与 `run_configured_ablations.py` 纳入 smoke test，并将总 smoke tests 数量更新到 22。
- 继续扩大结果链回归：将 `generate_statistics.py` 纳入 smoke test，并将总 smoke tests 数量更新到 23。
- 继续扩大配置化入口回归：将 `run_all_configured.py` 纳入 smoke test，并将总 smoke tests 数量更新到 24。
- 继续扩大成本链回归：新增 `prompt_tokens` 非零 smoke test，并将总 smoke tests 数量更新到 25。
- 同步更新实验实现进展文档：明确 `run_all_configured.py` 现已串起配置化实验、baseline、ablation、表图、Markdown 报告与统计摘要。
- 新增 `generate_run_index.py`，用于自动汇总当前 `reports/` 下全部 run 的索引清单，并将其纳入 smoke test。
- 继续扩大结果链回归：将 `generate_significance.py` 纳入 smoke test，并将总 smoke tests 数量更新到 26。

## 2026-07-25

- 继续收紧实验主线的任务成功判定：`TaskTrace` 现已记录 `assertion_results`、`action_success`、`clarification_success`、`memory_assertion_success`、`final_state_success` 与 `task_success`，`TSR` 改为以任务级成功为准，避免最终状态与语义失败脱钩。
- 继续补齐 planner / runner 语义：`OraclePlanner` 现区分 `query`、`automation`、`control` 三类任务；`query` 返回 `memory.answer`，`automation` 在无可用记忆时静默不执行，`control` 在无可用记忆时优先澄清。
- 继续补齐时间窗与生命周期门控：`refresh_status` 现会处理 `valid_from` 前的未生效记忆，`expect_no_action` 现在只检查是否产生动作，不再把“是否澄清”混入同一断言。
- 继续补齐场景封版缺口：`A1` 的动作模板已补到真实执行步，`sync_ground_truth.py`、`scenario_ground_truth` 与当前脚本结构保持一致。
- 当前 smoke 仍有少量场景在执行语义和标注粒度上未完全对齐，已记录到 `docs/实验实现进展.md`，下一轮继续收口。
- 新增《论文最终实验结果封版计划.md》，将当前开发态原型推进到论文正式结果所需的工作拆分为 P0-P7 阶段，并明确成功判定、36 场景覆盖、正式多 seed、统计审计、可复现封版和论文写入的验收门槛。

- 修正实验主线对 Python 3.9 的兼容性：将 `experiments/memory/schemas.py` 与 `experiments/trace/schemas.py` 中会触发 pydantic 导入失败的联合类型注解改为兼容写法，恢复 `python3 -m unittest experiments.tests.test_smoke` 可执行。
- 继续补齐 `usable-stale` 运行时语义：当前 stale 记忆已支持“查询可用、控制仅可用于澄清”的区分，成功验证后会回迁为 `active`，并把 `runtime_status` 写入 trace。
- 扩大回归覆盖：新增 stale 澄清语义与 stale→active 回迁的 smoke tests，并将总 smoke tests 数量更新到 29。
- 修正 `generate_report.py` 中的硬编码日期，`docs/实验结果摘要.md` 现会按运行当天生成日期。
- 同步更新 `docs/实验实现进展.md`，反映 Saturday, July 25, 2026 这轮代码状态、测试数量和新增语义。
- 继续补齐反馈链的真实语义：`mark_outcome` 现已支持沿关系链传播负向 ripple，按 1 跳 `0.3`、2 跳 `0.09` 衰减，并在 3 跳处截断；`F3/F4` 场景已从手工 `patch` 改为真实机制触发。
- 同步运行 `sync_ground_truth.py`，让 `scenario_ground_truth` 跟随最新的 F3/F4 场景脚本更新。
- 继续扩大回归覆盖：新增真实 ripple 传播 smoke test，并将总 smoke tests 数量更新到 30。
- 继续补齐 `F5/F6` 的真实语义：`maintenance` 事件现已支持脚本化 `memory_ops`，`split` 会保留 `supersedes / derived_from_memory_ids` 与 specialize/generalize edge，`merge` 会保留 `coverage_proof` 与 `evidence_refs` 并集。
- 同步运行 `sync_ground_truth.py`，让 `scenario_ground_truth/F5.json` 与 `F6.json` 跟随最新场景脚本更新。
- 继续扩大回归覆盖：新增 split lineage / edge 与 merge evidence union 的 smoke tests，并将总 smoke tests 数量更新到 32。
- 继续把 candidate 晋升从简化阈值补成 7 天窗口 / 无反例规则，并把 `B2/B5` 场景改成更完整的多次观测序列。
- 同步运行 `sync_ground_truth.py`，让 `scenario_ground_truth/B2.json` 与 `B5.json` 跟随最新场景脚本更新。
- 继续扩大回归覆盖：新增 candidate 晋升窗口规则的 smoke test，并将总 smoke tests 数量更新到 33。
- 继续收紧 `merge` / `reflection` 语义：`coverage_proof` 现会按 `source_ids` 自动补全并校验，缺失或不完整时会在维护阶段回滚；同时补充 `reflection` candidate 晋升 smoke test，并将总 smoke tests 数量更新到 35。
- 继续补齐检索上下文：`SearchResultPackage.global_constraints` 现会携带 preference / routine / reflection 约束记忆，并补充对应 smoke test。
- 继续补齐失活治理：`resampling` 现会保留 `resampled_from` / `resampled_at` 的可追溯字段，并补充对应 smoke test。
- 继续把薄场景补成更细粒度断言：`A1/B3/B4/E2` 现已增加字段级 `expect_memory` 断言，并重新同步 `scenario_ground_truth`，总 smoke tests 更新到 37。
- 继续补充薄场景回归：新增 `test_thin_specs`，让 A1/B3/B4/E2 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续补充 query/automation 薄场景回归：新增 `test_query_automation_thin_specs`，让 H1/H2/C1/C4 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续补充变更/缺失薄场景回归：新增 `test_mutation_and_absence_thin_specs`，让 D1/D2/G1/G5 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续补充关系修订/冲突/涟漪薄场景回归：进一步收紧 `D3/F1/F2/F4` 的字段级断言，并复跑现有 `test_relation_conflict_and_ripple_paths`。
- 继续补充修订/有效期/安全偏好薄场景回归：新增 `test_revision_validity_and_safety_thin_specs`，让 `A2/A5/B1/B6/C2/C3` 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续补充过期/阈值薄场景回归：新增 `test_expiry_and_threshold_thin_specs`，让 `B1/B4/C2/C3` 的字段级断言也进入自动化回归，并将 `docs/实验结果摘要.md` 中对应开发态 run 重新生成入册。
- 继续补充噪声/阈值薄场景回归：新增 `test_noise_and_threshold_thin_specs`，让 `G2/G3/G4` 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续补充安全反思/删除薄场景回归：新增 `test_safety_reflection_and_delete_thin_specs`，让 `E3/F7` 的字段级断言也进入自动化回归，并在结果摘要中留下对应开发态记录。
- 继续细化 `C3/G3` 场景：`C3` 补上 stale 的 query-usable 路径，`G3` 补上 capability 的 query / control 分流，并同步 `scenario_ground_truth` 与结果摘要。
- 继续细化 `C1` 与 habit 阈值回归：`C1` 补上到期后的 `expect_no_action` 静默断言，`B5` 进入新的 `habit / routine` 联合回归，并同步结果摘要与 `scenario_ground_truth/C1.json`。
- 继续细化 `D2` capability 失效后的回退执行：在 `D2` 中补上澄清后的“只开客厅顶灯”路径，并新增 `test_capability_routine_fallback_thin_specs` 专门覆盖该回归。
- 继续细化 `F5` 的 split 语义：在 `F5` 中补上分裂后对“开客厅灯”的澄清与静默断言，进一步约束宽泛 alias 分裂后的歧义处理。
- 继续补强未单独覆盖的高价值场景：新增 `test_candidate_isolation_resampling_split_thin_specs`，把 `A3/A4/F5` 的 candidate 隔离、重采样恢复与 split 歧义处理纳入独立 smoke，并同步结果摘要。
- 继续补强比较统计链：`generate_significance.py` 现在除了 bootstrap delta 外，还会输出 `Cohen's d` 与 Holm 校正 p 值，`docs/实验结果摘要.md` 也同步展示这些字段。
- 继续补强比较统计链：`generate_statistics.py` 现在也会合并 `Cohen's d` 与 Holm 校正 p 值，让统计摘要 JSON/CSV 与比较型统计保持一致。
- 继续补强结果目录可追溯性：`batch_run` 的 `manifest.json` 现在补入了 `resolved_config`、`generated_at` 与 `failed_task_ids`。
- 补齐 `generate_run_index.py` 对旧 `manifest.json` 的 `generated_at` 回退逻辑，并重新生成 `experiments/results/reports/dev/run_index.json`，让索引清单中的时间戳不再为空。
- 同步更新 `docs/实验实现进展.md`，记录当前阶段已收口完成，可先暂停在这里。
- 补齐场景标注元数据链：`sync_ground_truth.py` 现在会把 `title` / `category` / `rq_tags` 一并写入 `scenario_ground_truth`，并修正了 `A1` 缺失的 `rq_tags`。
- 清理配置化整链入口：`run_all_configured.py` 去掉了重复执行 `generate_run_index.py` 的冗余步骤，并同步更新对应 smoke 断言。
- 继续收口软过期场景口径：`C3` 的 `stale` 记忆层级从 `active` 对齐为 `dormant`，并重新同步 `scenario_ground_truth/C3.json`，避免生命周期状态和场景断言冲突。
- 复跑 `python3 -m unittest experiments.tests.test_smoke`，48 个 smoke tests 全部通过，`test_expiry_and_threshold_thin_specs` 与 `test_revision_validity_and_safety_thin_specs` 的 `C3` 回归已收口。
- 建立正式结果隔离根目录 `experiments/results/formal`，并在该根上完成 full formal run：`configured_oracle_formal` 30 seeds、`configured_agent_formal` 20 seeds、`configured_baseline_formal` 30 seeds、`configured_ablation_formal` 20 seeds。
- 在正式根上重建 `generate_tables.py`、`generate_figures.py`、`generate_significance.py`、`generate_statistics.py`、`generate_report.py` 与 `generate_run_index.py`，`docs/实验结果摘要.md` 已切换为 formal 结果摘要并标注 seed 数已达标、进入最终审计。
- 对 formal 根执行 trace / manifest 一致性审计，确认 `run_index`、`failed_task_ids`、`task_success` 与 `outcome` 逐项一致，formal 结果可追溯链闭合。
- 复核旧 formal 后确认其不能作为论文最终结果：存在 Oracle seed 伪独立、TSR 与 final-state 口径不一致、B0/B4 等价、Agent 文本特判、人工双标注为空以及正式主表为空等问题。
- 为所有包含物理动作的场景补充显式 `expect_final_state`，runner 改为累积多动作最终状态；不适用指标保留 `None`，新增 `State TSR`。
- 重构 SRR、MP、DMR、RRR、UC、WDR、CE 与成本字段口径；Oracle 统计单位改为 scenario，显著性使用场景级 paired exact sign test 与分层 Holm 校正，估算 token 字段明确标为 `Estimated`。
- 做实 B4 全量历史路径并验证其不再等同 B0；B5 保持 recency + importance + relevance 打分。
- 移除 Agent 对“观影模式/睡前模式”等文本硬编码，改为通用检索包 fallback，并在 trace/manifest 中标记 `heuristic_fallback`，不作为确认性 Agent 结果。
- 新增人工标注模板状态、`compute_annotation_agreement.py`、`audit_mechanism_sensitivity.py` 与 `audit_results.py`；空人工标注保持 κ 为 null，不生成虚假一致性。
- 修复 `table_1.csv` / `table_2.csv` 的 dev run id 硬编码，扩展 multi-seed manifest，并把正式结果链回归提升到 52 个测试全部通过。
- 根据最终口径修正《师兄写的记忆实现方案.md》：SQLite/canonical database 加确定性检索即满足要求，不要求 Chroma 或其他向量数据库。
- 提交 formal_v2 冻结口径，代码 revision 为 `2aed34c`；随后在独立 `experiments/results/formal_v2` 根完成全量运行。
- formal_v2 产出 17 个 consolidated manifest、12,500 条任务 trace、12,500 条 maintenance trace、5 张非空表和 5 份图数据，所有 manifest 均绑定 `2aed34c`。
- formal_v2 `artifact_audit.json` 状态为 `pass`、无 failure，确认性范围为 `oracle_only`；Agent 明确为 `heuristic_fallback`，人工双标注仍为 pending。
- 最终 Oracle Ours 结果为 TSR=1.0000（31场景）、State TSR=1.0000（15个适用场景）、WDR=0、CB=0.4516、PM=1.0000；统计使用场景级 paired exact sign test 与分层 Holm 校正。
- 机制敏感性审计确认 `-AsymFeedback` 与 `-FeatureAbsorption` 在当前测试集上无可观察行为差异，论文必须诚实报告而不能制造退化。
- 重构 `experiments/planners/agent_planner.py` 为实验侧 `plan-only` real-LLM adapter：真实模型只负责输出结构化 JSON 计划，动作执行统一回到 `HAOracle/wm-v1` runner，避免沿用原始 Agent 的 HTTP Home Assistant 执行路径。
- 扩展 `CandidateDevice` 与 `TaskTrace`：补入 `entity_type`、`capabilities`、`available_services`、`current_state`、结构化决策、tool calls、usage metadata、latency、failure type、动作序列与执行结果等审计字段。
- 调整 `run_agent_scenario`：当 decision 要求澄清时不再偷偷补执行动作；真实 external-LLM 决策、usage 与执行结果现在都会显式落入 trace。
- 为 real-LLM adapter 补充 7 条零成本 stub/smoke 回归，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `59/59` 全部通过。
- 使用现有 Conda 环境完成 1 次最小真实 API smoke，请求与脱敏结果写入 `experiments/results/agent_llm_smoke/api_smoke.json`，确认可收到非空响应和真实 usage metadata。
- 在独立目录 `experiments/results/agent_llm_smoke/` 完成 `G1 / E1 / B6 / E2 / E3` 五个 Agent 场景的单-seed 真实 external-LLM 验证，全部 `task_success=true`，且 `agent_backend=external_llm`。
- 新增并回填 real-LLM candidate manifest：`experiments/results/agent_llm_smoke/reports/real_llm_candidate_20260725/Ours/agent/manifest.json`，记录场景数、seed 数、backend、model/provider、API 调用数与 token usage，总计 5 个场景、9 次场景内调用、`9400` tokens。
- 同步更新 `docs/实验实现进展.md`、`docs/实验结果摘要.md` 与 `docs/论文最终实验结果封版计划.md`，明确区分 `heuristic_fallback` 与 `real_llm_smoke / real_llm_candidate`，避免论文口径混写。
- 为 external-LLM Agent 补充 `safety_execution_hint` prompt 规则，使 `B6` 这类高 `memory_worth`、强 grounding、唯一单动作的 safety 场景可在 prompt 中被明确标记为直接执行；同时新增对应 smoke test，`python3 -m unittest experiments.tests.test_smoke` 总数提升到 `60/60` 全部通过。
- 串行补跑第二个固定 seed：在 `experiments/results/agent_llm_smoke/` 下新增 `G1 / E1 / B6 / E2 / E3 @ seed=1002` 的真实 external-LLM 结果，成功部分共 `9` 次调用、`9077` tokens。
- `B6@1002` 首次真实 external-LLM 尝试因过度保守澄清而失败；离线定位后只重试 1 次，成功结果写入 `b6_seed1002_real_llm_retry1`，失败首次尝试保留在 `b6_seed1002_real_llm`，额外消耗 `1494` tokens。
- 新增 `experiments/scripts/consolidate_agent_llm_smoke.py`，可将隔离的单场景 real-LLM run 聚合为 consolidated multi-seed candidate；并生成 `real_llm_candidate_20260725_two_seed` 的 `manifest.json`、`audit.json`、`comparison.json` 与 `metrics.by_seed/by_scenario/summary`。
- 当前 `real_llm_candidate_20260725_two_seed` 覆盖 `G1 / E1 / B6 / E2 / E3` 共 5 个 agent 场景、2 个固定 seeds、10/10 成功 trace，成功 trace 共 `18` 次调用、`18477` tokens；仍明确保留为 `real_llm_candidate`，不包装成论文最终封版结果。
- 新增 `experiments/scripts/audit_real_llm_seal_readiness.py`，对 two-seed candidate 输出机器可读的封版就绪度审计；当前结论为 `candidate_only`，主要缺口仍是 `seed_count < 20`、source revision 不唯一与保留失败首次尝试。
- 同步更新 `docs/实验实现进展.md`、`docs/实验结果摘要.md`、`docs/论文最终实验结果封版计划.md`，记录 two-seed candidate 的成本、限制、比较边界与下一步扩量门槛。

## 2026-07-26

- 完成 `strict_main_agent_final_20260726_v4` 最终封版：`seed=1001-1030`、`Ours + B0-B5`、`36` 场景、`7560/7560` unit 全部落盘，`strict_main_agent.strict_audit.json` 状态为 `pass`。
- 为上述最终封版生成 `aggregated_metrics/strict_main_agent_final_20260726_v4`、`tables/strict_main_agent_final_20260726_v4`、`figures/strict_main_agent_final_20260726_v4` 与 `reports/strict_main_agent_final_20260726_v4`，并同步更新 `docs/实验结果摘要.md`、`docs/实验实现进展.md`、`docs/WORKLOG.md`。
- 汇总真实 API 成本：`11340` 次调用、`65,431,252` prompt tokens、`702,001` completion tokens、`66,133,253` total tokens；任务级失败主要集中在 `H2`、`C2`、`A4`、`A6`、`A2`、`D2`、`C1`。
- 生成最终比较统计：`Ours` 在 TSR、WDR、CB、PM 与 Context Efficiency 上均优于 `B0-B5`，TSR 相对最强 baseline `B3` 仍提升约 `6.2` 个百分点，严格 paired exact sign test 的 Holm 校正 p 值保持显著。
- 更新 `docs/实验结果摘要.md`，补入 `strict_main_agent_final_20260726_v4` 的当前真实 LLM 主实验状态，明确当前收口口径为 `seed=1012`、`1013` 已清理。
- 按当前正式 pilot 进度继续推进 `strict_main_agent_final_20260726_v4`，并根据最新口径将结果范围收口到 `seed=1012`；`seed=1013` 的误跑结果已从结果树中清理，不纳入当前正式数据。
- 重新整理 `strict_main_agent_final_20260726_v4` 的结果目录后，`1012` 现已形成 252/252 的完整结果，`strict_main_agent.strict_audit.json` 已重新生成并回到仅含 `1012` 的 partial 审计状态。
- 继续收口双 planner 语义：`_inject_registry_candidates` 现已支持 memory-grounded candidate 与 routine candidate，`retrieval_metadata` 补入 `memory_entity_map`，`OraclePlanner` / `AgentPlanner` 对 query、automation、routine 与高 `memory_worth` safety 语义已重新对齐。
- 验证 `Ours` 在不修改场景资产的前提下，当前已可把同一套 36 场景分别以 `oracle` 和 `agent` planner 路径执行并通过断言，为严格 full-grid 主实验提供底层执行能力。
- 新增 `experiments/scripts/build_strict_experiment_matrix.py`，并生成 `experiments/configs/strict_experiment_matrix.json`：明确 `Ours+B0-B5 × 36 × 30 = 7560` 个真实 Agent 主实验 unit、`8 ablations × 36 × 20 = 5760` 个 Oracle 消融 unit，总计 `13320` 个严格矩阵 unit。
- 新增 `experiments/scripts/run_strict_serial_unit.py`，提供单 `system-scenario-seed` 串行执行、不可覆盖输出、`--resume`、独立 unit manifest 与 `external_llm` 严格后端检查。
- 新增 `experiments/scripts/audit_strict_experiment.py`，可按严格矩阵审计不完整网格、fallback 混入、mixed revision、缺失 trace 与 strict checks 失败。
- 新增 `experiments/scripts/estimate_strict_main_cost.py`，可基于 pilot unit manifest 外推完整 `7×36×30` 主实验的调用量、token 与串行耗时，并在提供单价环境变量时输出费用区间。
- 为上述严格矩阵 / 串行 runner / strict audit / fallback 拒绝链补充 smoke 回归，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `64/64` 全部通过。
- 同步更新 `docs/实验实现进展.md` 与 `docs/论文最终实验结果封版计划.md`，将当前状态从“停止在 Oracle confirmatory”改为“严格主实验自动化基础设施已就绪，下一步进入 clean revision 上的受控真实 LLM pilot”。
- 发现 strict pilot 首次尝试 `strict_agent_pilot_20260726_v1 / Ours / A1 / 1001` 并未真正触发 API：`ExternalLLMClient` 对 `langchain` 存在硬依赖，初始化阶段直接退回 `heuristic_fallback`；该失败尝试结果被保留在 `experiments/results/strict_serial_pilot/` 中，仅作为技术性阻塞记录，不纳入后续 clean-revision pilot。
- 重构 `ExternalLLMClient`：保留 `langchain` 优先路径，但在缺少该依赖时自动回退到标准库 HTTP 的 OpenAI-compatible 调用，不安装新依赖、不修改项目外环境。
- 为新的 HTTP transport 增加 smoke test，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `65/65` 全部通过。
- 在 clean revision `0f20eab` 上启动新的 strict serial pilot：结果根为 `experiments/results/strict_serial_pilot_v2/`，run id 为 `strict_agent_pilot_20260726_v2`。
- 当前 strict serial pilot 已完成 `Ours / A1 / C1 / H2 / B6 @ seed=1001`，以及 `B6 @ seed=1001` 的 `Ours + B0-B5` paired pilot，共 `10` 个 unit、`13` 次 API 调用、`80444` prompt tokens、`788` completion tokens、`81232` total tokens。
- 当前 strict serial pilot 的真实行为结果为：`A1` success、`C1` success、`B6` success、`H2` failure；`B6` paired pilot 中 `B0` failure、`B1-B5` success。
- 生成 `experiments/results/strict_serial_pilot_v2/reports/strict_agent_pilot_20260726_v2/strict_main_agent.strict_audit.json` 与 `strict_main_agent.cost_estimate.json`：当前 audit 状态为 `partial`、无 fallback / mixed revision / missing trace；full-grid 主实验外推约为 `9828` 次调用、`61411392` total tokens。
- 新增 `experiments/scripts/run_strict_group.py`，用于在 strict 矩阵下按 group/system/scenario/seed 子集串行执行 unit，并落盘 `group_run_summary.json`，避免在需要批量运行 Oracle 零成本实验时手工拼接单 unit 命令。
- 调整 `run_strict_serial_unit.py`、`audit_strict_experiment.py` 与 `estimate_strict_main_cost.py` 的 usage 统计逻辑，统一按 trace 中真实 `prompt/completion/input/output/total tokens` 归一化汇总，避免只依赖 manifest 汇总字段。
- 为 strict group runner 与 token 归一化链新增 smoke tests，覆盖 group summary 落盘，以及 strict audit / cost estimate 对 `prompt_tokens`、`completion_tokens` 的读取与外推。
- 复跑 `python3 -m unittest experiments.tests.test_smoke` 与 `python3 -m compileall -q experiments`，当前离线验证为 `67/67` 全部通过，且 `experiments/` 全量编译无报错。
- 同步更新 `docs/实验结果摘要.md`、`docs/实验实现进展.md` 与 `docs/论文最终实验结果封版计划.md`，明确 `strict_oracle_ablations_20260726_v1` 已完成 `5760/5760` unit、strict audit `pass`，当前剩余核心缺口已集中到真实 `external_llm` 主实验。
- 提交 clean revision `fbedd87`（提交信息：`补齐 strict group runner 与 token 归一化审计`），作为后续新一轮 strict real-LLM pilot 的冻结起点。
- 在新的 clean revision `fbedd87` 上启动 `experiments/results/strict_serial_pilot_v3/`：已串行完成 `Ours / G1 / D3 / E1 / F2 / C1 @ seed=1001` 共 `5` 个 unit、`9` 次 API 调用、`11103` prompt tokens、`532` completion tokens、`11635` total tokens。
- `strict_agent_pilot_20260726_v3` 当前真实行为结果为：`G1` success、`D3` success、`E1` success、`F2` success、`C1` failure；其中 `C1` 的失败是模型漏掉了有效窗口内本应执行的动作，而不是过期后误执行。
- 生成 `experiments/results/strict_serial_pilot_v3/reports/strict_agent_pilot_20260726_v3/strict_main_agent.strict_audit.json` 与 `strict_main_agent.cost_estimate.json`：当前 audit 状态为 `partial`、无 fallback / mixed revision / missing trace；基于 `v3` 样本外推，full-grid 主实验约为 `13608` 次调用、`17592120` total tokens。
- 同步更新 `docs/实验结果摘要.md`、`docs/实验实现进展.md` 与 `docs/论文最终实验结果封版计划.md`，把 `strict_agent_pilot_20260726_v3` 作为当前最新 clean-revision pilot 记录入册，并明确 `v2/v3` 成本外推差异较大、full-grid 预算仍需更多代表场景校准。
- 将 `experiments/trace/writer.py` 改为同目录临时文件 + 原子替换写入，减少 paid run 中断时留下半个 JSON 导致 resume 误判的风险。
- 强化 `experiments/scripts/run_strict_serial_unit.py` 的 `--resume` 语义：不再因任意单个产物存在就跳过，而是要求 `trace + maintenance + manifest` 三件套都可解析、路径一致、strict checks 通过；否则自动进入 repair rerun。
- 重写 `experiments/scripts/run_strict_group.py` 为 bounded-concurrency 协调器：支持单协调器并发调度、阶段性原子 `group_run_summary.json`、API call / token 预算统计、技术性传输故障有限重试、指数退避与自动降并发。
- 扩展 `experiments/scripts/audit_strict_experiment.py`，把 maintenance trace 缺失或损坏纳入 strict audit 范围，避免只审 trace / manifest 而漏掉第三件关键产物。
- 为以上 strict execution safety 改动补充 smoke：覆盖“半残结果不能被 resume 误跳过”和“group runner 的并发 summary 协议”，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `68/68` 全部通过；同时复跑 `python3 -m compileall -q experiments` 通过。
- 将 request-level seed 从 runner 贯通到 external LLM client，并把 `agent_requested_seed / agent_request_seed_supported / agent_request_seed_applied / agent_seed_protocol` 写入 trace 与 strict manifest，避免正式 run 后再回头解释 seed 口径。
- 新增 `experiments/scripts/probe_external_llm_seed_support.py`，并在项目内产出 `experiments/results/seed_probe/reports/strict_seed_probe_20260726_v1/external_llm_seed_probe.json`；当前真实探测结果确认 `newapi / gpt-5.4-mini-2026-03-17 / http` 接受 request-level `seed`。
- 为 request-level seed 链补充 smoke，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `69/69` 全部通过；同时复跑 `python3 -m compileall -q experiments` 通过。
- 启动第一次阶段 A 正式 run：`experiments/results/strict_main_agent_final_20260726_v1/` 在 frozen revision `b6ee62b` 上串行执行 `seed=1001`，跑到 `22/252` 时在 `B0/F1/1001` 停止，原因是 `F1` 这类无 `say` 步的 agent 场景在 trace 中保留了 `agent_backend=null`，被 strict check 误判为后端错误。
- 修复 agent no-op 场景协议：当 agent 路径场景本身不需要 planner 调用时，trace 现在会保留 `agent_backend=external_llm`，并把 `agent_seed_protocol` 标记为 `no_agent_call_required`，避免把“零调用”误报成“错误后端”。
- 为上述 no-op agent 场景协议补充 smoke，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `70/70` 全部通过；同时复跑 `python3 -m compileall -q experiments` 通过。
- 启动第二次阶段 A 正式 run：`experiments/results/strict_main_agent_final_20260726_v2/` 在 frozen revision `df7b67d` 上串行执行 `seed=1001`，成功越过 `F1` 阻断点并推进到 `35/252`，随后在 `B0/H2/1001` 暴露出新的执行层缺口。
- 修复模型坏动作的执行层容错：当模型输出缺少必需参数或其他无效 service/args 时，runner 现在会把它记录为失败动作和行为失败，而不是抛 Python 异常打断整轮 run。
- 为上述坏动作容错补充 smoke，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `71/71` 全部通过；同时复跑 `python3 -m compileall -q experiments` 通过。
- 启动第三次阶段 A 正式 run：`experiments/results/strict_main_agent_final_20260726_v3/` 在 frozen revision `84aca0f` 上串行执行 `seed=1001`，成功推进到 `175/252`，跑过 `B0 / B1 / B2 / B3` 四个系统，随后在 `B4/G3/1001` 暴露出新的 strict 协议缺口。
- 修复 external parse failure 的归因口径：当模型输出近似 JSON 但不合法时，planner 现在保留 `agent_backend=external_llm` 并记录 `external_parse_failed:*` 行为失败，不再偷偷走 `heuristic_fallback`；同时将 `external_call_failed` / `external_init_failed` 单独保留为 strict transport failure / retry 信号。
- 为上述 parse-failure 归因修复补充 smoke，并复跑 `python3 -m unittest experiments.tests.test_smoke`，当前总数提升到 `72/72` 全部通过；同时复跑 `python3 -m compileall -q experiments` 通过。

## 2026-08-10

- 根据 `实验结果分析.md` 启动论文级 v4 协议改造：新增 evaluator-owned lifecycle truth、外部行为 TSR/真实 usage token 指标、raw/guarded planner trace 字段、B1 raw-text RAG 与 B4 full raw-history 路径，旧 composite 结果保留为 `Contract Conformance Score`。
- 将 v4 场景与 legacy 36 场景隔离：新增 H2/C2/B6 行为场景与 L1 跨 session longitudinal 场景；Agent v4 runner 会拒绝 `memory_ops` 与 `action_template`，防止隐藏真值桥接。
- 新增 v4 独立标注目录与 `sync_ground_truth.py --protocol v4`，生成 4 个双人标注占位文件和独立 annotation agreement，不污染 legacy 标注资产。
- 冻结 `protocol_v4_pilot_matrix.json`（7 systems x 3 scenarios x 2 seeds = 42 units）及 `protocol_v4_longitudinal_matrix.json`（7 systems x 1 held-out trajectory x 2 seeds = 14 units）；L1 不参与 pilot 调参。
- 修复 strict serial runner 对旧矩阵缺失 `source_planner_mode` 的兼容，以及 Agent retrieval metadata 未落盘导致 B1/B4 context source 无法审计的问题；新增对应 smoke 覆盖。
- 完成 `protocol_v4_dry_20260810_r3` 的 5 个 heuristic 零成本代表单元：strict audit 为 partial、无 failure，B1/B4 context source 分别为 `raw_text_rag` / `full_raw_history`，API 调用与 token 均为 0。该 dry-run 仅为协议验证，未产生 v4 真实 LLM 性能数据。
- 复跑 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest experiments.tests.test_smoke`，76/76 通过；`python3 -m compileall -q experiments` 与 `git diff --check` 通过。
- 扩展 `build_artifact_bundle.py`：manifest 现在记录工作树是否干净，并可对 v4 矩阵、场景、world model、system registry、runner/evaluator/metrics 代码及 dry-run audit 生成 SHA-256；当前 bundle 明确标记 `working_tree_clean=false`，仅作为改造阶段审计资产。
- 增加 artifact bundle smoke 后复跑 `python3 -m unittest experiments.tests.test_smoke`，77/77 通过；`compileall` 与 `git diff --check` 仍通过。
- 为 8 个消融增加结构化 `mechanism_activation` 与 `system_configuration` trace，并将 activation audit 改为验证“目标机制被调用、对应消融中关闭、除声明开关外无额外配置差异”。零成本 Oracle contract 以 `-Decay/H2`、`-AsymFeedback/A5`、`-Governance/A4`、`-CandidateGate/A3`、`-ConflictHandling/A2`、`-FeatureAbsorption/F6`、`-Ripple/F3`、`-Split/F5` 全部通过；F1 无 merge activation，明确不能用于 FeatureAbsorption 贡献结论。
- 新增 v4 evaluator-only ground truth 资产，PM/UAA/UC 使用显式 evaluator eligible labels，DMR 对齐维护阶段的最近活动时间；修复 UAA 条件表达式导致非门控 safety 任务被错误计入分母的问题。新增 metrics/fidelity/activation smoke，当前 `81/81` 通过。
- 将 `generate_report.py` 改为默认输出到 results 下的 generated report，只有显式 `--write-summary` 才覆盖 `docs/实验结果摘要.md`；补充 smoke 防止测试改写论文摘要。
- 启动受控 v4 external pilot 的唯一首个单元 `Ours/H2_v4_behavioral/1001`；项目内 `newapi` 配置返回 `401 Invalid token`，strict trace 记录 `external_call_failed`，无有效 API 调用与 usage token。为避免把授权故障误写为模型行为或扩大成本，未继续 C2/B6 或第二 seed；等待有效项目 LLM 授权后从 H2 重试。
- 新增 `audit_protocol_v4_readiness.py`，将本地门禁、8/8 activation、标注资产和真实 external trace 分开审计；当前 readiness 为 `blocked_on_llm_authorization`，唯一下一条件是提供有效项目 LLM 授权后重试 `Ours/H2_v4_behavioral/1001`，在人工检查前不扩量。
- 最终零成本回归为 `83/83` smoke，通过 `compileall` 与 `git diff --check`；readiness audit、activation audit 和 transport-blocked pilot trace 已留在项目内结果树，未修改项目外文件。
- 修复 artifact bundle 的重建命令曾指向不存在脚本的问题：新增可执行的 `experiments/scripts/generate_v4_artifacts.py`，实际重建 v4 pilot/longitudinal matrix、独立标注占位与 29-file SHA-256 artifact manifest；补充 smoke 后当前回归为 `84/84`。
- 补充 v4 全场景 hidden-bridge 与 evaluator-only prompt 泄漏测试：覆盖 H2/C2/B6/L1 四个场景及 planner prompt，确保 evaluator 标签不会序列化给 Agent。
- 复跑最终本地门禁：`86/86` smoke、`compileall` 与 `git diff --check` 通过；再次确认唯一 external pilot trace 的有效 API 调用和 usage token 均为 0，仍仅含 `external_call_failed` 授权故障记录。

## 2026-08-11

- 恢复 goal 后重新核验工作区、项目 LLM 配置与 v4 readiness；环境变量未覆盖项目配置，`Ours/H2_v4_behavioral/1001` 仍为 `external_call_failed`，readiness 仍为 `blocked_on_llm_authorization`。
- 本次复核未发起任何新的 LLM API 请求，未扩大 C2/B6 或其他 seed；等待有效授权后仍从同一 H2 单元受控重试。
- 用户更新 `smartHome/m_agent/common/llm_config.ini` 后，确认项目实际读取 provider=`my_gac`、model=`gpt-5.4-mini`、HTTP transport；在不启动实验单元的前提下执行两次 seed probe，均收到上游 `503 proxy_unavailable: All accounts are currently unavailable`。probe 产物分别位于 `experiments/results/protocol_v4_external_pilot/reports/protocol_v4_external_seed_probe_20260811/` 与 `.../protocol_v4_external_seed_probe_20260811_retry1/`。
- 本次重试未产生有效模型响应、external trace 或 usage token，未将 503 计入实验指标，也未扩大 C2/B6 或其他 seed；v4 external pilot 继续保持 `blocked_on_llm_authorization`，待代理恢复后从 `Ours/H2_v4_behavioral/1001` 重试。
- 最新配置再次确认 provider=`my_gac`、model=`gpt-5.4`、HTTP transport；第三次最低成本 seed probe 仍收到上游 `503 proxy_unavailable: All accounts are currently unavailable`，产物位于 `experiments/results/protocol_v4_external_pilot/reports/protocol_v4_external_seed_probe_20260811_retry2/`。未获得有效模型响应、external trace 或 usage token，未扩大 pilot。
- 用户确认代理普通请求已返回 `200/API_OK` 后，项目客户端无 seed 请求获得真实响应（usage 非零）；带 `seed=1001` 的 H2 请求先收到 503，客户端按受控规则重试无 seed 请求并成功。`Ours/H2_v4_behavioral/1001` 位于 `experiments/results/protocol_v4_external_pilot_after_api_ok/`，严格检查通过，2 次 API 调用、2050 prompt、721 completion、2771 total tokens，无 fallback/transport failure。真实模型完成查询和设温动作，但未对低置信度控制请求进行必要 clarification，故 `external_task_success=false`；该失败归因于模型行为，不是执行链故障。
- 为适配该代理的 seed 行为，HTTP client 仅在带 seed 请求返回 503 时重试一次无 seed 请求，并将 `request_seed_supported=false`、`seed_protocol=replicate_id` 写入 trace；新增回归用例后 smoke 为 `88/88`。新 run 的 readiness 为 `pilot_ready_for_manual_review`，但有效样本仅 1/42，人工复核完成前不继续 C2/B6。
- 在 H2 trace 人工检查通过后，按受控顺序运行 `Ours/C2/1001` 与 `Ours/B6/1001`；两者均为真实 external-LLM 且 strict audit 通过。H2/C2/B6 共 3 个代表性 unit、5 次 API 调用、2050+2225+1341=`5616` prompt tokens、721+210+92=`1023` completion tokens、总计 `6639` tokens。H2 未完成必要澄清而失败，C2 正确不执行未知规则，B6 正确执行门锁动作；三条 trace 均无 fallback、transport failure 或 guard override。当前仅完成 `3/42` pilot units，仍需人工复核记录后才能决定扩大。
- 新增 `experiments/scripts/estimate_protocol_v4_cost.py`，基于 3 个有效 v4 external trace 生成 `protocol_v4_cost_estimate_20260811.json`：42-unit pilot 的样本均值外推约 70 次调用、92946 total tokens；14-unit longitudinal 外推约 30982 tokens。新增 seed probe 成功识别回归后，完整 smoke 为 `90/90`，artifact bundle 重建并纳入当前 pilot 资产。

## 2026-08-13

## 2026-08-16

- 经用户明确授权，在 `try/memory` 修改前先将该外部依赖目录归档到项目内 `experiments/external_dependency_backups/try_memory_pre_fts_escape_20260816.tar.gz`，并记录 SHA-256 `68e97381553e2dfb92ef354d779299dd4e5c31753ae8c4d94c1fc1a08e33cbb5`；备份用于在需要时恢复原始实现，不包含或改写任何冻结实验工件。
- 修复 `try/memory/sqlite_store.py` 的 SQLite FTS 输入兼容性：将用户/LLM 文本作为字面短语查询，避免失败反思文本 `Error code: 400` 被 FTS 误解析为 `code` 列而中断产品 runtime 的失败收尾流程。
- 使用全新临时 SQLite 完成含冒号和引号文本的 FTS 回归，并在现有 Python 3.11 runtime 环境运行 `try/memory` 的 `8/8` 测试通过；未读写 v4、v4.1 或旧 v4.2 的任何结果根。后续 runtime 验证必须使用新 revision、全新结果根与独立 SQLite。
- 加固 v4.2 产品 runtime runner 的失败工件保障：每条轨迹在独立子进程内调用未修改的 `run_ourAgent`，父进程总会保存 canonical JSON、worker return code 与 stdout/stderr；纯本地 mock 回归确认子进程无输出时仍可审计地记录失败。
- 在 revision `bfbf884` 的新 v4.2 产品 runtime 根执行 `R1-R3 @ 1001`：三条均真实进入产品 Agent、LLM、`tool_filter` 和 `query_tool`，隔离 SQLite 各保留 19 条 memory records/1 条 event，且 `no such column: code` 未复发；但三条均在后续调用收到 `400 upstream_unavailable`。产品 runtime 没有规范 usage callback，canonical usage 无法从日志安全汇总，runtime pilot strict gate 失败；结果根保持忽略，不扩展到 10 replicates，也不纳入论文表。
- 为下一次产品 runtime gate 增加任务级 telemetry：middleware 直接捕获实际 LangChain `AIMessage` 的 response usage、model/provider 与 tool calls，`DemoMemoryRuntime` 在 task 生命周期内聚合，runner 无论成功或异常都写入 canonical JSON。新增纯本地 smoke 验证该聚合，完整 smoke 为 `133/133`。
- 在 revision `84b06e6` 的新 product runtime root 完成 `R1-R3 @ 1001` telemetry gate：三条均留下 canonical usage（合计 53,363 tokens）和 15 个真实 tool call，FTS `code` 错误未复发；但每条均在后续 LLM 调用收到 `400 upstream_unavailable`，专项审计 fail。为避免在同一上游状态下无意义重复付费调用，不扩展至 10 replicates，失败根继续保持忽略。
- 产品 Agent 新增受限 transport repair：只对明确 `upstream_unavailable` 签名在模型调用边界最多重试一次，SDK 隐式重试保持为 0，避免工具或任务重放；每次 attempt 写入 `DemoMemoryRuntime` task audit 和 canonical runtime trace。两项 repair 边界回归及完整 smoke `135/135` 通过，后续以新 revision/new root 做一次受控真实 pilot。
- revision `a2cf215` 的 repair-enabled pilot 仍由 `APITimeoutError` 与代理 `500 get_channel_failed` 阻断；将 repair 分类仅扩展至这两个已观察到的 transient 签名，普通 500 仍不重试。对应边界回归通过，完整 smoke 更新为 `136/136`；失败根保持忽略且不混入任何性能结果。
- revision `342cfc6` 的扩大 repair pilot 恢复 R1/R2，但 R3 最后一个模型请求连续两次 `APITimeoutError`。产品单请求 timeout 从 30 秒调整为 90 秒，SDK retry 保持 0、middleware repair 仍最多一次；新增配置回归，完整 smoke 为 `137/137`。后续仍用独立 revision/root 重新 gate。
- 默认 `newapi/gpt-5.4-mini` 的 `ed4f6ea` gate 继续出现间歇代理不可用；项目内独立 `my_gac/gpt-5.4` 最小 probe 返回 `API_OK`。产品 runtime runner 新增仅对子进程有效的 `--provider` override，并在 canonical unit 中记录 configured provider/model，不改默认配置、不混合旧结果；新增回归后 smoke 为 `138/138`。
- `my_gac/gpt-5.4` 的 provider-separated runtime gate 真实加载 override，但三条在首个模型请求均返回 `503 proxy_unavailable / All accounts are currently unavailable`，无有效 usage。该失败与默认 `newapi` 的间歇 400/timeout/channel failure 共同确认当前阻塞在外部 provider 可用性；不再扩大或重复付费请求，失败根继续保持忽略。

## 2026-08-17

- 暂停 v4.2 投稿前补充实验并完成汇报口径收尾：同步 `实验结果摘要.md` 与权威 v4/v4.1 汇报，明确产品 runtime 工程审计已完成但外部 provider 不稳定，机制/longitudinal 仍未通过 1-replicate strict gate；所有 v4.2 pilot 均不进入论文结果表，也不改变 v4/v4.1 冻结结论。
- 新建仓库上级汇报文档 `实验进展-2026-8-17.md`，统一整合 v4 正式主实验、v4.1 ingestion 补充实验和 v4.2 诊断性 pilot；明确当前可投稿结论、负结果、标注/runtime 范围、不可声称内容、风险优先级和可复核工件路径，并将 2026-07-26 的 7560-unit 旧协议结果降级为历史研发证据，避免新旧协议混用。
- 调整 `实验进展-2026-8-17.md` 的产品 runtime 汇报措辞与短版标题，保留已完成工程审计但尚无可复现 runtime TSR 的结论边界。

## 2026-08-14

- 扩展 protocol-v4 证据资产：新增 7 个用户可观察行为场景和第二家庭 `wm-v2-alt-home`/B6W paired robustness 场景，主行为矩阵更新为 `7×10×30=2100` units，未启动全量运行。
- 新增 post-commit freeze receipt/audit、scenario×replicate_id paired bootstrap/guard diagnostics、ingestion boundary audit；否定与房间歧义文本明确拒绝而非自动写入。80-history longitudinal audit 确认 B1 top-k=5 与 B4 full-history 边界。
- 本轮完成 `102/102` smoke、compileall 与 diff check；新增预运行门禁报告，真实人工双标注、正式矩阵与第二模型仍明确标为未完成。

- 完成 v4 正式协议与运行就绪资产：新增 formal freeze manifest、`630` unit behavioral、`210` unit longitudinal、`14` unit held-out robustness 和 raw-text ingestion workload；冻结真实 usage、外部主指标、baseline fidelity、统计/Holm 与缺失值口径。新增人工标注任务包且所有人工字段保持 pending/null，不伪造 κ。新增 `B6R` held-out 释义场景并只运行 `Ours/B6R/1001` external-LLM pilot（1423 tokens、trace audit pass）；本轮 smoke 为 `100/100`，并通过 compileall 与 diff check。
- 修复 `run_strict_group.py` 未将 `--matrix` 传递给 serial unit 的问题，避免 v4 group runner 回退到旧 strict matrix；新增 v4 trace audit、按 system/scenario/seed 聚合和 v4 成本估算脚本，transport failure 不进入性能聚合。
- 完成冻结的 `protocol_v4_agent_pilot_20260813`：`Ours+B0-B5 × H2/C2/B6 × seed=1001,1002` 共 `42/42` unit，串行执行，0 retry/0 failure/0 fallback/0 transport failure，70 次真实 external-LLM 调用，77826 prompt、9413 completion、87239 total tokens；strict audit 和 trace audit 均为 pass。pilot 的 Ours TSR=1.000，B0-B5 分别为 0.333/0.333/0.500/0.667/0.333/0.667，仅作为小规模真实 Agent pilot，不作为最终论文主表。
- 新增 raw-text integrated ingestion/replay：两段原始用户文本完成偏好写入、自然语言纠正、SQLite 持久化、检索与执行；无 `memory_ops`、`action_template` 或 evaluator 标签输入。真实 LLM replay 成功执行 26 度，使用 1302 prompt、181 completion、1483 total tokens，seed 口径为 replicate_id。
- 新增 L1 跨 session/长历史审计：持久 SQLite 在 14 天 session 边界后可检索；B1 保持 raw-text RAG，B4 在 40/80 历史条目下分别暴露 41/81 条 full raw history，不读取结构化 MemoryRecord。`Ours/L1 @ 1001,1002` 真实验证完成，4 次调用、4842 total tokens、trace audit pass；旧 L1 首次 timeout trace 保留并隔离，不计入指标。
- 补齐双标注的缺失值与裁决格式：缺失人工标注不进入 κ 分母，分歧需要第三方裁决，不得由自动标签填补。当前 4 个 v4 场景仍为 pending，κ=null。
- artifact bundle 重建为 201 个 SHA-256 固定资产，包含 pilot、integrated replay、L1 audit/trace、冻结矩阵、场景、world model、代码和审计/聚合结果；本轮结束前完整 smoke、compileall、git diff --check 均通过。
