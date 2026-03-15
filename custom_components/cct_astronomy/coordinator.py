from __future__ import annotations

import datetime
import logging
from dataclasses import asdict

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .astro_cct import solar_times, cct_kmax, cct_kmin_no_twilight, phase_of_day
from .const import (
    DOMAIN,
    CONF_MODE, CONF_K_MIN, CONF_K_MAX, CONF_TWILIGHT_DEG, CONF_ZONE_MERIDIAN, CONF_ENABLED,
    CONF_TRANS_NIGHT, CONF_TRANS_DAWN, CONF_TRANS_DAY, CONF_TRANS_DUSK,
    CONF_DIM_DEFAULT,
    DEFAULT_MODE, DEFAULT_K_MIN, DEFAULT_K_MAX, DEFAULT_TWILIGHT_DEG, DEFAULT_ZONE_MERIDIAN, DEFAULT_ENABLED,
    DEFAULT_TRANS_NIGHT, DEFAULT_TRANS_DAWN, DEFAULT_TRANS_DAY, DEFAULT_TRANS_DUSK,
    DEFAULT_DIM_DEFAULT,
    SERVICE_APPLY_TO_LIGHT_PREFIX,
)

_LOGGER = logging.getLogger(__name__)


def kelvin_to_mired(k: float) -> int:
    if k <= 0:
        return 0
    return int(round(1000000.0 / k))

class CctCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=datetime.timedelta(minutes=1),
        )
        self.entry = entry

    def is_enabled(self) -> bool:
        return bool(self.entry.options.get(CONF_ENABLED, self.entry.data.get(CONF_ENABLED, DEFAULT_ENABLED)))

    def transition_defaults(self) -> dict:
        return {
            "night": float(self.entry.options.get(CONF_TRANS_NIGHT, self.entry.data.get(CONF_TRANS_NIGHT, DEFAULT_TRANS_NIGHT))),
            "dawn": float(self.entry.options.get(CONF_TRANS_DAWN, self.entry.data.get(CONF_TRANS_DAWN, DEFAULT_TRANS_DAWN))),
            "day": float(self.entry.options.get(CONF_TRANS_DAY, self.entry.data.get(CONF_TRANS_DAY, DEFAULT_TRANS_DAY))),
            "dusk": float(self.entry.options.get(CONF_TRANS_DUSK, self.entry.data.get(CONF_TRANS_DUSK, DEFAULT_TRANS_DUSK))),
        }

    async def _async_update_data(self) -> dict:
        try:
            now = dt_util.now()
            date = now.date()

            lat = float(self.hass.config.latitude)
            lon = float(self.hass.config.longitude)

            mode = self.entry.options.get(CONF_MODE, self.entry.data.get(CONF_MODE, DEFAULT_MODE))
            k_min = float(self.entry.options.get(CONF_K_MIN, self.entry.data.get(CONF_K_MIN, DEFAULT_K_MIN)))
            k_max = float(self.entry.options.get(CONF_K_MAX, self.entry.data.get(CONF_K_MAX, DEFAULT_K_MAX)))
            twilight = float(self.entry.options.get(CONF_TWILIGHT_DEG, self.entry.data.get(CONF_TWILIGHT_DEG, DEFAULT_TWILIGHT_DEG)))
            zone_meridian = float(self.entry.options.get(CONF_ZONE_MERIDIAN, self.entry.data.get(CONF_ZONE_MERIDIAN, DEFAULT_ZONE_MERIDIAN)))
            enabled = bool(self.entry.options.get(CONF_ENABLED, self.entry.data.get(CONF_ENABLED, DEFAULT_ENABLED)))

            trans = self.transition_defaults()

            dim_default = float(self.entry.options.get(CONF_DIM_DEFAULT, self.entry.data.get(CONF_DIM_DEFAULT, DEFAULT_DIM_DEFAULT)))

            dst_td = now.dst() or datetime.timedelta(0)
            dst_hours = dst_td.total_seconds() / 3600.0

            a = solar_times(
                date=date,
                lat_deg=lat,
                lon_deg=lon,
                zone_meridian_deg=zone_meridian,
                dst_hours=dst_hours,
                twilight_abs_deg=twilight,
            )

            t = now.hour + now.minute / 60.0 + now.second / 3600.0

            if mode == "kmin":
                cct = cct_kmin_no_twilight(t, k_min, k_max, a)
            else:
                cct = cct_kmax(t, k_min, k_max, a)

            service_name = f"{DOMAIN}.{SERVICE_APPLY_TO_LIGHT_PREFIX}{self.entry.entry_id}"

            return {
                "cct_kelvin": float(cct),
                "cct_mired": kelvin_to_mired(float(cct)),
                "dim": float(dim_default),
                "phase": phase_of_day(t, a),
                "fade_seconds": float(trans.get(phase_of_day(t, a), 60.0)),
                "enabled": enabled,
                "apply_service": service_name,
                "transition_defaults": trans,
                "astro": asdict(a),
                "params": {
                    "mode": mode,
                    "k_min": k_min,
                    "k_max": k_max,
                    "twilight_deg": twilight,
                    "zone_meridian": zone_meridian,
                    "lat": lat,
                    "lon": lon,
                    "dst_hours": dst_hours,
                    "enabled": enabled,
                    "dim_default": dim_default,
                    "apply_service": service_name,
                    **{f"transition_{k}": v for k, v in trans.items()},
                },
            }
        except Exception as e:
            raise UpdateFailed(str(e)) from e
