from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .config import Settings
from .models import DeviceDefinition, EntityDefinition, ServiceDefinition, StateRecord
from .runtime import FakeHomeAssistantRuntime, StorageManager


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _infer_profile(entity_id: str, domain: str, state: Any, attributes: dict[str, Any]) -> dict[str, Any]:
    profile: dict[str, Any] = {}
    for key in ("min", "max", "step"):
        if key in attributes:
            profile[key] = attributes[key]
    if domain == "text":
        pattern = attributes.get("pattern")
        text_value = str(state)
        if not pattern:
            if re.fullmatch(r"\d{2}:\d{2}-\d{2}:\d{2}", text_value):
                pattern = r"\d{2}:\d{2}-\d{2}:\d{2}"
            elif re.fullmatch(r"\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}", text_value):
                pattern = r"\d{2}:\d{2}:\d{2}-\d{2}:\d{2}:\d{2}"
        if pattern:
            profile["pattern"] = pattern
    if domain == "light":
        if "effect_list" in attributes:
            profile["effect_list"] = attributes["effect_list"]
    if entity_id.endswith("_dvalue_p_3_1"):
        profile.setdefault("min", 0)
        profile.setdefault("max", 21600)
    return profile


def _device_domain_map(entity_registry_entries: list[dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    by_device: dict[str, dict[str, list[str]]] = {}
    for item in entity_registry_entries:
        device_id = item.get("device_id")
        if not device_id:
            continue
        domain = item["entity_id"].split(".", 1)[0]
        by_device.setdefault(device_id, {}).setdefault(domain, []).append(item["entity_id"])
    return by_device


def _infer_links_and_actions(entity_id: str, domain: str, device_id: str | None, by_device: dict[str, dict[str, list[str]]]) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    links: dict[str, Any] = {}
    actions: dict[str, list[dict[str, Any]]] = {}
    if device_id is None:
        return links, actions

    device_entities = by_device.get(device_id, {})
    lights = device_entities.get("light", [])
    players = device_entities.get("media_player", [])

    if domain == "button" and lights:
        links["light"] = lights[0]
        if entity_id.endswith("_toggle_a_2_1"):
            actions["on_press"] = [
                {"type": "call_service", "domain": "light", "service": "toggle", "data": {"entity_id": "${links.light}"}}
            ]
        elif entity_id.endswith("_brightness_down_a_3_1"):
            actions["on_press"] = [
                {
                    "type": "call_service",
                    "domain": "light",
                    "service": "turn_on",
                    "data": {"entity_id": "${links.light}", "brightness_step_pct": -10},
                }
            ]
        elif entity_id.endswith("_brightness_up_a_3_2"):
            actions["on_press"] = [
                {
                    "type": "call_service",
                    "domain": "light",
                    "service": "turn_on",
                    "data": {"entity_id": "${links.light}", "brightness_step_pct": 10},
                }
            ]

    if domain == "button" and players:
        links["media_player"] = players[0]
        if entity_id.endswith("_play_music_a_7_5"):
            actions["on_press"] = [
                {
                    "type": "call_service",
                    "domain": "media_player",
                    "service": "media_play",
                    "data": {"entity_id": "${links.media_player}"},
                }
            ]

    return links, actions


def _service_handler_name(key: str) -> str:
    default_handlers = {
        "switch.turn_on": "builtin:switch.turn_on",
        "switch.turn_off": "builtin:switch.turn_off",
        "switch.toggle": "builtin:switch.toggle",
        "light.turn_on": "builtin:light.turn_on",
        "light.turn_off": "builtin:light.turn_off",
        "light.toggle": "builtin:light.toggle",
        "number.set_value": "builtin:number.set_value",
        "text.set_value": "builtin:text.set_value",
        "select.select_first": "builtin:select.select_first",
        "select.select_last": "builtin:select.select_last",
        "select.select_next": "builtin:select.select_next",
        "select.select_previous": "builtin:select.select_previous",
        "select.select_option": "builtin:select.select_option",
        "button.press": "builtin:button.press",
        "media_player.volume_set": "builtin:media_player.volume_set",
        "media_player.volume_up": "builtin:media_player.volume_up",
        "media_player.volume_down": "builtin:media_player.volume_down",
        "media_player.volume_mute": "builtin:media_player.volume_mute",
        "media_player.media_play": "builtin:media_player.media_play",
        "media_player.media_pause": "builtin:media_player.media_pause",
        "media_player.media_play_pause": "builtin:media_player.media_play_pause",
        "media_player.media_stop": "builtin:media_player.media_stop",
        "media_player.media_previous_track": "builtin:media_player.media_previous_track",
        "media_player.media_next_track": "builtin:media_player.media_next_track",
        "notify.send_message": "builtin:notify.send_message",
        "homeassistant.turn_on": "builtin:homeassistant.turn_on",
        "homeassistant.turn_off": "builtin:homeassistant.turn_off",
        "homeassistant.toggle": "builtin:homeassistant.toggle",
        "homeassistant.update_entity": "builtin:homeassistant.update_entity",
        "homeassistant.save_persistent_states": "builtin:homeassistant.save_persistent_states",
    }
    return default_handlers.get(key, "builtin:service.not_implemented")


def import_legacy_data(legacy_root: Path, storage: StorageManager) -> None:
    devices_payload = _read_json(legacy_root / "device_registry.json")
    entity_registry_payload = _read_json(legacy_root / "entity_registry.json")
    states_payload = _read_json(legacy_root / "entities.json")
    services_payload = _read_json(legacy_root / "domains_services.json")

    device_entries = devices_payload["data"]["devices"]
    entity_registry_entries = entity_registry_payload["data"]["entities"]
    state_by_entity = {item["entity_id"]: item for item in states_payload}
    entity_registry_by_id = {item["entity_id"]: item for item in entity_registry_entries}
    by_device = _device_domain_map(entity_registry_entries)

    for device_item in device_entries:
        device_id = device_item["id"]
        entities = sorted(by_device.get(device_id, {}).get("binary_sensor", []))
        for entity_ids in by_device.get(device_id, {}).values():
            entities.extend(entity_ids)
        device = DeviceDefinition(
            device_id=device_id,
            name=device_item.get("name"),
            name_by_user=device_item.get("name_by_user"),
            area_id=device_item.get("area_id"),
            manufacturer=device_item.get("manufacturer"),
            model=device_item.get("model"),
            model_id=device_item.get("model_id"),
            sw_version=device_item.get("sw_version"),
            hw_version=device_item.get("hw_version"),
            serial_number=device_item.get("serial_number"),
            identifiers=device_item.get("identifiers", []),
            connections=device_item.get("connections", []),
            configuration_url=device_item.get("configuration_url"),
            via_device_id=device_item.get("via_device_id"),
            entities=sorted(set(entities)),
            metadata={k: v for k, v in device_item.items() if k not in {"id", "name", "name_by_user", "area_id", "manufacturer", "model", "model_id", "sw_version", "hw_version", "serial_number", "identifiers", "connections", "configuration_url", "via_device_id"}},
        )
        storage.write_device(device)

    states: dict[str, StateRecord] = {}
    for entity_id, state_item in state_by_entity.items():
        registry_item = entity_registry_by_id.get(entity_id, {})
        domain, object_id = entity_id.split(".", 1)
        attributes = state_item.get("attributes", {})
        profile = _infer_profile(entity_id, domain, state_item.get("state"), attributes)
        links, actions = _infer_links_and_actions(entity_id, domain, registry_item.get("device_id"), by_device)
        entity = EntityDefinition(
            entity_id=entity_id,
            domain=domain,
            object_id=object_id,
            unique_id=registry_item.get("unique_id"),
            device_id=registry_item.get("device_id"),
            area_id=registry_item.get("area_id"),
            platform=registry_item.get("platform", "legacy_import"),
            name=registry_item.get("name"),
            original_name=registry_item.get("original_name"),
            device_class=registry_item.get("device_class") or registry_item.get("original_device_class"),
            entity_category=registry_item.get("entity_category"),
            hidden_by=registry_item.get("hidden_by"),
            disabled_by=registry_item.get("disabled_by"),
            supported_features=registry_item.get("supported_features", attributes.get("supported_features", 0)),
            capabilities=registry_item.get("capabilities"),
            service_profile=profile,
            links=links,
            actions=actions,
            state=state_item.get("state", "unknown"),
            attributes=attributes,
            metadata={k: v for k, v in registry_item.items() if k not in {"entity_id", "device_id", "unique_id", "area_id", "platform", "name", "original_name", "device_class", "original_device_class", "entity_category", "hidden_by", "disabled_by", "supported_features", "capabilities"}},
        )
        storage.write_entity(entity)
        states[entity_id] = StateRecord.model_validate(state_item)

    storage.write_states(states)

    existing_services = storage.load_services()
    for domain_item in services_payload:
        domain = domain_item["domain"]
        for service_name, service_item in domain_item.get("services", {}).items():
            key = f"{domain}.{service_name}"
            existing = existing_services.get(key)
            merged = ServiceDefinition(
                domain=domain,
                service=service_name,
                name=service_item.get("name", existing.name if existing else service_name),
                description=service_item.get("description", existing.description if existing else None),
                fields=service_item.get("fields", existing.fields if existing else {}),
                target=service_item.get("target", existing.target if existing else None),
                handler=existing.handler if existing else _service_handler_name(key),
                supports_response=existing.supports_response if existing else False,
            )
            storage.write_service(merged)


def bootstrap_runtime(settings: Settings, extra_handlers: dict[str, Any] | None = None) -> FakeHomeAssistantRuntime:
    storage = StorageManager(settings.storage_root)
    storage.seed_services(settings.service_seed_root)
    if not any(storage.list_data_files(storage.entities_dir)) and settings.legacy_root is not None:
        import_legacy_data(settings.legacy_root, storage)
    runtime = FakeHomeAssistantRuntime(settings, storage)
    runtime.reload()
    for name, func in (extra_handlers or {}).items():
        runtime.handlers.register(name, func)
    return runtime
