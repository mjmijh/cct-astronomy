# CCT Astronomy

Home Assistant Custom Integration, die eine Farbtemperaturkurve (CCT) basierend auf der astronomischen Sonnenposition berechnet — ohne externe API oder Internetverbindung.

> Also available in [English](README.md) | También disponible en [Español](README.es.md)

---

## Funktionsweise

Die Integration berechnet den Sonnenstand aus dem HA-Standort und der aktuellen Uhrzeit. Anhand der Sonnenhöhe wird die aktuelle Phase bestimmt (Nacht / Dämmerung / Tag / Abenddämmerung) und ein stufenloser CCT-Wert zwischen den konfigurierten Kelvin-Grenzwerten interpoliert. Die gesamte Berechnung erfolgt lokal.

---

## Installation (HACS)

1. HACS → Integrations → ⋮ → Benutzerdefinierte Repositories
2. `https://github.com/mjmijh/cct-astronomy` hinzufügen — Kategorie: Integration
3. **Astronomically Guided CCT** installieren
4. Home Assistant neu starten
5. Einstellungen → Geräte & Dienste → Integration hinzufügen → **CCT** suchen

---

## Konfiguration

| Parameter | Beschreibung |
|-----------|-------------|
| **Modus** | `kmax` — Nacht nutzt K_max mit Dämmerungsrampe; `kmin` — Nacht nutzt K_min (einfacher, keine Rampe) |
| **K_min** | Wärmste Farbtemperatur in Kelvin (Nacht / Abenddämmerung) |
| **K_max** | Kühlste Farbtemperatur in Kelvin (Mittag) |
| **Dämmerungswinkel** | Sonnenhöhe, die die Dämmerungsgrenze markiert (z.B. `6` = zivile Dämmerung) |
| **Zonenmeridian** | Referenzmeridian der Zeitzone in Grad (z.B. `15` für MEZ/UTC+1) |
| **Standardhelligkeit** | Fallback-Helligkeit in Prozent |
| **Übergangszeiten** | Einblendzeit pro Phase — Nacht / Dämmerung / Tag / Abenddämmerung in Sekunden |

### Modi

**`kmax`** — empfohlen für zirkadiane Beleuchtung:
Nacht → K_max (warm), Morgendämmerung → Rampe zu K_min, Tag → K_min (kühl), Abenddämmerung → Rampe zurück zu K_max.

**`kmin`** — einfacher, ohne Dämmerungsrampe:
Nacht nutzt K_min; keine separate Dämmerungsphase.

---

## Entitäten

| Entität | Beschreibung |
|---------|-------------|
| `sensor.<name>_cct` | Aktueller CCT-Zielwert in Kelvin |
| `sensor.<name>_phase` | Aktuelle Phase: `night`, `dawn`, `day` oder `dusk` |
| `switch.<name>_enabled` | Hauptschalter — deaktiviert die Automation wenn ausgeschaltet |

---

## Dienste

| Dienst | Beschreibung |
|--------|-------------|
| `cct_astronomy.apply_to_light` | Aktuellen CCT-Wert auf eine oder mehrere Licht-Entitäten anwenden |

---

## Blueprints

Zwei Automations-Blueprints sind enthalten:

| Blueprint | Beschreibung |
|-----------|-------------|
| `blueprint_cct_astronomy_lights_v1_1.yaml` | Wendet CCT regelmäßig auf eine Leuchte an |
| `blueprint_cct_astronomy_override_auto_resume_v1_2.yaml` | Pausiert die Automation bei manuellem Eingriff; nimmt nach konfigurierbarer Verzögerung wieder auf |

---

## Webapp

Nach der Installation erscheint **CCT Astronomy** als Sidebar-Eintrag in Home Assistant. Die Webapp zeigt die CCT-Kurve des aktuellen Tages, Phasenzeitpunkte und eine Live-Konfigurationsvorschau.

Direkte URL: `http://<dein-ha-host>/cct_astronomy/index.html`

---

## Voraussetzungen

| Komponente | Mindestversion |
|------------|---------------|
| Home Assistant | 2024.1.0 |

---

## Links

- [Fehler & Feature-Anfragen](https://github.com/mjmijh/cct-astronomy/issues)
- [PICOlightnode Integration](https://github.com/mjmijh/picolightnode-ha)
- [Keyframe Scheduler Integration](https://github.com/mjmijh/keyframe-scheduler)
