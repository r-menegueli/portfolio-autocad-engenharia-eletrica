from __future__ import annotations

import csv
import math
from pathlib import Path

from calculos_independentes_p23 import calculate, read_parameters


ROOT = Path(__file__).resolve().parents[1]


def test_power_balance_and_compensation_are_consistent() -> None:
    p = read_parameters()
    result = calculate(p)["balanco-cargas"]
    assert math.isclose(result["P_MW"], 28.0, rel_tol=1e-12)
    assert math.isclose(result["Q_STATCOM_MVAr"] + result["Q_filtros_MVAr"] + result["Q_rede_alvo_MVAr"], result["Q_bruta_MVAr"], rel_tol=1e-12)
    assert 0 <= result["Q_STATCOM_MVAr"] <= p["statcom_limit_mvar"]
    assert math.isclose(result["I_PCC_A"], result["S_PCC_MVA"] * 1e6 / (math.sqrt(3) * p["grid_voltage_kv"] * 1e3), rel_tol=1e-12)


def test_short_circuit_uses_full_transformer_impedance_magnitude() -> None:
    p = read_parameters()
    result = calculate(p)["curto-circuito"]
    z = math.hypot(p["main_transformer_r_pu"], p["main_transformer_x_pu"] + p["main_transformer_mva"] / p["source_short_circuit_mva"])
    expected_mva = p["main_transformer_mva"] / z
    expected_ka = expected_mva / (math.sqrt(3) * p["bus_voltage_kv"])
    assert math.isclose(result["Scc_34k5_MVA"], expected_mva, rel_tol=1e-12)
    assert math.isclose(result["Icc_34k5_kA"], expected_ka, rel_tol=1e-12)
    assert result["Icc_34k5_kA"] < p["main_transformer_mva"] / result["X_total_pu"] / (math.sqrt(3) * p["bus_voltage_kv"])


def test_harmonic_rss_is_explicitly_synthetic_and_source_table_is_complete() -> None:
    p = read_parameters()
    result = calculate(p)["harmonicos"]
    expected = math.sqrt(sum(p[f"harmonic_current_pu_{i}"] ** 2 for i in range(1, 5)))
    assert math.isclose(result["THDi_sintetico_pu"], expected, rel_tol=1e-12)
    source = ROOT / "dados" / "origem-parametros.csv"
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert {row["parametro"] for row in rows} == set(p)
    assert all(row["classe_origem"] and row["fonte_ou_justificativa"] and row["limitacao"] for row in rows)
