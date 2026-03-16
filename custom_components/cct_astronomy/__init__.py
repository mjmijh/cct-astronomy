from __future__ import annotations

import logging
import os
from typing import Any, Callable

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.light import ATTR_SUPPORTED_COLOR_MODES, ColorMode

_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    SERVICE_APPLY_TO_LIGHT,
    SERVICE_APPLY_TO_LIGHT_PREFIX,
    ATTR_LIGHT_ENTITY_ID,
    ATTR_TRANSITION,
    CONF_ENABLED,
    DEFAULT_ENABLED,
)
from .coordinator import CctCoordinator

PLATFORMS: list[str] = ["sensor", "switch"]

_PANEL_URL_PATH = "cct-astronomy"
_STATIC_URL_PATH = "/cct_astronomy"

def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v) for v in value]
    return [str(value)]

def _kelvin_to_mired(k: float) -> int:
    if k <= 0:
        return 0
    return int(round(1_000_000 / k))

def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def _choose_color_temp_payload(state_attrs: dict, cct_kelvin: int) -> dict:
    supported = state_attrs.get(ATTR_SUPPORTED_COLOR_MODES) or []
    supported_set = set(str(x) for x in supported)

    min_mireds = state_attrs.get("min_mireds")
    max_mireds = state_attrs.get("max_mireds")

    if str(ColorMode.COLOR_TEMP) in supported_set or "color_temp" in supported_set:
        payload = {"color_temp_kelvin": int(cct_kelvin)}
        if min_mireds is not None and max_mireds is not None:
            m = _kelvin_to_mired(cct_kelvin)
            m = int(_clamp(m, float(min_mireds), float(max_mireds)))
            if m > 0:
                payload["color_temp_kelvin"] = int(round(1_000_000 / m))
        return payload

    mired = _kelvin_to_mired(cct_kelvin)
    if min_mireds is not None and max_mireds is not None:
        mired = int(_clamp(mired, float(min_mireds), float(max_mireds)))
    return {"color_temp": int(mired)}

def _make_apply_handler(hass: HomeAssistant, entry: ConfigEntry, coordinator: CctCoordinator) -> Callable[[ServiceCall], Any]:
    async def _handler(call: ServiceCall) -> None:
        enabled = bool(entry.options.get(CONF_ENABLED, entry.data.get(CONF_ENABLED, DEFAULT_ENABLED)))
        if not enabled:
            return

        targets = _as_list(call.data.get(ATTR_LIGHT_ENTITY_ID))
        if not targets:
            return

        cct_kelvin = int(round(float(coordinator.data.get("cct_kelvin", 0))))
        phase = str(coordinator.data.get("phase", "day"))

        transition = call.data.get(ATTR_TRANSITION)
        if transition is None:
            defaults = coordinator.transition_defaults()
            transition = defaults.get(phase, defaults.get("day", 60))

        for entity_id in targets:
            state = hass.states.get(entity_id)
            if state is None:
                continue

            payload = _choose_color_temp_payload(state.attributes or {}, cct_kelvin)
            payload["entity_id"] = entity_id
            if transition is not None:
                payload["transition"] = float(transition)

            await hass.services.async_call(
                "light",
                "turn_on",
                payload,
                blocking=True,
            )
    return _handler

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    # Register static path for the bundled webapp (once per HA process)
    if not hass.data[DOMAIN].get("static_path_registered"):
        webapp_dir = os.path.join(os.path.dirname(__file__), "www")
        if os.path.isdir(webapp_dir):
            try:
                await hass.http.async_register_static_paths([
                    StaticPathConfig(_STATIC_URL_PATH, webapp_dir, cache_headers=False)
                ])
                hass.data[DOMAIN]["static_path_registered"] = True
            except Exception as err:
                _LOGGER.warning("Could not register static path for webapp: %s", err)

    # Register sidebar panel (once — panels are global, not per entry)
    if not hass.data[DOMAIN].get("panel_registered"):
        try:
            frontend.async_register_built_in_panel(
                hass,
                component_name="iframe",
                sidebar_title="CCT Astronomy",
                sidebar_icon="mdi:weather-sunset",
                frontend_url_path=_PANEL_URL_PATH,
                config={"url": f"{_STATIC_URL_PATH}/index.html"},
                require_admin=False,
            )
            hass.data[DOMAIN]["panel_registered"] = True
        except Exception:
            pass

    coordinator = CctCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    per_entry_service = f"{SERVICE_APPLY_TO_LIGHT_PREFIX}{entry.entry_id}"
    hass.services.async_register(DOMAIN, per_entry_service, _make_apply_handler(hass, entry, coordinator))

    if not hass.services.has_service(DOMAIN, SERVICE_APPLY_TO_LIGHT):
        hass.services.async_register(DOMAIN, SERVICE_APPLY_TO_LIGHT, _make_apply_handler(hass, entry, coordinator))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    per_entry_service = f"{SERVICE_APPLY_TO_LIGHT_PREFIX}{entry.entry_id}"
    hass.services.async_remove(DOMAIN, per_entry_service)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        # Remove panel when the last config entry is removed
        _meta_keys = {"static_path_registered", "panel_registered"}
        remaining_entries = [k for k in hass.data[DOMAIN] if k not in _meta_keys]
        if not remaining_entries and hass.data[DOMAIN].pop("panel_registered", False):
            try:
                frontend.async_remove_panel(hass, _PANEL_URL_PATH)
            except Exception:
                pass

    return unload_ok
