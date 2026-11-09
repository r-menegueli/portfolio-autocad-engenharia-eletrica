from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = ROOT / "dados" / "parametros.csv"
OUTPUT = ROOT / "resultados" / "tabelas"
PLOT = ROOT / "resultados" / "graficos" / "resposta-cenarios-python.png"
PLOT_SAG = ROOT / "resultados" / "graficos" / "resposta-afundamento-python.png"
DT = 0.005
DURATION = 5.0

SCENARIOS: tuple[dict[str, Any], ...] = (
    {"name": "nominal", "steps": ()},
    {"name": "referencia_potencia_mais_0p04pu", "steps": ((2.5, 0.04),)},
    {"name": "referencia_potencia_menos_0p04pu", "steps": ((2.5, -0.04),)},
    {"name": "afundamento_tensao", "steps": (), "sag": True},
    {"name": "afundamento_mais_referencia", "steps": ((2.5, 0.04),), "sag": True},
    {"name": "afundamento_sem_AVR", "steps": (), "sag": True, "avr": False},
    {"name": "referencia_mais_0p04pu_sem_governador", "steps": ((2.5, 0.04),), "governor": False},
    {"name": "sensibilidade_inercia_metade", "steps": ((2.5, 0.04),), "inertia_scale": 0.5},
)


def read_parameters(path: Path = PARAMETERS) -> dict[str, float]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return {row["name"]: float(row["value"]) for row in csv.DictReader(stream)}


def operating_point(p: dict[str, float]) -> dict[str, float]:
    base = p["generator_rating_mva"]
    pm0 = p["generator_active_mw"] / p["generator_efficiency"] / base
    pe0 = p["generator_active_mw"] / base
    q0 = p["generator_active_mw"] * math.tan(math.acos(p["generator_power_factor"])) / base
    x = p["generator_transient_reactance_pu"]
    e0 = math.hypot(x * pe0, 1 + x * q0)
    delta0 = math.atan2(x * pe0, 1 + x * q0)
    return {
        "pm0_pu": pm0,
        "pe0_pu": pe0,
        "q0_pu": q0,
        "efd0_deviation_pu": e0 - 1,
        "delta0_rad": delta0,
        "loss_pu": pm0 - pe0,
    }


def _inputs(t: float, scenario: dict[str, Any], p: dict[str, float], op: dict[str, float]) -> tuple[float, float, float]:
    pref = op["pm0_pu"]
    for at, delta in scenario["steps"]:
        if t >= at:
            pref += delta
    v_grid = 1.0
    if scenario.get("sag", False):
        t0 = 1.0
        t1 = t0 + p["fault_duration_s"]
        if t0 <= t < t1:
            v_grid = p["fault_voltage_pu"]
    return pref, v_grid, 1.0


def _derivative(t: float, x: list[float], scenario: dict[str, Any], p: dict[str, float], op: dict[str, float]) -> list[float]:
    pref, v_grid, v_ref = _inputs(t, scenario, p, op)
    delta, speed, pm, efd_dev = x
    reactance = p["generator_transient_reactance_pu"]
    efd = min(1.25, max(0.7, 1 + efd_dev))
    pe = efd * v_grid / reactance * math.sin(delta)
    vt = v_grid + 0.02 * (efd_dev - op["efd0_deviation_pu"])
    q = (efd * v_grid * math.cos(delta) - v_grid * v_grid) / reactance

    efd_rate = 0.0
    if scenario.get("avr", True):
        efd_rate = (
            op["efd0_deviation_pu"]
            + p["avr_gain"] * (v_ref - vt)
            - efd_dev
        ) / p["avr_time_constant_s"]
        if efd_dev >= 0.25 and efd_rate > 0:
            efd_rate = 0.0
        elif efd_dev <= -0.3 and efd_rate < 0:
            efd_rate = 0.0

    governor_rate = 0.0
    if scenario.get("governor", True):
        governor_rate = (pref - pm - speed / p["governor_droop_pu"]) / p["governor_time_constant_s"]
    inertia = p["inertia_constant_s"] * scenario.get("inertia_scale", 1.0)
    speed_rate = (pm - pe - op["loss_pu"] - p["damping_pu"] * speed) / (2 * inertia)
    return [
        2 * math.pi * p["frequency_hz"] * speed,
        speed_rate,
        governor_rate,
        efd_rate,
    ]


def _add(x: list[float], dx: list[float], scale: float) -> list[float]:
    return [a + scale * b for a, b in zip(x, dx)]


