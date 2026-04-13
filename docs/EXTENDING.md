# Fake Home Assistant v2 扩展指南

本文档说明如何为当前模拟器新增设备、实体、service、actions 和自定义 handler。

## 1. 扩展前先判断选哪条路

优先顺序：

1. 声明式设备/实体
2. 实体 actions
3. Python handler

简单判断：

- 只是新增一个普通设备或实体，直接写定义
- 只是按钮联动、调用其他 service、发事件，优先写 actions
- 存在复杂校验、复杂状态计算、复杂副作用，才写 Python handler

详细原则见：

- [DESIGN_RULES.md](F:\coding_workspace\codex_workspace\homeassitant_demo\docs\DESIGN_RULES.md)

## 2. 扩展入口一览

### 方式 A：通过 API 动态新增

适合：

- 调试
- 小规模新增
- 运行时快速验证

接口：

- `PUT /api/mock/devices/{device_id}`
- `PUT /api/mock/entities/{entity_id}`

注意：

- 这是运行时定义管理接口
- 写入后会持久化到 `.fake_homeassistant`

### 方式 B：直接写运行时定义文件

适合：

- 本地准备一批静态数据
- 希望服务启动后自动加载

目录：

- `.fake_homeassistant/devices/`
- `.fake_homeassistant/entities/`
- `.fake_homeassistant/services/`

写入后可以调用：

- `POST /api/mock/reload`

### 方式 C：修改仓库默认实现

适合：

- 新增通用内置行为
- 完善默认 service 定义
- 增加新的内置 handler

涉及位置：

- [base.yaml](F:\coding_workspace\codex_workspace\homeassitant_demo\src\fake_homeassistant_v2\data\services\base.yaml)
- [runtime.py](F:\coding_workspace\codex_workspace\homeassitant_demo\src\fake_homeassistant_v2\runtime.py)
- [tests/test_api.py](F:\coding_workspace\codex_workspace\homeassitant_demo\tests\test_api.py)

## 3. 新增实体的最小步骤

如果目标只是增加一个能被查询和调用的实体，最少需要：

1. 确定 `entity_id`
2. 确定 `domain`
3. 定义初始 `state`
4. 定义必要的 `attributes`
5. 如果该 domain 已有可复用的 service，就不需要再改 handler

最小实体示例：

```json
{
  "entity": {
    "entity_id": "switch.demo_lamp_power",
    "domain": "switch",
    "object_id": "demo_lamp_power",
    "state": "off",
    "attributes": {
      "friendly_name": "Demo Lamp Power"
    }
  }
}
```

调用方式：

```powershell
curl -X PUT http://127.0.0.1:8123/api/mock/entities/switch.demo_lamp_power `
  -H "Content-Type: application/json" `
  -d "@entity.json"
```

## 4. 新增设备的最小步骤

如果一个设备包含多个实体，建议一次性用设备接口注册。

最小设备示例：

```json
{
  "device": {
    "device_id": "device.demo_lamp",
    "name": "Demo Lamp",
    "manufacturer": "Demo",
    "model": "Lamp",
    "entities": []
  },
  "entities": [
    {
      "entity_id": "switch.demo_lamp_power",
      "domain": "switch",
      "object_id": "demo_lamp_power",
      "device_id": "device.demo_lamp",
      "state": "off",
      "attributes": {
        "friendly_name": "Demo Lamp Power"
      }
    }
  ]
}
```

## 5. 新增 service 的最小步骤

如果现有 domain 没有对应 service，需要新增 `ServiceDefinition`。

service 定义最少包含：

- `domain`
- `service`
- `name`
- `fields`
- `handler`

最小示例：

```yaml
domain: fan
service: set_percentage
name: Set percentage
description: Set a fan percentage.
fields:
  entity_id:
    required: true
  percentage:
    required: true
target:
  entity:
    - {}
handler: tests.custom_handlers:fan_set_percentage
supports_response: true
```

如果 handler 指向的是自定义 Python 实现，运行时会按 `module:function` 方式动态加载。

## 6. 什么时候用 actions

actions 适合表达：

- 按按钮后调用另一个 service
- 修改另一个实体状态
- 发送一个事件

支持的 action 类型：

- `call_service`
- `set_state`
- `fire_event`

按钮联动灯的示例：

```json
{
  "actions": {
    "on_press": [
      {
        "type": "call_service",
        "domain": "light",
        "service": "toggle",
        "data": {
          "entity_id": "${links.light}"
        }
      }
    ]
  },
  "links": {
    "light": "light.demo_lamp"
  }
}
```

占位符支持读取：

- `${entity_id}`
- `${links.xxx}`
- `${payload.xxx}`
- `${attributes.xxx}`

## 7. 什么时候写 Python handler

出现下面情况时，直接写 handler：

- 参数校验明显复杂
- 需要根据多个属性计算状态
- 需要跨多个实体做复杂联动
- actions 表达起来已经不清晰
- 返回值需要明确的 `service_response`

自定义 handler 示例可以参考：

- [tests/custom_handlers.py](F:\coding_workspace\codex_workspace\homeassitant_demo\tests\custom_handlers.py)

## 8. 推荐扩展流程

新增一个扩展时，按这个顺序做：

1. 先确认目标是否能复用现有 domain 和内置 service
2. 能复用就只写设备/实体定义
3. 如果需要简单联动，先尝试 actions
4. 如果 actions 不够，再增加 Python handler
5. 如果引入了新的 service，就补 `ServiceDefinition`
6. 最后补测试和文档

## 9. 每次扩展至少验证什么

最少验证：

1. 新实体能在 `/api/states` 中看到
2. 对应 service 能调用成功
3. 状态变化后会持久化
4. 重启后状态或定义符合预期

如果新增的是 service 或 handler，还应额外验证：

1. 缺失必填字段时返回 `400`
2. 非法实体返回 `404`
3. 如果声明支持 `return_response`，返回结构正确

## 10. 文档更新约定

扩展完成后按需更新：

- 对外接口变化：更新 [API.md](F:\coding_workspace\codex_workspace\homeassitant_demo\docs\API.md)
- 内部机制变化：更新 [ARCHITECTURE.md](F:\coding_workspace\codex_workspace\homeassitant_demo\docs\ARCHITECTURE.md)
- 扩展规则变化：更新 [DESIGN_RULES.md](F:\coding_workspace\codex_workspace\homeassitant_demo\docs\DESIGN_RULES.md)

不要把这些知识重新堆回 `README.md`。
