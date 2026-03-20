# CCT Astronomy

Integración personalizada de Home Assistant que calcula una curva de temperatura de color correlacionada (CCT) basada en la posición astronómica del sol — sin API externa ni conexión a internet.

> Also available in [English](README.md) | Auch verfügbar auf [Deutsch](README.de.md)

---

## Cómo funciona

La integración calcula la elevación solar a partir de la ubicación de HA y la hora actual. En función de la elevación, determina la fase actual (noche / amanecer / día / atardecer) e interpola un valor CCT continuo entre los límites de Kelvin configurados. Todo el cálculo es local.

---

## Instalación (HACS)

1. HACS → Integraciones → ⋮ → Repositorios personalizados
2. Añadir `https://github.com/mjmijh/cct-astronomy` — categoría: Integración
3. Instalar **Astronomically Guided CCT**
4. Reiniciar Home Assistant
5. Configuración → Dispositivos y servicios → Añadir integración → buscar **CCT**

---

## Configuración

| Parámetro | Descripción |
|-----------|-------------|
| **Modo** | `kmax` — noche usa K_max con rampa crepuscular; `kmin` — noche usa K_min (más simple, sin rampa) |
| **K_min** | CCT más cálido en Kelvin (noche / atardecer) |
| **K_max** | CCT más frío en Kelvin (mediodía) |
| **Ángulo crepuscular** | Elevación solar que marca el límite del crepúsculo (p. ej. `6` = crepúsculo civil) |
| **Meridiano de zona** | Meridiano de referencia de la zona horaria en grados (p. ej. `15` para CET/UTC+1) |
| **Brillo predeterminado** | Brillo de respaldo en porcentaje |
| **Tiempos de transición** | Duración del fundido por fase — noche / amanecer / día / atardecer en segundos |

### Modos

**`kmax`** — recomendado para iluminación circadiana:
Noche → K_max (cálido), Amanecer → rampa a K_min, Día → K_min (frío), Atardecer → rampa de vuelta a K_max.

**`kmin`** — más simple, sin rampa crepuscular:
La noche usa K_min; no hay fase crepuscular separada.

---

## Entidades

| Entidad | Descripción |
|---------|-------------|
| `sensor.<nombre>_cct` | Valor CCT objetivo actual en Kelvin |
| `sensor.<nombre>_phase` | Fase actual: `night`, `dawn`, `day` o `dusk` |
| `switch.<nombre>_enabled` | Interruptor principal — desactiva la automatización cuando está apagado |

---

## Servicios

| Servicio | Descripción |
|----------|-------------|
| `cct_astronomy.apply_to_light` | Aplica el valor CCT actual a una o más entidades de luz |

---

## Blueprints

Se incluyen dos blueprints de automatización:

| Blueprint | Descripción |
|-----------|-------------|
| `blueprint_cct_astronomy_lights_v1_1.yaml` | Aplica el CCT a una luz de forma periódica |
| `blueprint_cct_astronomy_override_auto_resume_v1_2.yaml` | Pausa la automatización ante un control manual; reanuda tras un retardo configurable |

---

## Webapp

Tras la instalación, **CCT Astronomy** aparece como entrada en la barra lateral de Home Assistant. La webapp muestra la curva CCT del día actual, los tiempos de fase y una vista previa de configuración en vivo.

URL directa: `http://<tu-host-ha>/cct_astronomy/index.html`

---

## Requisitos

| Componente | Versión mínima |
|------------|---------------|
| Home Assistant | 2024.1.0 |

---

## Enlaces

- [Problemas y solicitudes de funciones](https://github.com/mjmijh/cct-astronomy/issues)
- [Integración PICOlightnode](https://github.com/mjmijh/picolightnode-ha)
- [Integración Keyframe Scheduler](https://github.com/mjmijh/keyframe-scheduler)