def _signals(t: float, x: list[float], scenario: dict[str, Any], p: dict[str, float], op: dict[str, float]) -> dict[str, float | str]:
    pref, v_grid, v_ref = _inputs(t, scenario, p, op)
    delta, speed, pm, efd_dev = x
    reactance = p["generator_transient_reactance_pu"]
    efd = min(1.25, max(0.7, 1 + efd_dev))
    pe = efd * v_grid / reactance * math.sin(delta)
    vt = v_grid + 0.02 * (efd_dev - op["efd0_deviation_pu"])
    q = (efd * v_grid * math.cos(delta) - v_grid * v_grid) / reactance
    apparent_pu = math.hypot(pe, q) / max(vt, 0.1)
    current_base_a = p["generator_rating_mva"] * 1e6 / (math.sqrt(3) * p["generator_voltage_kv"] * 1e3)
    return {
        "cenario": scenario["name"],
        "time_s": t,
        "angle_rad": delta,
        "speed_deviation_pu": speed,
        "frequency_Hz": p["frequency_hz"] * (1 + speed),
        "Pm_MW": pm * p["generator_rating_mva"],
        "Pe_MW": pe * p["generator_rating_mva"],
        "Q_MVAr": q * p["generator_rating_mva"],
        "Efd_pu": efd,
        "Vt_pu": vt,
        "I_gerador_A": apparent_pu * current_base_a,
        "P_ref_pu": pref,
    }


def simulate_scenario(scenario: dict[str, Any], p: dict[str, float], dt: float = DT, duration: float = DURATION) -> list[dict[str, float | str]]:
    op = operating_point(p)
    state = [op["delta0_rad"], 0.0, op["pm0_pu"], op["efd0_deviation_pu"]]
    steps = round(duration / dt)
    rows: list[dict[str, float | str]] = []
    for index in range(steps + 1):
        t = index * dt
        rows.append(_signals(t, state, scenario, p, op))
        if index == steps:
            break
        k1 = _derivative(t, state, scenario, p, op)
        k2 = _derivative(t + dt / 2, _add(state, k1, dt / 2), scenario, p, op)
        k3 = _derivative(t + dt / 2, _add(state, k2, dt / 2), scenario, p, op)
        k4 = _derivative(t + dt, _add(state, k3, dt), scenario, p, op)
        state = [
            state[j] + dt * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]) / 6
            for j in range(len(state))
        ]
    return rows


def simulate_all(p: dict[str, float] | None = None) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    params = p or read_parameters()
    rows: list[dict[str, float | str]] = []
    summaries: list[dict[str, float | str]] = []
    for scenario in SCENARIOS:
        result = simulate_scenario(scenario, params)
        rows.extend(result)
        voltage = [float(row["Vt_pu"]) for row in result]
        frequency = [float(row["frequency_Hz"]) for row in result]
        current = [float(row["I_gerador_A"]) for row in result]
        summaries.append({
            "cenario": scenario["name"],
            "Vt_min_pu": min(voltage),
            "Vt_max_pu": max(voltage),
            "Vt_final_pu": voltage[-1],
            "f_min_Hz": min(frequency),
            "f_max_Hz": max(frequency),
            "f_final_Hz": frequency[-1],
            "I_max_A": max(current),
            "Pe_final_MW": float(result[-1]["Pe_MW"]),
            "Q_final_MVAr": float(result[-1]["Q_MVAr"]),
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
    labels = {
        "Vt_pu": "Tensão terminal (pu)",
        "frequency_Hz": "Desvio de frequência, Δf (Hz)",
        "Pe_MW": "Potência ativa Pe (MW)",
        "Q_MVAr": "Potência reativa Q (MVAr)",
        "I_gerador_A": "Corrente do gerador (A)",
    }
    plot_groups = (
        (PLOT, [scenario for scenario in SCENARIOS if not scenario.get("sag", False)],
         "P25 — degrau de referência de potência; modelo reduzido em Python, não é Simulink",
         ("frequency_Hz", "Pe_MW", "Q_MVAr", "I_gerador_A")),
        (PLOT_SAG, [scenario for scenario in SCENARIOS if scenario.get("sag", False)],
         "P25 — diagnóstico de afundamento; não se recompõe em 5 s; sem rede, limitador ou proteção",
         ("Vt_pu", "frequency_Hz", "Pe_MW", "I_gerador_A")),
    )
    nominal_frequency = read_parameters()["frequency_hz"]
    for plot_path, scenarios, title, signals in plot_groups:
        fig, axes = plt.subplots(4, 1, figsize=(10, 11), sharex=True, constrained_layout=True)
        for scenario in scenarios:
            subset = [row for row in rows if row["cenario"] == scenario["name"]]
            t = [float(row["time_s"]) for row in subset]
            for axis, signal in zip(axes, signals):
                values = [float(row[signal]) for row in subset]
                if signal == "frequency_Hz":
                    values = [value - nominal_frequency for value in values]
                axis.plot(t, values, label=scenario["name"])
        for axis, signal in zip(axes, signals):
            axis.set_ylabel(labels[signal])
            axis.grid(True, alpha=0.3)
            axis.legend(fontsize=7, ncol=2, loc="best")
        axes[-1].set_xlabel("Tempo (s)")
        fig.suptitle(title)
        plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(plot_path, dpi=180)
        plt.close(fig)


if __name__ == "__main__":
    params = read_parameters()
    rows, summaries = simulate_all(params)
    write_results(rows, summaries)
    print(f"P25: {len(SCENARIOS)} cenários, {len(rows)} amostras")
    for result in summaries:
        print(result)
