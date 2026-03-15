import math
import datetime
from dataclasses import dataclass

def deg2rad(d: float) -> float:
    return d * math.pi / 180.0

def day_of_year(date: datetime.date) -> int:
    return date.timetuple().tm_yday

def solar_declination_rad(N: int) -> float:
    return -23.44 * math.pi / 180.0 * math.cos((2.0 * math.pi / 365.0) * (N + 10))

def equation_of_time_minutes(N: int) -> float:
    B = deg2rad((360.0 / 365.0) * (N - 81))
    return 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

def hour_angle_deg(phi_rad: float, delta_rad: float, h_rad: float) -> float:
    cosH = (math.sin(h_rad) - math.sin(phi_rad) * math.sin(delta_rad)) / (
        math.cos(phi_rad) * math.cos(delta_rad)
    )
    cosH = max(-1.0, min(1.0, cosH))
    return math.degrees(math.acos(cosH))

@dataclass
class AstroTimes:
    t_ds: float
    t_sr: float
    t_ss: float
    t_de: float
    t_noon: float
    delta: float

def solar_times(
    date: datetime.date,
    lat_deg: float,
    lon_deg: float,
    zone_meridian_deg: float,
    dst_hours: float,
    twilight_abs_deg: float,
) -> AstroTimes:
    N = day_of_year(date)
    delta = solar_declination_rad(N)
    eot = equation_of_time_minutes(N)

    d_lambda = 4.0 * (zone_meridian_deg - lon_deg)  # Minuten
    t_noon = 12.0 + (d_lambda - eot) / 60.0 + dst_hours

    phi_rad = deg2rad(lat_deg)
    h_sr = deg2rad(-0.833)
    h_tw = deg2rad(-abs(twilight_abs_deg))

    H0_deg = hour_angle_deg(phi_rad, delta, h_sr)
    Htw_deg = hour_angle_deg(phi_rad, delta, h_tw)

    t_sr = t_noon - H0_deg / 15.0
    t_ss = t_noon + H0_deg / 15.0
    t_ds = t_noon - Htw_deg / 15.0
    t_de = t_noon + Htw_deg / 15.0

    return AstroTimes(t_ds=t_ds, t_sr=t_sr, t_ss=t_ss, t_de=t_de, t_noon=t_noon, delta=delta)

def cct_kmax(t: float, K_min: float, K_max: float, a: AstroTimes) -> float:
    Delta_m = a.t_sr - a.t_ds
    T_tag = a.t_ss - a.t_sr
    Delta_e = a.t_de - a.t_ss

    C_dm = (K_min + K_max) / 2.0
    A_dm = (K_max - K_min) / 2.0

    if t < a.t_ds:
        return K_max
    if t <= a.t_sr:
        u = (t - a.t_ds) / Delta_m
        return C_dm + A_dm * math.cos(math.pi * u)
    if t <= a.t_ss:
        u = (t - a.t_sr) / T_tag
        return K_min + (K_max - K_min) * (math.sin(math.pi * u) ** 2)
    if t < a.t_de:
        u = (t - a.t_ss) / Delta_e
        return C_dm + A_dm * math.cos(math.pi * (u - 1.0))
    return K_max

def cct_kmin_no_twilight(t: float, K_min: float, K_max: float, a: AstroTimes) -> float:
    if t <= a.t_sr or t >= a.t_ss:
        return K_min
    T_tag = a.t_ss - a.t_sr
    u = (t - a.t_sr) / T_tag
    return K_min + (K_max - K_min) * (math.sin(math.pi * u) ** 2)

def phase_of_day(t: float, a: AstroTimes) -> str:
    if t < a.t_ds:
        return "night"
    if t <= a.t_sr:
        return "dawn"
    if t <= a.t_ss:
        return "day"
    if t < a.t_de:
        return "dusk"
    return "night"
