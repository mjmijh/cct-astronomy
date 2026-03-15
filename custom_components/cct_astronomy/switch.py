from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_ENABLED, DEFAULT_ENABLED
from .coordinator import CctCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator: CctCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CctAutomationSwitch(hass, coordinator, entry)])


class CctAutomationSwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "Automation"
    _attr_icon = "mdi:robot"

    def __init__(self, hass: HomeAssistant, coordinator: CctCoordinator, entry: ConfigEntry):
        self.hass = hass
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_automation"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="CCT Astronomy",
            model="Astronomic CCT (Kelvin/Mired)",
        )

    async def async_added_to_hass(self):
        self.coordinator.async_add_listener(self.async_write_ha_state)

    @property
    def is_on(self) -> bool:
        return bool(self.entry.options.get(CONF_ENABLED, self.entry.data.get(CONF_ENABLED, DEFAULT_ENABLED)))

    async def async_turn_on(self, **kwargs):
        opts = dict(self.entry.options)
        opts[CONF_ENABLED] = True
        self.hass.config_entries.async_update_entry(self.entry, options=opts)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        opts = dict(self.entry.options)
        opts[CONF_ENABLED] = False
        self.hass.config_entries.async_update_entry(self.entry, options=opts)
        await self.coordinator.async_request_refresh()
