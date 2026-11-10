from __future__ import annotations

import json
from pathlib import Path

from simulacao_dinamica_python_p25 import SCENARIOS, operating_point, read_parameters, simulate_scenario


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resultados" / "relatorios"
SAG = next(scenario for scenario in SCENARIOS if scenario["name"] == "afundamento_tensao")


def _summary(rows: list[dict[str, float | str]], dt: float, duration: float) -> dict[str, float | int]:
    pe = [float(row["Pe_MW"]) for row in rows]
    angle = [float(row["angle_rad"]) for row in rows]
    current = [float(row["I_gerador_A"]) for row in rows]
    min_index = min(range(len(pe)), key=pe.__getitem__)
    max_index = max(range(len(pe)), key=pe.__getitem__)
    return {
        "dt_s": dt,
        "duration_s": duration,
        "samples": len(rows),
        "Pe_initial_MW": pe[0],
        "Pe_final_MW": pe[-1],
        "Pe_min_MW": pe[min_index],
        "time_Pe_min_s": float(rows[min_index]["time_s"]),
        "Pe_max_MW": pe[max_index],
        "time_Pe_max_s": float(rows[max_index]["time_s"]),
        "angle_min_rad": min(angle),
        "angle_max_rad": max(angle),
        "frequency_final_Hz": float(rows[-1]["frequency_Hz"]),
        "current_max_A": max(current),
        "negative_Pe_samples": sum(value < 0 for value in pe),
    }


