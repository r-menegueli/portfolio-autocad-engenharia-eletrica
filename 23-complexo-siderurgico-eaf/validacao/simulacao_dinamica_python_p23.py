from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

from calculos_independentes_p23 import calculate, read_parameters


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resultados" / "tabelas"
PLOT = ROOT / "resultados" / "graficos" / "resposta-cenarios-python.png"
DT = 0.01
DURATION = 5.0


SCENARIOS: tuple[dict[str, Any], ...] = (
    {"name": "forno_desligado_compensado", "statcom": True, "steps": ((0.0, 0.0),)},
    {"name": "nominal_sem_STATCOM", "statcom": False, "steps": ((0.0, 1.0),)},
    {"name": "nominal_com_STATCOM", "statcom": True, "steps": ((0.0, 1.0),)},
    {"name": "degrau_carga_mais_20pct", "statcom": True, "steps": ((0.0, 1.0), (1.0, 1.2))},
    {"name": "degrau_carga_menos_20pct", "statcom": True, "steps": ((0.0, 1.0), (1.0, 0.8))},
    {"name": "saturacao_STATCOM_mais_40pct", "statcom": True, "steps": ((0.0, 1.0), (1.0, 1.4))},
    {"name": "afundamento_rede_0p8pu", "statcom": True, "steps": ((0.0, 1.0),), "sag": (1.0, 1.15, 0.8)},
    {"name": "flutuacao_arco_sintetica", "statcom": True, "steps": ((0.0, 1.0),), "arc": True},
)


def _inputs(t: float, scenario: dict[str, Any], p: dict[str, float]) -> tuple[float, float, float, float]:
    scale = scenario["steps"][0][1]
    for at, value in scenario["steps"]:
        if t >= at:
            scale = value
    sf = p["furnace_transformer_mva"]
    pf = p["furnace_power_factor"]
    furnace_p = sf * pf * scale
    furnace_q = math.sqrt(sf**2 - (sf * pf) ** 2) * scale
    aux_p = p["auxiliary_active_mw"]
    aux_q = aux_p * math.tan(math.acos(p["auxiliary_power_factor"]))
    p_pu = (furnace_p + aux_p) / p["main_transformer_mva"]
    q_pu = (furnace_q + aux_q) / p["main_transformer_mva"]
    v_grid = 1.0
    if "sag" in scenario:
        t0, t1, v_sag = scenario["sag"]
        if t0 <= t < t1:
            v_grid = v_sag
    arc = 0.0
    if scenario.get("arc", False):
        arc = p["arc_fluctuation_pu"] * math.sin(2 * math.pi * 2 * t)
    return p_pu, q_pu, v_grid, arc


def _clamp(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, value))


def _derivative(t: float, x: list[float], scenario: dict[str, Any], p: dict[str, float]) -> list[float]:
    p_pu, q_pu, v_grid, arc = _inputs(t, scenario, p)
    base = p["main_transformer_mva"]
    q_filter = p["filter_total_mvar"] / base
    q_grid_ref = abs(p_pu) * math.tan(math.acos(p["target_power_factor"]))
    q_limit = p["statcom_limit_mvar"] / base
    q_reference = 0.0
    if scenario["statcom"]:
        q_reference = _clamp(q_pu - q_grid_ref - q_filter, -q_limit, q_limit)
    q_net = q_pu - q_filter - x[1]
    v_reference = v_grid - p["main_transformer_r_pu"] * p_pu
    v_reference -= (p["main_transformer_x_pu"] + base / p["source_short_circuit_mva"]) * q_net
    v_reference += arc
    return [
        (v_reference - x[0]) / p["bus_voltage_time_constant_s"],
        (q_reference - x[1]) / p["statcom_time_constant_s"],
    ]


def _add(x: list[float], dx: list[float], scale: float) -> list[float]:
    return [a + scale * b for a, b in zip(x, dx)]


def _signals(t: float, x: list[float], scenario: dict[str, Any], p: dict[str, float]) -> dict[str, float | str]:
    p_pu, q_pu, v_grid, arc = _inputs(t, scenario, p)
    q_filter_pu = p["filter_total_mvar"] / p["main_transformer_mva"]
    q_net_pu = q_pu - q_filter_pu - x[1]
    apparent_pu = math.hypot(p_pu, q_net_pu)
    pf = abs(p_pu) / apparent_pu if apparent_pu > 1e-12 else 1.0
    current_base_bus = p["main_transformer_mva"] * 1e6 / (math.sqrt(3) * p["bus_voltage_kv"] * 1e3)
    current_base_pcc = p["main_transformer_mva"] * 1e6 / (math.sqrt(3) * p["grid_voltage_kv"] * 1e3)
    return {
        "cenario": scenario["name"],
        "time_s": t,
        "P_MW": p_pu * p["main_transformer_mva"],
        "Q_bruta_MVAr": q_pu * p["main_transformer_mva"],
        "V_grid_pu": v_grid,
        "V_barra_pu": x[0],
        "Q_STATCOM_MVAr": x[1] * p["main_transformer_mva"],
        "Q_rede_MVAr": q_net_pu * p["main_transformer_mva"],
        "fp_PCC": pf,
        "I_barra_A": apparent_pu * current_base_bus / max(x[0], 0.1),
        "I_PCC_A": apparent_pu * current_base_pcc / max(x[0], 0.1),
        "arc_disturbance_pu": arc,
    }


