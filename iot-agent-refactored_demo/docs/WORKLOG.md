# WORKLOG

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
