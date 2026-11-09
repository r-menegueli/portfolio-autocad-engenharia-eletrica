"""Independent consistency checks for P24 result tables exported by MATLAB."""

from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


@pytest.fixture(scope="module")
def p():
    return {row["name"]: row["value"] for row in read_csv(PROJECT / "dados" / "parametros.csv")}


@pytest.fixture(scope="module")
def results():
    return {
        "electrical": read_csv(PROJECT / "resultados" / "tabelas" / "resultados-eletricos.csv"),
        "mechanical": read_csv(PROJECT / "resultados" / "tabelas" / "resultados-mecanicos.csv"),
        "thermal": read_csv(PROJECT / "resultados" / "tabelas" / "ampacidade-estimada.csv"),
        "structures": read_csv(PROJECT / "resultados" / "tabelas" / "tabela-estruturas.csv"),
    }


def f(p, key):
    return float(p[key])


def sag_state(p, temp_c, wind_m_s):
    span = f(p, "span_m")
    mass = f(p, "conductor_mass_kg_m")
    wv = mass * 9.80665
    d = f(p, "conductor_diameter_m")
    ww = 0.5 * f(p, "air_density_kg_m3") * f(p, "drag_coefficient") * d * wind_m_s**2
    we = math.hypot(wv, ww)
    ea = f(p, "conductor_ea_n")
    alpha = f(p, "conductor_alpha_per_c")
    h0 = f(p, "reference_horizontal_tension_n")
    f0 = wv * span**2 / (8 * h0)
    s0 = span + 8 * f0**2 / (3 * span)
    unstressed = s0 / (1 + h0 / ea) * (1 + alpha * (temp_c - f(p, "reference_temperature_c")))

    def arc_length(h):
        sag = we * span**2 / (8 * h)
        return (span + 8 * sag**2 / (3 * span)) / (1 + h / ea)

    lo, hi = 1000.0, 500000.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if arc_length(mid) > unstressed:
            lo = mid
        else:
            hi = mid
    h = (lo + hi) / 2
    sag_v = wv * span**2 / (8 * h)
    support_tension = math.hypot(h, we * span / 2)
    sag_h = ww * span**2 / (8 * h)
    sag_resultant = math.hypot(sag_v, sag_h)
    return sag_v, sag_h, sag_resultant, h, support_tension


def profile_elevation(p, station_m):
    route_km = [f(p, f"route_km_{i}") for i in range(1, 17)]
    route_z = [f(p, f"route_elevation_m_{i}") for i in range(1, 17)]
    km = station_m / 1000
    for i in range(len(route_km) - 1):
        if route_km[i] <= km <= route_km[i + 1]:
            u = (km - route_km[i]) / (route_km[i + 1] - route_km[i])
            return route_z[i] * (1 - u) + route_z[i + 1] * u
    raise AssertionError(f"Station outside synthetic route: {station_m} m")


def expected_clearance(p, start_m, sag):
    span = f(p, "span_m")
    t_route = []
    for i in range(1, 17):
        station = f(p, f"route_km_{i}") * 1000
        t = (station - start_m) / span
        if 0 < t < 1:
            t_route.append(t)
    samples = sorted({i / 50 for i in range(51)} | set(t_route))
    z0 = profile_elevation(p, start_m)
    z1 = profile_elevation(p, start_m + span)
    clearances = []
    for t in samples:
        ground = profile_elevation(p, start_m + span * t)
        attach = (z0 + f(p, "mean_conductor_height_m")) * (1 - t) + (z1 + f(p, "mean_conductor_height_m")) * t
        clearances.append(attach - sag * 4 * t * (1 - t) - ground)
    return min(clearances)


def test_electrical_table_covers_all_load_and_pf_pairs_and_matches_pi_model(p, results):
    rows = results["electrical"]
    assert len(rows) == 9
    assert {(float(r["P_MW"]), float(r["fp"])) for r in rows} == {
        (load, pf) for load in (50.0, 100.0, 140.0) for pf in (0.9, 0.95, 1.0)
    }

    spacings = [f(p, "phase_spacing_m_1"), f(p, "phase_spacing_m_2"), f(p, "phase_spacing_m_3")]
    d = [abs(spacings[1] - spacings[0]), abs(spacings[2] - spacings[1]), abs(spacings[2] - spacings[0])]
    gmd = math.prod(d) ** (1 / 3)
    bundle_n = int(f(p, "bundle_subconductors"))
    bundle_spacing = f(p, "bundle_spacing_m")
    gmr_bundle = math.sqrt(f(p, "conductor_gmr_m") * bundle_spacing)
    radius_bundle = math.sqrt(f(p, "conductor_diameter_m") / 2 * bundle_spacing)
    length_km = f(p, "length_km")
    length_m = length_km * 1000
    freq = f(p, "frequency_hz")
    vll = f(p, "voltage_kv") * 1000
    lpkm = 2e-4 * math.log(gmd / gmr_bundle)
    cpm = 2 * math.pi * 8.8541878128e-12 / math.log(gmd / radius_bundle)
    z = (f(p, "conductor_rac75_ohm_km") / bundle_n + 1j * 2 * math.pi * freq * lpkm) * length_km
    y = 1j * 2 * math.pi * freq * cpm * length_m
    a = 1 + y * z / 2
    b = z * (1 + y * z / 4)
    c = y * (1 + y * z / 4)
    dcoef = a
    vr = vll / math.sqrt(3)

    for row in rows:
        load = float(row["P_MW"])
        pf = float(row["fp"])
        q = load * math.tan(math.acos(pf))
        s_mva = math.hypot(load, q)
        ir = ((load + 1j * q) * 1e6 / (3 * vr)).conjugate()
        vs = a * vr + b * ir
        isend = c * vr + dcoef * ir
        expected = {
            "S_MVA": s_mva,
            "I_recebimento_A": abs(ir),
            "V_envio_LL_kV": math.sqrt(3) * abs(vs) / 1000,
            "regulacao_percentual": 100 * (math.sqrt(3) * abs(vs) / 1000 - vll / 1000) / (vll / 1000),
            "P_envio_MW": 3 * (vs * isend.conjugate()).real / 1e6,
        }
        for name, value in expected.items():
            assert float(row[name]) == pytest.approx(value, rel=2e-10, abs=1e-9)
        assert float(row["perdas_MW"]) == pytest.approx(float(row["P_envio_MW"]) - load, abs=1e-9)


