"""Recalcula em Python os balanços estáticos P25 a partir dos parâmetros centrais.

O modelo de curto-circuito é uma triagem trifásica em regime transitório, sem
componente CC, sem motores e sem coeficiente de tensão pré-falta. A reatância
fornecida é X'd (transitória), não X''d; portanto, o resultado não é a corrente
inicial de curto-circuito IEC 60909 nem um ajuste de proteção.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "25-usina-cogeracao-biomassa"
SQRT3 = math.sqrt(3.0)


def read_parameters(path: Path = PROJECT / "dados" / "parametros.csv") -> dict[str, float]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        params = {row["name"]: float(row["value"]) for row in rows}
    if not params:
        raise ValueError(f"CSV sem parâmetros: {path}")
    return params


def calculate(params: dict[str, float]) -> dict[str, dict[str, float]]:
    pg = params["generator_active_mw"]
    sgen = params["generator_rating_mva"]
    vgen = params["generator_voltage_kv"]
    fpgen = params["generator_power_factor"]
    paux = params["auxiliary_active_mw"]
    fpaux = params["auxiliary_power_factor"]
    pnet = pg - paux
    qgen = pg * math.tan(math.acos(fpgen))
    qaux = paux * math.tan(math.acos(fpaux))
    qnet_before_cap = qgen - qaux
    qnet = qnet_before_cap - params["capacitor_bank_mvar"]
    snet = math.hypot(pnet, qnet)
    qtarget = pnet * math.tan(math.acos(params["power_factor_target"]))
    qcap_required = max(0.0, qnet_before_cap - qtarget)

    sgen_operating = math.hypot(pg, qgen)
    i_gen_operating = sgen_operating * 1e6 / (SQRT3 * vgen * 1e3)
    i_gen_rated = sgen * 1e6 / (SQRT3 * vgen * 1e3)
    i_transformer_rated_hv = (
        params["main_transformer_mva"]
        * 1e6
        / (SQRT3 * params["grid_voltage_kv"] * 1e3)
    )
    i_poi = snet * 1e6 / (SQRT3 * params["grid_voltage_kv"] * 1e3)

    # Three-phase Thevenin equivalents. Transformer R/X and grid short-circuit
    # MVA are first combined on the transformer base, then converted to the
    # generator base for the 13.8 kV terminal calculation.
    st = params["main_transformer_mva"]
    sg = sgen
    z_grid_t = complex(0.0, st / params["grid_short_circuit_mva"])
    z_transformer_t = complex(
        params["main_transformer_r_pu"], params["main_transformer_x_pu"]
    )
    z_utility_at_generator = (z_grid_t + z_transformer_t) * st / sg
    i_utility_gen_pu = 1.0 / z_utility_at_generator
    xgen = params["generator_transient_reactance_pu"]
    i_machine_gen_pu = 1.0 / complex(0.0, xgen)
    i_total_gen_pu = i_utility_gen_pu + i_machine_gen_pu
    ibase_gen = sg * 1e6 / (SQRT3 * vgen * 1e3)
    i_utility_gen_a = abs(i_utility_gen_pu) * ibase_gen
    i_machine_gen_a = abs(i_machine_gen_pu) * ibase_gen
    i_total_gen_a = abs(i_total_gen_pu) * ibase_gen
    scc_gen_mva = abs(i_total_gen_pu) * sg

    # The 138 kV current uses a 40 MVA base. Grid and machine contributions
    # are phasors; grid resistance is omitted because no grid X/R was provided.
    z_grid_hv = complex(0.0, st / params["grid_short_circuit_mva"])
    z_machine_hv = complex(
        params["main_transformer_r_pu"],
        params["main_transformer_x_pu"] + xgen * sg / st,
    )
    i_grid_hv_pu = 1.0 / z_grid_hv
    i_machine_hv_pu = 1.0 / z_machine_hv
    i_total_hv_pu = i_grid_hv_pu + i_machine_hv_pu
    ibase_hv = st * 1e6 / (SQRT3 * params["grid_voltage_kv"] * 1e3)
    i_grid_hv_a = abs(i_grid_hv_pu) * ibase_hv
    i_machine_hv_a = abs(i_machine_hv_pu) * ibase_hv
    i_total_hv_a = abs(i_total_hv_pu) * ibase_hv

    fuel_mw = (
        params["biomass_flow_t_h"]
        * 1000.0
        * params["biomass_lhv_mj_kg"]
        / 3600.0
    )
    steam_mw = fuel_mw * params["boiler_efficiency"]
    hours = params["annual_operating_hours"]
    useful_efficiency = (pg + params["process_steam_thermal_mw"]) / fuel_mw

    balance = {
        "P_gerador_MW": pg,
        "P_mecanica_MW": pg / params["generator_efficiency"],
        "P_aux_MW": paux,
        "P_exportada_MW": pnet,
        "Q_gerador_MVAr": qgen,
        "Q_aux_MVAr": qaux,
        "Q_banco_MVAr": params["capacitor_bank_mvar"],
        "Q_exportada_MVAr": qnet,
        "S_exportada_MVA": snet,
        "fp_POI": pnet / snet,
        "Q_alvo_fp_MVAr": qtarget,
        "Q_compensacao_necessaria_MVAr": qcap_required,
        "S_gerador_operacao_MVA": sgen_operating,
        "I_operacao_gerador_A": i_gen_operating,
        "I_placa_gerador_A": i_gen_rated,
        "I_transformador_AT_A": i_transformer_rated_hv,
        "I_POI_A": i_poi,
        "carregamento_trafo_pu": snet / st,
    }
    short = {
        "Base_gerador_MVA": sg,
        "Base_transformador_MVA": st,
        "X_rede_na_base_trafo_pu": st / params["grid_short_circuit_mva"],
        "R_trafo_pu": params["main_transformer_r_pu"],
        "X_trafo_pu": params["main_transformer_x_pu"],
        "X_d_transitoria_pu": xgen,
        "I_rede_13k8_A": i_utility_gen_a,
        "I_gerador_13k8_A": i_machine_gen_a,
        "I_total_13k8_A": i_total_gen_a,
        "Scc_total_13k8_MVA": scc_gen_mva,
        "I_rede_138_A": i_grid_hv_a,
        "I_gerador_138_A": i_machine_hv_a,
        "I_total_138_A": i_total_hv_a,
    }
    energy = {
        "combustivel_MW": fuel_mw,
        "vapor_disponivel_MWth": steam_mw,
        "vapor_util_MWth": params["process_steam_thermal_mw"],
        "geracao_bruta_MW": pg,
        "exportacao_liquida_MW": pnet,
        "rendimento_util_pu": useful_efficiency,
        "energia_combustivel_MWh_ano": fuel_mw * hours,
        "energia_bruta_MWh_ano": pg * hours,
        "energia_liquida_MWh_ano": pnet * hours,
        "vapor_util_MWhth_ano": params["process_steam_thermal_mw"] * hours,
    }
    return {"balanco-potencia": balance, "curto-circuito": short, "balanco-energetico": energy}


def write_csv(path: Path, values: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(values))
        writer.writeheader()
        writer.writerow({key: f"{value:.10g}" for key, value in values.items()})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Raiz do repositório")
    args = parser.parse_args()
    project = args.root.resolve() / "25-usina-cogeracao-biomassa"
    results = calculate(read_parameters(project / "dados" / "parametros.csv"))
    for name, row in results.items():
        path = project / "resultados" / "tabelas" / f"{name}.csv"
        write_csv(path, row)
        print(f"Recalculado independentemente: {path.relative_to(args.root.resolve())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
