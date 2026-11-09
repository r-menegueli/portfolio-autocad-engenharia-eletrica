from __future__ import annotations

import math

from calculos_independentes_p23 import calculate, read_parameters
from simulacao_dinamica_python_p23 import SCENARIOS, simulate_all


def _scenario(rows, name):
    return [row for row in rows if row["cenario"] == name]


def test_eight_scenarios_are_finite_and_include_all_required_signals() -> None:
    rows, summaries = simulate_all()
    assert len(SCENARIOS) == 8
    assert len(summaries) == 8
    assert len(rows) == 8 * 501
    required = {"V_barra_pu", "Q_STATCOM_MVAr", "Q_rede_MVAr", "fp_PCC", "I_barra_A", "I_PCC_A"}
    assert required <= set(rows[0])
    assert all(math.isfinite(float(row[key])) for row in rows for key in required)


def test_nominal_steady_state_matches_independent_static_balance() -> None:
    p = read_parameters()
    rows, _ = simulate_all(p)
    last = _scenario(rows, "nominal_com_STATCOM")[-1]
    static = calculate(p)["balanco-cargas"]
    assert math.isclose(float(last["Q_STATCOM_MVAr"]), static["Q_STATCOM_MVAr"], rel_tol=1e-6)
    assert math.isclose(float(last["P_MW"]), static["P_MW"], rel_tol=1e-12)
    assert abs(float(last["fp_PCC"]) - p["target_power_factor"]) < 1e-5


def test_furnace_off_absorbs_filter_excess_and_high_load_respects_statcom_limit() -> None:
    rows, _ = simulate_all()
    off = _scenario(rows, "forno_desligado_compensado")[-1]
    overload = _scenario(rows, "saturacao_STATCOM_mais_40pct")
    assert float(off["Q_STATCOM_MVAr"]) < 0
    assert max(abs(float(row["Q_STATCOM_MVAr"])) for row in overload) <= 12.5 + 1e-8
    assert max(abs(float(row["Q_STATCOM_MVAr"])) for row in overload) > 12.0


def test_voltage_sag_is_visible_and_recovers_after_event() -> None:
    rows, _ = simulate_all()
    nominal = _scenario(rows, "nominal_com_STATCOM")
    sag = _scenario(rows, "afundamento_rede_0p8pu")
    assert min(float(row["V_barra_pu"]) for row in sag) < min(float(row["V_barra_pu"]) for row in nominal) - 0.1
    assert abs(float(sag[-1]["V_barra_pu"]) - float(nominal[-1]["V_barra_pu"])) < 1e-4