def test_structures_close_30_km_and_anchors(p, results):
    rows = results["structures"]
    assert len(rows) == 101
    assert float(rows[0]["km"]) == 0
    assert float(rows[-1]["km"]) == pytest.approx(30)
    assert sum(float(r["vao_ate_proxima_estrutura_m"]) for r in rows) == pytest.approx(30000)
    assert float(rows[-1]["vao_ate_proxima_estrutura_m"]) == 0
    anchors = [float(r["km"]) for r in rows if r["tipo"] == "ancoragem"]
    assert anchors == pytest.approx([0, 9.9, 20.1, 30.0])
    assert float(p["span_m"]) * (len(rows) - 1) == pytest.approx(30000)


def test_mechanical_output_matches_sag_compatibility_and_clearance(p, results):
    rows = results["mechanical"]
    assert len(rows) == 900
    counts = Counter((float(r["temperatura_condutor_C"]), float(r["vento_m_s"])) for r in rows)
    assert len(counts) == 9 and set(counts.values()) == {100}
    expected_temps = {f(p, f"mechanical_conductor_temperatures_c_{i}") for i in range(1, 4)}
    expected_winds = {f(p, f"mechanical_wind_speeds_m_s_{i}") for i in range(1, 4)}
    assert {temp for temp, _ in counts} == expected_temps
    assert {wind for _, wind in counts} == expected_winds
    for (temp, wind), count in counts.items():
        sag, sag_h, sag_resultant, h, support = sag_state(p, temp, wind)
        group = [r for r in rows if float(r["temperatura_condutor_C"]) == temp and float(r["vento_m_s"]) == wind]
        for row in group:
            assert float(row["flecha_vertical_m"]) == pytest.approx(sag, abs=1e-8)
            assert float(row["flecha_transversal_m"]) == pytest.approx(sag_h, abs=1e-8)
            assert float(row["flecha_resultante_m"]) == pytest.approx(sag_resultant, abs=1e-8)
            assert float(row["tracao_horizontal_kN"]) == pytest.approx(h / 1000, abs=1e-8)
            assert float(row["tracao_no_apoio_kN"]) == pytest.approx(support / 1000, abs=1e-8)
            span_index = int(row["vao_inicial"])
            assert float(row["clearance_minimo_sintetico_m"]) == pytest.approx(
                expected_clearance(p, (span_index - 1) * f(p, "span_m"), sag), abs=1e-8
            )
            assert 0 < float(row["fracao_carga_ruptura"]) < 1


def test_thermal_output_matches_declared_simplified_heat_balance(p, results):
    rows = results["thermal"]
    assert len(rows) == 9
    assert len({float(r["ambiente_C"]) for r in rows}) == 3
    assert len({float(r["vento_m_s"]) for r in rows}) == 3
    currents = [float(r["I_recebimento_A"]) for r in results["electrical"]]
    imax = max(currents)
    d = f(p, "conductor_diameter_m")
    limit = f(p, "conductor_temperature_limit_c")
    resistance = f(p, "conductor_rac75_ohm_km") / 1000
    sigma = 5.670374419e-8
    for row in rows:
        ambient = float(row["ambiente_C"])
        wind = float(row["vento_m_s"])
        h = max(f(p, "thermal_natural_h_w_m2_c"), f(p, "thermal_h_w_m2_c") * math.sqrt(wind / f(p, "thermal_reference_wind_m_s")))
        solar = f(p, "solar_absorptivity") * f(p, "solar_flux_w_m2") * d
        convection = math.pi * d * h * (limit - ambient)
        radiation = math.pi * d * 0.5 * sigma * ((limit + 273.15) ** 4 - (ambient + 273.15) ** 4)
        per_sub = math.sqrt((convection + radiation - solar) / resistance)
        bundle = per_sub * f(p, "bundle_subconductors")
        margin = 100 * (bundle - imax) / bundle
        assert float(row["h_conveccao_assumido_W_m2K"]) == pytest.approx(h, rel=1e-10)
        assert float(row["ampacidade_por_subcondutor_A"]) == pytest.approx(per_sub, rel=2e-10)
        assert float(row["ampacidade_feixe_A"]) == pytest.approx(bundle, rel=2e-10)
        assert float(row["margem_percentual"]) == pytest.approx(margin, rel=2e-10)
        assert float(row["I_max_nove_casos_A"]) == pytest.approx(imax, rel=1e-10)
        assert row["status_triagem"] == ("EXCEEDS_SCREEN" if imax > bundle else "PASS_SCREEN")