def simulate_scenario(scenario: dict[str, Any], p: dict[str, float], dt: float = DT, duration: float = DURATION) -> list[dict[str, float | str]]:
    p0, q0, v0, _ = _inputs(0.0, scenario, p)
    qfilter = p["filter_total_mvar"] / p["main_transformer_mva"]
    qgrid_ref = abs(p0) * math.tan(math.acos(p["target_power_factor"]))
    q_limit = p["statcom_limit_mvar"] / p["main_transformer_mva"]
    q_statcom0 = _clamp(q0 - qgrid_ref - qfilter, -q_limit, q_limit) if scenario["statcom"] else 0.0
    q_net0 = q0 - qfilter - q_statcom0
    x_total = p["main_transformer_x_pu"] + p["main_transformer_mva"] / p["source_short_circuit_mva"]
    v0 = v0 - p["main_transformer_r_pu"] * p0 - x_total * q_net0
    state = [v0, q_statcom0]
    count = round(duration / dt)
    output: list[dict[str, float | str]] = []
    for index in range(count + 1):
        t = index * dt
        output.append(_signals(t, state, scenario, p))
        if index == count:
            break
        k1 = _derivative(t, state, scenario, p)
        k2 = _derivative(t + dt / 2, _add(state, k1, dt / 2), scenario, p)
        k3 = _derivative(t + dt / 2, _add(state, k2, dt / 2), scenario, p)
        k4 = _derivative(t + dt, _add(state, k3, dt), scenario, p)
        state = [
            state[j] + dt * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) / 6
            for j in range(len(state))
        ]
    return output


def simulate_all(p: dict[str, float] | None = None) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    params = p or read_parameters()
    rows: list[dict[str, float | str]] = []
    summaries: list[dict[str, float | str]] = []
    for scenario in SCENARIOS:
        result = simulate_scenario(scenario, params)
        rows.extend(result)
        voltage = [float(row["V_barra_pu"]) for row in result]
        statcom = [float(row["Q_STATCOM_MVAr"]) for row in result]
        current = [float(row["I_barra_A"]) for row in result]
        summaries.append({
            "cenario": scenario["name"],
            "V_min_pu": min(voltage),
            "V_max_pu": max(voltage),
            "V_final_pu": voltage[-1],
            "Q_STATCOM_min_MVAr": min(statcom),
            "Q_STATCOM_max_MVAr": max(statcom),
            "I_barra_max_A": max(current),
            "fp_final": float(result[-1]["fp_PCC"]),
        })
    return rows, summaries


def write_results(rows: list[dict[str, float | str]], summaries: list[dict[str, float | str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path, data in (
        (OUTPUT / "dinamica-cenarios-python.csv", rows),
        (OUTPUT / "resumo-cenarios-python.csv", summaries),
    ):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True, constrained_layout=True)
    for scenario in SCENARIOS:
        subset = [row for row in rows if row["cenario"] == scenario["name"]]
        t = [float(row["time_s"]) for row in subset]
        axes[0].plot(t, [float(row["V_barra_pu"]) for row in subset], label=scenario["name"])
        axes[1].plot(t, [float(row["Q_STATCOM_MVAr"]) for row in subset], label=scenario["name"])
        axes[2].plot(t, [float(row["I_barra_A"]) for row in subset], label=scenario["name"])
    axes[0].set_ylabel("Tensão da barra (pu)")
    axes[1].set_ylabel("Q STATCOM (MVAr)")
    axes[2].set_ylabel("Corrente na barra (A)")
    axes[2].set_xlabel("Tempo (s)")
    for axis in axes:
        axis.grid(True, alpha=0.3)
        axis.legend(fontsize=7, ncol=2, loc="best")
    fig.suptitle("P23 — simulação reduzida em Python; não é execução Simulink")
    PLOT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PLOT, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    params = read_parameters()
    rows, summaries = simulate_all(params)
    write_results(rows, summaries)
    print(f"P23: {len(SCENARIOS)} cenários, {len(rows)} amostras")
    print(f"Nominal independente: {calculate(params)['balanco-cargas']}")