def run_diagnostic() -> dict[str, object]:
    p = read_parameters()
    op = operating_point(p)
    dt_values = (0.005, 0.0025, 0.00125, 0.000625)
    short_runs = {
        dt: simulate_scenario(SAG, p, dt=dt, duration=5.0)
        for dt in dt_values
    }
    summaries_5s = [_summary(short_runs[dt], dt, 5.0) for dt in dt_values]
    convergence: list[dict[str, float]] = []
    for coarse_dt, fine_dt in zip(dt_values, dt_values[1:]):
        coarse = short_runs[coarse_dt]
        fine = short_runs[fine_dt]
        ratio = round(coarse_dt / fine_dt)
        max_error = max(
            abs(float(coarse[index]["Pe_MW"]) - float(fine[ratio * index]["Pe_MW"]))
            for index in range(len(coarse))
        )
        convergence.append({
            "coarse_dt_s": coarse_dt,
            "fine_dt_s": fine_dt,
            "max_common_time_Pe_difference_MW": max_error,
            "coarse_final_Pe_MW": float(coarse[-1]["Pe_MW"]),
            "fine_final_Pe_MW": float(fine[-1]["Pe_MW"]),
        })

    long_runs = [
        _summary(simulate_scenario(SAG, p, dt=dt, duration=duration), dt, duration)
        for duration in (20.0, 60.0)
        for dt in (0.0025, 0.00125)
    ]
    base = p["generator_rating_mva"]
    initial_swing_residual_pu = op["pm0_pu"] - op["pe0_pu"] - op["loss_pu"]
    evidence: dict[str, object] = {
        "status": "EXECUTADO_PYTHON_MODELO_AGREGADO; NAO E SIMULINK",
        "parameters_used": {
            "generator_rating_mva": base,
            "generator_active_mw": p["generator_active_mw"],
            "generator_efficiency": p["generator_efficiency"],
            "generator_transient_reactance_pu": p["generator_transient_reactance_pu"],
            "inertia_constant_s": p["inertia_constant_s"],
            "damping_pu": p["damping_pu"],
            "governor_droop_pu": p["governor_droop_pu"],
            "governor_time_constant_s": p["governor_time_constant_s"],
            "avr_gain": p["avr_gain"],
            "avr_time_constant_s": p["avr_time_constant_s"],
            "fault_voltage_pu": p["fault_voltage_pu"],
            "fault_duration_s": p["fault_duration_s"],
        },
        "initial_operating_point": {
            "Pm_pu": op["pm0_pu"],
            "Pe_pu": op["pe0_pu"],
            "Pe_MW": p["generator_active_mw"],
            "delta_rad": op["delta0_rad"],
            "loss_pu": op["loss_pu"],
            "swing_equation_residual_pu": initial_swing_residual_pu,
        },
        "signed_active_power_equation": "Pe_pu = Efd_pu * Vgrid_pu / Xd_transitoria_pu * sin(delta_rad)",
        "interpretation": (
            "Pe inicial positiva confirma exportacao no ponto nominal. O sinal negativo aparece quando a oscilacao "
            "leva delta abaixo de zero; no modelo reduzido isso representa reversao transitiva do fluxo ativo, "
            "nao evidencia de erro de convencao nem justificativa para inverter/clamp. A resposta de 5 s tem "
            "oscilacoes e picos acima da potencia nominal, portanto nao valida suportabilidade nem estabilidade. "
            "A sensibilidade a dt e reportada sem selecionar um passo para ocultar a limitacao."
        ),
        "five_second_step_sensitivity": summaries_5s,
        "adjacent_step_comparison": convergence,
        "long_horizon_step_sensitivity": long_runs,
        "model_limits": [
            "equivalente agregado maquina-rede, sem parametros validados de fabricante",
            "Xd_transitoria usada; sem Xd_subtransitoria, eixo d/q completo ou rede externa detalhada",
            "AVR e governador reduzidos, com limites e resposta parametrizados por hipoteses",
            "sem limitador de corrente do gerador, protecao, falta trifasica EMT ou cargas auxiliares dinamicas",
            "potencia ativa assinada e corrente calculada sao indicadores do modelo, nao limites de placa",
        ],
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT / "diagnostico-potencia-negativa-python.json"
    json_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Diagnóstico do resultado de potência ativa negativa — P25",
        "",
        "## Execução e ponto nominal",
        "",
        "Este arquivo foi gerado pelo modelo agregado RK4 em Python. Não é saída MATLAB/Simulink.",
        f"No ponto inicial, Pe = {p['generator_active_mw']:.3f} MW e o resíduo da equação de balanço do rotor é {initial_swing_residual_pu:.3e} pu.",
        "A potência usa `Pe = Efd·Vgrid/Xd'·sin(δ)`, com sinal definido pelo ângulo do rotor. Não foi aplicada inversão nem saturação artificial de Pe.",
        "",
        "## Sensibilidade do cenário de afundamento",
        "",
        "| dt (s) | Pe final em 5 s (MW) | Pe mínima (MW) | t da mínima (s) | Pe máxima (MW) | t da máxima (s) | I máxima (A) |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries_5s:
        lines.append(
            f"| {row['dt_s']:.6g} | {row['Pe_final_MW']:.3f} | {row['Pe_min_MW']:.3f} | "
            f"{row['time_Pe_min_s']:.4f} | {row['Pe_max_MW']:.3f} | {row['time_Pe_max_s']:.4f} | {row['current_max_A']:.1f} |"
        )
    lines.extend([
        "",
        "O cenário nominal inicial mantém exportação positiva. Após a falta sintética de 0,2 pu por 0,12 s, δ cruza zero durante a oscilação e Pe fica temporariamente negativo. Isso é reversão de potência ativa prevista pela equação assinada do modelo; os picos calculados também ultrapassam 25 MW e 32 MVA, mostrando que o equivalente não inclui limites de corrente/estabilidade utilizáveis para liberar equipamento.",
        "",
        "A comparação entre passos e horizontes está no JSON ao lado. A variação numérica não foi ocultada: a curva de 5 s permanece sensível ao passo devido a descontinuidades e limitadores do modelo reduzido. Em horizonte maior, a comparação serve apenas para conferir a tendência deste sistema matemático; não valida a usina real.",
        "",
        "## Conclusão técnica",
        "",
        "O valor negativo não deve ser corrigido invertendo o sinal ou cortando a curva. É um resultado transitório do modelo, enquanto a magnitude de pico e a sensibilidade numérica deixam a resposta inadequada para concluir estabilidade, suportabilidade à falta ou comportamento de uma unidade comercial. O modelo Simulink ainda precisa de execução real e revisão técnica independente.",
        "",
        "Reprodução: `python 25-usina-cogeracao-biomassa/validacao/diagnostico_potencia_negativa_p25.py`.",
    ])
    (OUTPUT / "diagnostico-potencia-negativa-python.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"JSON={json_path}")
    print(f"MD={OUTPUT / 'diagnostico-potencia-negativa-python.md'}")
    print(json.dumps(summaries_5s, ensure_ascii=False))
    print(json.dumps(convergence, ensure_ascii=False))
    print(json.dumps(long_runs, ensure_ascii=False))
    return evidence


if __name__ == "__main__":
    run_diagnostic()
