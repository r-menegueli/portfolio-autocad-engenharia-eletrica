from __future__ import annotations

import math
import csv
from pathlib import Path

from calculos_independentes_p25 import calculate, read_parameters


def test_operating_apparent_power_and_currents_are_coherent() -> None:
    params = read_parameters()
    balance = calculate(params)["balanco-potencia"]
    assert balance["P_gerador_MW"] == params["generator_active_mw"]
    assert balance["S_gerador_operacao_MVA"] < params["generator_rating_mva"]
    assert balance["I_operacao_gerador_A"] < balance["I_placa_gerador_A"]
    assert balance["carregamento_trafo_pu"] < 1.0
    assert balance["fp_POI"] >= params["power_factor_target"]
    assert math.isclose(
        balance["I_POI_A"],
        balance["S_exportada_MVA"] * 1e6 / (math.sqrt(3) * params["grid_voltage_kv"] * 1e3),
        rel_tol=1e-12,
    )


def test_short_circuit_includes_converted_grid_and_machine_contributions() -> None:
    params = read_parameters()
    result = calculate(params)["curto-circuito"]
    st = params["main_transformer_mva"]
    sg = params["generator_rating_mva"]
    z_grid_t = complex(0, st / params["grid_short_circuit_mva"])
    z_trafo_t = complex(params["main_transformer_r_pu"], params["main_transformer_x_pu"])
    expected_grid = 1 / ((z_grid_t + z_trafo_t) * st / sg)
    expected_machine = 1 / complex(0, params["generator_transient_reactance_pu"])
    expected_total = expected_grid + expected_machine
    ibase = sg * 1e6 / (math.sqrt(3) * params["generator_voltage_kv"] * 1e3)
    assert result["Base_transformador_MVA"] == params["main_transformer_mva"]
    assert result["I_rede_13k8_A"] > 0
    assert result["I_gerador_13k8_A"] > 0
    assert result["I_total_13k8_A"] > max(result["I_rede_13k8_A"], result["I_gerador_13k8_A"])
    assert result["I_total_138_A"] > result["I_rede_138_A"]
    assert math.isclose(result["I_rede_13k8_A"], abs(expected_grid) * ibase, rel_tol=1e-12)
    assert math.isclose(result["I_gerador_13k8_A"], abs(expected_machine) * ibase, rel_tol=1e-12)
    assert math.isclose(result["I_total_13k8_A"], abs(expected_total) * ibase, rel_tol=1e-12)
    assert math.isclose(result["Scc_total_13k8_MVA"], abs(expected_total) * sg, rel_tol=1e-12)


def test_energy_balance_and_annual_energy_use_the_same_operating_hours() -> None:
    params = read_parameters()
    energy = calculate(params)["balanco-energetico"]
    assert math.isclose(
        energy["energia_liquida_MWh_ano"],
        energy["exportacao_liquida_MW"] * params["annual_operating_hours"],
        rel_tol=1e-12,
    )
    assert energy["vapor_disponivel_MWth"] >= energy["vapor_util_MWth"]
    assert 0 < energy["rendimento_util_pu"] < 1


def test_every_central_parameter_has_documented_origin_and_limit() -> None:
    params = read_parameters()
    source = Path(__file__).resolve().parents[1] / "dados" / "origem-parametros.csv"
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    names = [row["parametro"] for row in rows]
    assert len(names) == len(set(names))
    assert set(names) == set(params)
    assert all(row["classe_origem"].strip() and row["fonte_ou_justificativa"].strip() and row["limitacao"].strip() for row in rows)
