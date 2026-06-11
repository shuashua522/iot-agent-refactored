# WORKLOG

## 2026-06-11

- 模块：`try/memory`
  核心改动：新增 Memory V1 独立模块，包含 SQLite canonical store、FTS5 检索、HA 同步、Hybrid resolver、更新策略、usage tracker 与 maintenance。
  测试/接入影响：新增独立单元测试；后续由 demo 侧适配接入。
  文档更新：已同步新增本工作记录，并更新根 README 的记忆模块说明。

- 模块：`iot-agent-refactored_demo/smartHome/m_agent/memory`
  核心改动：新增 demo memory runtime，负责加载 Memory V1、同步 HA、写入样例 seed 记忆、跟踪任务级 memory usage。
  测试/接入影响：`query_tool` 从静态文本切换为真实 memory 检索；`base_home_agent` 增加任务开始/结束的记忆生命周期钩子。
  文档更新：已同步新增本工作记录，并更新根 README 的记忆模块说明。

- 模块：测试
  核心改动：新增 `try/memory` 单元测试与 demo `query_tool` 适配测试，覆盖 HA 同步、别名绑定、修订、降级、reflection 和检索摘要。
  测试/接入影响：优先可本地直接运行，不依赖额外外网；需要时仍可结合本地 Docker 环境联调。
  文档更新：已同步记录到本工作记录。
