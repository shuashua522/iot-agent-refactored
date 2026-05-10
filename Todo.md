## 可靠性的问题

1. 在小范围测试上的延时有点高：基本都要150s以上才能出结果。 考虑是因为可靠性检测是重新调用了一次agent,但即使这样砍半也需要几十秒。

**验证结果样例：**

```
验证查询结果（基于周边传感器数据）：

用于验证的 execution_completed_at：
- execution_completed_at: 2026-05-06T12:05:05.197170+08:00

1) 客厅（目标：客厅空调设定温度为 25°C，制冷模式保持）
- 使用的周边传感器：
  - entity_id: sensor.test_living_room_temperature_main  
    - friendly_name: 客厅温度传感器  
    - current state: 25.0 °C  
    - last_changed: 2026-05-06T12:04:11.507253+08:00  
    - last_updated: 2026-05-06T12:04:11.507253+08:00  
    - 与目标设备的关系：同一房间（客厅），可作为旁证环境温度
- 说明与判断依据：
  - 该传感器当前温度 25.0°C 与目标设定温度 25°C 一致（符合预期）。  
  - 该传感器的最近状态变更时间（12:04:11.507）距离 execution_completed_at（12:05:05.197）约 54 秒，时间上非常接近，表明温度变化发生在或紧接在本次操作前后，能够作为本次操作生效的旁证。  
结论（客厅）：通过。  
理由：同一房间的温度传感器状态与期望一致，且其最近变更时间与本次执行时间接近，满足“状态+时间接近”判定规则。

2) 卧室（目标：卧室空调设定温度为 26°C，制冷模式保持）
- 使用的周边传感器：
  - entity_id: sensor.test_bedroom_temperature_main  
    - friendly_name: 卧室温度传感器  
    - current state: 26.0 °C  
    - last_changed: 2026-05-06T12:04:09.245152+08:00  
    - last_updated: 2026-05-06T12:04:09.245152+08:00  
    - 与目标设备的关系：同一房间（卧室），可作为旁证环境温度
- 说明与判断依据：
  - 该传感器当前温度 26.0°C 与目标设定温度 26°C 一致（符合预期）。  
  - 该传感器的最近状态变更时间（12:04:09.245）距离 execution_completed_at（12:05:05.197）约 56 秒，时间上非常接近，能够作为本次操作生效的旁证。  
结论（卧室）：通过。  
理由：同一房间的温度传感器状态与期望一致，且其最近变更时间与本次执行时间接近，满足“状态+时间接近”判定规则。

补充说明：
- 我主要依据的是两个房间内的温度传感器（周边传感器），并未把空调设备自身的 state 作为最终判定依据；空调设备的状态可作为辅助信息但不是本次结论的主要证据。  
- 时间证据完整（包含 last_changed 与 execution_completed_at），且变更时间与执行完成时间接近，所以不属于“早于执行且无法判断”的情况。若你希望更严格的判定阈值或需要进一步观测一段时间以确认温度稳定性，我可以继续监测或读取更多周边传感器（如湿度、人体/运动感应器等）。
```

### 当前 demo 测试场景

- 使用的场景：`normal`、`one_shot_network_error`、`fake_success`
- 对应测试案例：
  - `te_normal_pair_a_v1`
  - `te_normal_pair_b_v1`
  - `te_one_shot_network_error_pair_a_v1`
  - `te_one_shot_network_error_pair_b_v1`
  - `te_fake_success_pair_a_v1`
  - `te_fake_success_pair_b_v1`
- 这些测试案例涉及的设备：
  - 客厅空调设备：`device.test_living_room_ac_main`
  - 客厅温度传感器设备：`device.test_living_room_temperature_sensor_main`
  - 卧室空调设备：`device.test_bedroom_ac_main`
  - 卧室温度传感器设备：`device.test_bedroom_temperature_sensor_main`



待修改的部分：

- 路由节点提示词，因为可能在检查时，由于执行结果中包含实体ID，直接使用这些实体或者被这些执行计划的结果误导，导致没拿出正确的实体ID或生成正确的格式，导致验证失败。 `"callback failed: Failed to parse structured output for tool 'EntityIdList': Failed to parse data to EntityIdList: 2 validation errors for EntityIdList\nentities.0.entity_name\n  Field required [type=missing, input_value={'entity_id': 'sensor.tes...于验证温度变化'}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.12/v/missing\nentities.1.entity_name\n  Field required [type=missing, input_value={'entity_id': 'sensor.tes...感器，作为参考'}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.12/v/missing."`
- 

## 隐私处理

问题1：（429:上游 API 拒绝了过量或超额请求。）

```
"callback failed: Error code: 429 - {'error': {'code': 'bad_response_status_code', 'message': 'Provider API error: bad response status code 429', 'param': '429', 'type': 'upstream_error'}}"
```

1. 一开始隐私处理和正常agent都是用gpt5mini
2. 把隐私处理换成deepseek，还是429。但发现不是隐私处理那里的量的问题，还是gpt5mini的问题。

3. 都换成deepseek-reasoner：`"callback failed: Error code: 400 - {'error': {'message': 'deepseek-reasoner does not support this tool_choice', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_request_error'}}"`

问题2：deepseek-reasoner在隐私处理时的返回格式不对。在更小的模型上可能会出现更多类似的问题。

```
"callback failed: LLM 返回内容必须包含 'encoded_text' 对象：{}"
```

### 当前 demo 测试场景

- 使用的场景：两个正常环境下的隐私处理执行场景
- 对应测试案例：
  - `te_normal_pair_a_v1`
  - `te_normal_pair_b_v1`
- 这些测试案例涉及的设备：
  - 客厅空调设备：`device.test_living_room_ac_main`
  - 客厅温度传感器设备：`device.test_living_room_temperature_sensor_main`
  - 卧室空调设备：`device.test_bedroom_ac_main`
  - 卧室温度传感器设备：`device.test_bedroom_temperature_sensor_main`
