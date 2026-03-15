# Astronomically Guided CCT v1.6.9

Home Assistant custom integration that calculates a correlated colour temperature (CCT) curve
based on astronomical sun position — no external API required.

---

## Webapp

After installation, **CCT Astronomy** appears as a sidebar entry in Home Assistant.
The webapp shows the CCT curve for the day, phase timings, and configuration preview.

Direct URL: `http://<your-ha-host>/cct_astronomy/index.html`

> **Language:** The webapp UI is currently in German (DE).

---

## Installation (HACS)

1. In HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/mjmijh/cct-astronomy` (category: Integration)
3. Install **Astronomically Guided CCT**
4. Restart Home Assistant
5. Settings → Devices & Services → Add Integration → search **CCT**

---

## Configuration

| Parameter | Description |
|-----------|-------------|
| **Mode** | `kmax` — night uses K_max with twilight ramp; `kmin` — night uses K_min (no twilight) |
| **K_min / K_max** | CCT range in Kelvin |
| **Twilight angle** | Solar elevation for twilight threshold (e.g. 6° = civil twilight) |
| **Zone meridian** | Time zone reference meridian in degrees (e.g. 15 for CET/UTC+1) |
| **Default brightness** | Fallback brightness [%] |
| **Transition times** | Fade duration per phase: night / dawn / day / dusk [s] |

---

## Blueprints

Two ready-to-use automation blueprints are included:

- **`blueprint_cct_astronomy_lights_v1_1.yaml`** — applies CCT to lights on schedule
- **`blueprint_cct_astronomy_override_auto_resume_v1_2.yaml`** — pauses automation on manual override, resumes after a delay

---

## Entities

Each config entry creates:
- `sensor.<name>_cct` — current CCT value in Kelvin
- `sensor.<name>_phase` — current phase (night / dawn / day / dusk)
- `switch.<name>_enabled` — master automation switch

## Services

- `cct_astronomy.apply_to_light` — apply current CCT to one or more lights
