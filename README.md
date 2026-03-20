# CCT Astronomy

Home Assistant custom integration that calculates a correlated colour temperature (CCT) curve based on astronomical sun position — no external API or internet connection required.

> Auch verfügbar auf [Deutsch](README.de.md) | También disponible en [Español](README.es.md)

---

## How It Works

The integration derives the sun's elevation from your HA location and the current time. Based on the elevation it determines the current phase (night / dawn / day / dusk) and interpolates a smooth CCT value between your configured Kelvin limits. All calculation is local.

---

## Installation (HACS)

1. HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/mjmijh/cct-astronomy` — category: Integration
3. Install **Astronomically Guided CCT**
4. Restart Home Assistant
5. Settings → Devices & Services → Add Integration → search **CCT**

---

## Configuration

| Parameter | Description |
|-----------|-------------|
| **Mode** | `kmax` — night uses K_max with twilight ramp; `kmin` — night uses K_min (simpler, no ramp) |
| **K_min** | Warmest CCT in Kelvin (night / dusk) |
| **K_max** | Coolest CCT in Kelvin (midday) |
| **Twilight angle** | Solar elevation marking the twilight boundary (e.g. `6` = civil twilight) |
| **Zone meridian** | Reference meridian for your time zone in degrees (e.g. `15` for CET/UTC+1) |
| **Default brightness** | Fallback brightness in percent |
| **Transition times** | Fade duration per phase — night / dawn / day / dusk in seconds |

### Modes

**`kmax`** — recommended for circadian lighting:
Night → K_max (warm), Dawn → ramps to K_min, Day → K_min (cool), Dusk → ramps back to K_max.

**`kmin`** — simpler, no twilight ramp:
Night uses K_min; no separate twilight phase.

---

## Entities

| Entity | Description |
|--------|-------------|
| `sensor.<name>_cct` | Current CCT target in Kelvin |
| `sensor.<name>_phase` | Current phase: `night`, `dawn`, `day`, or `dusk` |
| `switch.<name>_enabled` | Master switch — disables automation when off |

---

## Services

| Service | Description |
|---------|-------------|
| `cct_astronomy.apply_to_light` | Apply the current CCT value to one or more light entities |

---

## Blueprints

Two automation blueprints are included:

| Blueprint | Description |
|-----------|-------------|
| `blueprint_cct_astronomy_lights_v1_1.yaml` | Applies CCT to a light on a regular schedule |
| `blueprint_cct_astronomy_override_auto_resume_v1_2.yaml` | Pauses automation on manual override; resumes after a configurable delay |

---

## Webapp

After installation, **CCT Astronomy** appears as a sidebar entry in Home Assistant. The webapp displays the CCT curve for the current day, phase timings, and a live configuration preview.

Direct URL: `http://<your-ha-host>/cct_astronomy/index.html`

---

## Requirements

| Component | Minimum version |
|-----------|----------------|
| Home Assistant | 2024.1.0 |

---

## Links

- [Issues & Feature Requests](https://github.com/mjmijh/cct-astronomy/issues)
- [PICOlightnode Integration](https://github.com/mjmijh/picolightnode-ha)
- [Keyframe Scheduler Integration](https://github.com/mjmijh/keyframe-scheduler)
