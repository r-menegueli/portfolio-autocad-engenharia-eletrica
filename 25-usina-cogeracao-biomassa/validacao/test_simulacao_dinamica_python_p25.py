from __future__ import annotations

import math

from simulacao_dinamica_python_p25 import SCENARIOS, read_parameters, simulate_all


def _scenario(rows, name):
    return [row for row in rows if row["cenario"] == name]


def test_eight_scenarios_are_finite_and_log_requested_machine_signals() -> None:
    rows, summaries = simulate_all()
    assert len(SCENARIOS) == len(summaries) == 8
    assert len(rows) == 8 * 1001
    required = {"Vt_pu", "frequency_Hz", "speed_deviation_pu", "Pe_MW", "Q_MVAr", "I_gerador_A"}
    assert required <= set(rows[0])
    assert all(math.isfinite(float(row[key])) for row in rows for key in required)


def test_nominal_model_remains_at_its_analytical_operating_point() -> None:
    p = read_parameters()
    rows, _ = simulate_all(p)
    nominal = _scenario(rows, "nominal")
    assert abs(float(nominal[-1]["frequency_Hz"]) - p["frequency_hz"]) < 1e-6
    assert abs(float(nominal[-1]["Vt_pu"]) - 1.0) < 1e-6
    assert abs(float(nominal[-1]["Pe_MW"]) - p["generator_active_mw"]) < 1e-5


def test_governor_tracks_power_reference_and_avr_changes_sag_response() -> None:
    rows, _ = simulate_all()
    governed = _scenario(rows, "referencia_potencia_mais_0p04pu")
    ungoverned = _scenario(rows, "referencia_mais_0p04pu_sem_governador")
    governed_after_step = [row for row in governed if float(row["time_s"]) >= 2.5]
    ungoverned_after_step = [row for row in ungoverned if float(row["time_s"]) >= 2.5]
    pm_initial = float(governed[0]["Pm_MW"])
    assert max(float(row["Pm_MW"]) for row in governed_after_step) > pm_initial + 1.0
    assert all(abs(float(row["Pm_MW"]) - float(ungoverned[0]["Pm_MW"])) < 1e-9 for row in ungoverned_after_step)
    assert max(abs(float(row["frequency_Hz"]) - 60) for row in governed_after_step) < 0.01
    avr = _scenario(rows, "afundamento_tensao")
    no_avr = _scenario(rows, "afundamento_sem_AVR")
    fault_start = int(1.0 / 0.005)
    fault_end = int((1.0 + read_parameters()["fault_duration_s"]) / 0.005)
    avr_response = min(abs(float(row["Vt_pu"]) - 1) for row in avr[fault_start:fault_end])
    no_avr_response = min(abs(float(row["Vt_pu"]) - 1) for row in no_avr[fault_start:fault_end])
    assert avr_response < no_avr_response


def test_frequency_and_current_metrics_are_saved_for_every_scenario() -> None:
    _, summaries = simulate_all()
    assert all(float(row["I_max_A"]) > 0 for row in summaries)
    assert all(float(row["f_min_Hz"]) <= float(row["f_final_Hz"]) <= float(row["f_max_Hz"]) for row in summaries)
