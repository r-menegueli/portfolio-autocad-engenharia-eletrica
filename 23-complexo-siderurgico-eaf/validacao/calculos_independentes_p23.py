from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = ROOT / "dados" / "parametros.csv"
OUTPUT = ROOT / "resultados" / "tabelas"


def read_parameters(path: Path = PARAMETERS) -> dict[str, float]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    return {row["name"]: float(row["value"]) for row in rows}


def calculate(p: dict[str, float]) -> dict[str, dict[str, float]]:
    furnace_s = p["furnace_transformer_mva"]
    furnace_pf = p["furnace_power_factor"]
    furnace_p = furnace_s * furnace_pf
    furnace_q = math.sqrt(furnace_s**2 - furnace_p**2)
    aux_p = p["auxiliary_active_mw"]
    aux_pf = p["auxiliary_power_factor"]
    aux_q = aux_p * math.tan(math.acos(aux_pf))
    p_total = furnace_p + aux_p
    q_raw = furnace_q + aux_q
    s_raw = math.hypot(p_total, q_raw)
    q_target = p_total * math.tan(math.acos(p["target_power_factor"]))
    q_filters = p["filter_total_mvar"]
    q_statcom = q_raw - q_filters - q_target
    s_pcc = math.hypot(p_total, q_target)
    i_pcc = s_pcc * 1e6 / (math.sqrt(3) * p["grid_voltage_kv"] * 1e3)
    i_bus = s_pcc * 1e6 / (math.sqrt(3) * p["bus_voltage_kv"] * 1e3)
    i_furnace = furnace_s * 1e6 / (math.sqrt(3) * p["furnace_secondary_voltage_kv"] * 1e3)

    base = p["main_transformer_mva"]
    x_source = base / p["source_short_circuit_mva"]
    x_total = p["main_transformer_x_pu"] + x_source
    r_total = p["main_transformer_r_pu"]  # utility-source resistance is unavailable and set to zero
    z_total = math.hypot(r_total, x_total)
    scc = base / z_total
    icc_ka = scc / (math.sqrt(3) * p["bus_voltage_kv"])

    harmonics = [p[f"harmonic_current_pu_{i}"] for i in range(1, 5)]
    thdi = math.sqrt(sum(value**2 for value in harmonics))

    return {
        "balanco-cargas": {
            "P_MW": p_total,
            "Q_bruta_MVAr": q_raw,
            "S_bruta_MVA": s_raw,
            "fp_bruto": p_total / s_raw,
            "Q_rede_alvo_MVAr": q_target,
            "Q_filtros_MVAr": q_filters,
            "Q_STATCOM_MVAr": q_statcom,
            "S_PCC_MVA": s_pcc,
            "I_PCC_A": i_pcc,
            "I_B1_A": i_bus,
            "I_secundaria_A": i_furnace,
        },
        "curto-circuito": {
            "Base_MVA": base,
            "X_fonte_pu": x_source,
            "R_total_pu": r_total,
            "X_total_pu": x_total,
            "Z_total_pu": z_total,
            "Scc_34k5_MVA": scc,
            "Icc_34k5_kA": icc_ka,
        },
        "harmonicos": {
            "THDi_sintetico_pu": thdi,
            "THDi_sintetico_percentual": 100 * thdi,
        },
    }


def write_results(results: dict[str, dict[str, float]], p: dict[str, float]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, row in results.items():
        path = OUTPUT / f"{filename}.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            if filename == "harmonicos":
                fields = ["ordem", "Ih_pu", "Ih_percentual_fundamental", "THDi_global_percentual"]
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                for i, order in enumerate(range(1, 5), start=1):
                    current = p[f"harmonic_current_pu_{i}"]
                    writer.writerow({
                        "ordem": p[f"harmonic_orders_{i}"],
                        "Ih_pu": current,
                        "Ih_percentual_fundamental": 100 * current,
                        "THDi_global_percentual": row["THDi_sintetico_percentual"],
                    })
            else:
                writer = csv.DictWriter(stream, fieldnames=list(row))
                writer.writeheader()
                writer.writerow(row)


if __name__ == "__main__":
    parameters = read_parameters()
    result = calculate(parameters)
    write_results(result, parameters)
    for name, row in result.items():
        print(f"{name}: {row}")
