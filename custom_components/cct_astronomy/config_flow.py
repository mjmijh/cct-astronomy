from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_NAME,
    DEFAULT_NAME,
    CONF_MODE,
    CONF_K_MIN,
    CONF_K_MAX,
    CONF_TWILIGHT_DEG,
    CONF_ZONE_MERIDIAN,
    CONF_ENABLED,
    CONF_TRANS_NIGHT,
    CONF_TRANS_DAWN,
    CONF_TRANS_DAY,
    CONF_TRANS_DUSK,
    CONF_DIM_DEFAULT,
    DEFAULT_MODE,
    DEFAULT_K_MIN,
    DEFAULT_K_MAX,
    DEFAULT_TWILIGHT_DEG,
    DEFAULT_ZONE_MERIDIAN,
    DEFAULT_ENABLED,
    DEFAULT_TRANS_NIGHT,
    DEFAULT_TRANS_DAWN,
    DEFAULT_TRANS_DAY,
    DEFAULT_TRANS_DUSK,
    DEFAULT_DIM_DEFAULT,
)

_LOGGER = logging.getLogger(__name__)


def _options_schema(values: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_ENABLED, default=values.get(CONF_ENABLED, DEFAULT_ENABLED)): bool,
            vol.Optional(CONF_MODE, default=values.get(CONF_MODE, DEFAULT_MODE)): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "kmax", "label": "kmax — night: K_max (with twilight ramp)"},
                        {"value": "kmin", "label": "kmin — night: K_min (no twilight)"},
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(CONF_K_MIN, default=values.get(CONF_K_MIN, DEFAULT_K_MIN)): vol.Coerce(float),
            vol.Optional(CONF_K_MAX, default=values.get(CONF_K_MAX, DEFAULT_K_MAX)): vol.Coerce(float),
            vol.Optional(CONF_TWILIGHT_DEG, default=values.get(CONF_TWILIGHT_DEG, DEFAULT_TWILIGHT_DEG)): vol.Coerce(float),
            vol.Optional(CONF_ZONE_MERIDIAN, default=values.get(CONF_ZONE_MERIDIAN, DEFAULT_ZONE_MERIDIAN)): vol.Coerce(float),
            vol.Optional(CONF_DIM_DEFAULT, default=values.get(CONF_DIM_DEFAULT, DEFAULT_DIM_DEFAULT)): vol.Coerce(float),
            vol.Optional(CONF_TRANS_NIGHT, default=values.get(CONF_TRANS_NIGHT, DEFAULT_TRANS_NIGHT)): vol.Coerce(float),
            vol.Optional(CONF_TRANS_DAWN, default=values.get(CONF_TRANS_DAWN, DEFAULT_TRANS_DAWN)): vol.Coerce(float),
            vol.Optional(CONF_TRANS_DAY, default=values.get(CONF_TRANS_DAY, DEFAULT_TRANS_DAY)): vol.Coerce(float),
            vol.Optional(CONF_TRANS_DUSK, default=values.get(CONF_TRANS_DUSK, DEFAULT_TRANS_DUSK)): vol.Coerce(float),
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            base = _options_schema({}).schema
            schema = vol.Schema(
                {
                    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                    **base,
                }
            )
            return self.async_show_form(step_id="user", data_schema=schema)

        title = str(user_input.get(CONF_NAME) or DEFAULT_NAME).strip() or DEFAULT_NAME
        data = dict(user_input)
        data.pop(CONF_NAME, None)
        return self.async_create_entry(title=title, data=data)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is None:
            merged = dict(self._entry.data)
            merged.update(dict(self._entry.options))
            return self.async_show_form(
                step_id="init",
                data_schema=_options_schema(merged),
            )

        return self.async_create_entry(title="", data=user_input)
