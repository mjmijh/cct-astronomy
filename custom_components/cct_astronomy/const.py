DOMAIN = "cct_astronomy"

CONF_MODE = "mode"  # "kmax" = night uses K_max with twilight ramp, "kmin" = night uses K_min without twilight
CONF_K_MIN = "k_min"
CONF_K_MAX = "k_max"
CONF_TWILIGHT_DEG = "twilight_deg"  # e.g., 6 for civil twilight
CONF_ZONE_MERIDIAN = "zone_meridian"  # e.g., 15 for CET (UTC+1)
CONF_ENABLED = "enabled"  # master switch per entry

DEFAULT_MODE = "kmax"
DEFAULT_K_MIN = 2700
DEFAULT_K_MAX = 5700
DEFAULT_TWILIGHT_DEG = 6.0
DEFAULT_ZONE_MERIDIAN = 15.0
DEFAULT_ENABLED = True

SERVICE_APPLY_TO_LIGHT = "apply_to_light"  # global fallback service
SERVICE_APPLY_TO_LIGHT_PREFIX = "apply_to_light_"  # per-entry service: SERVICE_APPLY_TO_LIGHT_PREFIX + entry_id

ATTR_LIGHT_ENTITY_ID = "light_entity_id"
ATTR_TRANSITION = "transition"

CONF_TRANS_NIGHT = "transition_night"
CONF_TRANS_DAWN = "transition_dawn"
CONF_TRANS_DAY = "transition_day"
CONF_TRANS_DUSK = "transition_dusk"

DEFAULT_TRANS_NIGHT = 180
DEFAULT_TRANS_DAWN = 120
DEFAULT_TRANS_DAY = 60
DEFAULT_TRANS_DUSK = 120

CONF_DIM_DEFAULT = "dim_default"
DEFAULT_DIM_DEFAULT = 100.0

CONF_NAME = "name"
DEFAULT_NAME = "CCT Area"
