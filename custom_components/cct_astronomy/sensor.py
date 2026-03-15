from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CctCoordinator
from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class CctDesc(SensorEntityDescription):
    key: str


DESCRIPTIONS = (
    CctDesc(
        key="cct_kelvin",
        name="Kelvin",
        icon="mdi:thermometer",
        native_unit_of_measurement="K",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    CctDesc(
        key="cct_mired",
        name="Mired",
        icon="mdi:thermometer",
        native_unit_of_measurement="mired",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    CctDesc(
        key="dim",
        name="Dim",
        icon="mdi:brightness-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator: CctCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CctSensor(coordinator, entry, d) for d in DESCRIPTIONS])


class CctSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: CctCoordinator, entry: ConfigEntry, desc: CctDesc):
        self.coordinator = coordinator
        self.entry = entry
        self.entity_description = desc
        self._attr_unique_id = f"{entry.entry_id}_{desc.key}"
        self._attr_name = desc.name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="CCT Astronomy",
            model="Astronomic CCT (Kelvin/Mired)",
        )

    async def async_added_to_hass(self):
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        self.coordinator.async_remove_listener(self.async_write_ha_state)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def native_value(self) -> Any:
        data = self.coordinator.data or {}
        val = data.get(self.entity_description.key)
        if self.entity_description.key == "cct_kelvin" and val is not None:
            return int(round(float(val)))
        if self.entity_description.key == "cct_mired" and val is not None:
            return int(round(float(val)))
        if self.entity_description.key == "dim" and val is not None:
            return float(val)
        return val

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        data = self.coordinator.data or {}
        return {
            "phase": data.get("phase"),
            "fade_seconds": data.get("fade_seconds"),
            "enabled": data.get("enabled"),
            "apply_service": data.get("apply_service"),
        }
