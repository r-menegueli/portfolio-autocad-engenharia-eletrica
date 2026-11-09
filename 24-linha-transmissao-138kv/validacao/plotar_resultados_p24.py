"""Rebuild readable P24 result charts from the central parameters and MATLAB CSVs.

This lightweight renderer is the fallback for hosts where MATLAB figure export
exceeds available memory. It does not replace run_analysis.m calculations.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "resultados" / "graficos"
TABLES = PROJECT / "resultados" / "tabelas"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def get_params():
    rows = read_csv(PROJECT / "dados" / "parametros.csv")
    return {row["name"]: row["value"] for row in rows}


def f(p, key):
    return float(p[key])


def sag_state(p, span, temp_c, wind):
    g = 9.80665
    wv = f(p, "conductor_mass_kg_m") * g
    wind_load = 0.5 * f(p, "air_density_kg_m3") * f(p, "drag_coefficient") * f(p, "conductor_diameter_m") * wind**2
    we = math.hypot(wv, wind_load)
    ea = f(p, "conductor_ea_n")
    alpha = f(p, "conductor_alpha_per_c")
    h0 = f(p, "reference_horizontal_tension_n")
    t0 = f(p, "reference_temperature_c")
    f0 = wv * span**2 / (8 * h0)
    arc0 = span + 8 * f0**2 / (3 * span)
    target = arc0 / (1 + h0 / ea) * (1 + alpha * (temp_c - t0))

    def residual(h):
        sag_r = we * span**2 / (8 * h)
        return (span + 8 * sag_r**2 / (3 * span)) / (1 + h / ea) - target

    lo, hi = 1000.0, 500000.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    h = (lo + hi) / 2
    sag_v = wv * span**2 / (8 * h)
    support = math.hypot(h, we * span / 2)
    sag_h = wind_load * span**2 / (8 * h)
    sag_resultant = math.hypot(sag_v, sag_h)
    return sag_v, sag_h, sag_resultant, h, support


def profile_elevation(p, station_m):
    route_km = [f(p, f"route_km_{i}") for i in range(1, 17)]
    route_z = [f(p, f"route_elevation_m_{i}") for i in range(1, 17)]
    return float(np.interp(station_m / 1000, route_km, route_z))


def rebuild_mechanical_table(p):
    """Rebuild the MATLAB-equivalent mechanical matrix in low-memory fallback mode."""
    path = TABLES / "resultados-mecanicos.csv"
    fields = [
        "temperatura_condutor_C", "vento_m_s", "vao_inicial", "tracao_horizontal_kN",
        "flecha_vertical_m", "flecha_transversal_m", "flecha_resultante_m",
        "clearance_minimo_sintetico_m", "tracao_no_apoio_kN", "fracao_carga_ruptura",
    ]
    span = f(p, "span_m")
    n_span = int(f(p, "length_km") * 1000 / span)
    temps = [f(p, f"mechanical_conductor_temperatures_c_{i}") for i in range(1, 4)]
    winds = [f(p, f"mechanical_wind_speeds_m_s_{i}") for i in range(1, 4)]
    route_stations = [f(p, f"route_km_{i}") * 1000 for i in range(1, 17)]
    rows = []
    for temp in temps:
        for wind in winds:
            sag, lateral_sag, resultant_sag, horizontal, support = sag_state(p, span, temp, wind)
            for index in range(1, n_span + 1):
                start = (index - 1) * span
                t_route = [(station - start) / span for station in route_stations if start < station < start + span]
                samples = sorted({i / 50 for i in range(51)} | set(t_route))
                z0 = profile_elevation(p, start)
                z1 = profile_elevation(p, start + span)
                clearances = []
                for t in samples:
                    ground = profile_elevation(p, start + span * t)
                    attachment = (z0 + f(p, "mean_conductor_height_m")) * (1 - t) + (z1 + f(p, "mean_conductor_height_m")) * t
                    clearances.append(attachment - sag * 4 * t * (1 - t) - ground)
                rows.append({
                    "temperatura_condutor_C": temp,
                    "vento_m_s": wind,
                    "vao_inicial": index,
                    "tracao_horizontal_kN": horizontal / 1000,
                    "flecha_vertical_m": sag,
                    "flecha_transversal_m": lateral_sag,
                    "flecha_resultante_m": resultant_sag,
                    "clearance_minimo_sintetico_m": min(clearances),
                    "tracao_no_apoio_kN": support / 1000,
                    "fracao_carga_ruptura": support / f(p, "conductor_rated_tensile_n"),
                })
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    p = get_params()
    electrical = read_csv(TABLES / "resultados-eletricos.csv")
    rebuild_mechanical_table(p)
    mechanical = read_csv(TABLES / "resultados-mecanicos.csv")
    thermal = read_csv(TABLES / "ampacidade-estimada.csv")

    loads = np.array([float(r["P_MW"]) for r in electrical])
    pfs = np.array([float(r["fp"]) for r in electrical])
    currents = np.array([float(r["I_recebimento_A"]) for r in electrical])
    losses = np.array([float(r["perdas_MW"]) for r in electrical])
    imax = currents.max()

    fig, axes = plt.subplots(2, 1, figsize=(9, 7))
    for pf in sorted(set(pfs)):
        mask = np.isclose(pfs, pf)
        order = np.argsort(loads[mask])
        axes[0].plot(loads[mask][order], currents[mask][order], "o-", label=f"fp {pf:.2f}")
        axes[1].plot(loads[mask][order], losses[mask][order], "o-", label=f"fp {pf:.2f}")
    axes[0].set(ylabel="Corrente de recebimento (A)", title="Nove combinações de carga e fator de potência")
    axes[1].set(xlabel="Carga ativa recebida (MW)", ylabel="Perdas estimadas (MW)", title="Perdas série e efeito do fator de potência")
    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.legend(ncol=3)
    save(fig, "operacao-eletrica.png")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ambient in sorted({float(r["ambiente_C"]) for r in thermal}):
        group = sorted((r for r in thermal if float(r["ambiente_C"]) == ambient), key=lambda r: float(r["vento_m_s"]))
        wind = [float(r["vento_m_s"]) for r in group]
        ampacity = [float(r["ampacidade_feixe_A"]) for r in group]
        axes[0].plot(wind, ampacity, "o-", label=f"ambiente {ambient:.0f} °C")
        axes[1].plot(wind, [float(r["margem_percentual"]) for r in group], "o-", label=f"ambiente {ambient:.0f} °C")
    axes[0].axhline(imax, color="crimson", linestyle="--", label=f"I máx. = {imax:.1f} A")
    axes[0].set(xlabel="Vento transversal assumido (m/s)", ylabel="Ampacidade de feixe (A)", title="Equilíbrio térmico simplificado")
    axes[1].axhline(0, color="crimson", linestyle="--")
    axes[1].set(xlabel="Vento transversal assumido (m/s)", ylabel="Margem sobre I máx. (%)", title="Margem por cenário ambiental")
    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    save(fig, "triagem-termica.png")

    mechanical_t = np.array([float(r["temperatura_condutor_C"]) for r in mechanical])
    mechanical_w = np.array([float(r["vento_m_s"]) for r in mechanical])
    sag = np.array([float(r["flecha_vertical_m"]) for r in mechanical])
    tension = np.array([float(r["tracao_no_apoio_kN"]) for r in mechanical])
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.7))
    for wind in sorted(set(mechanical_w)):
        group = [i for i in range(len(mechanical)) if mechanical_w[i] == wind]
        temps = sorted(set(mechanical_t[group]))
        axes[0].plot(temps, [sag[group][np.where(mechanical_t[group] == temp)[0][0]] for temp in temps], "o-", label=f"vento {wind:g} m/s")
        axes[1].plot(temps, [tension[group][np.where(mechanical_t[group] == temp)[0][0]] for temp in temps], "o-", label=f"vento {wind:g} m/s")
        lateral_group = [float(mechanical[i]["flecha_transversal_m"]) for i in group]
        axes[2].plot(temps, [lateral_group[np.where(mechanical_t[group] == temp)[0][0]] for temp in temps], "o-", label=f"vento {wind:g} m/s")
    axes[0].set(xlabel="Temperatura do condutor (°C)", ylabel="Flecha vertical por vão (m)", title="Componente vertical")
    axes[1].set(xlabel="Temperatura do condutor (°C)", ylabel="Tração no apoio (kN)", title="Tração no apoio")
    axes[2].set(xlabel="Temperatura do condutor (°C)", ylabel="Deslocamento transversal (m)", title="Componente pelo vento")
    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    save(fig, "flecha-tracao.png")

    # Recreate the approximate 140 MW line-voltage profile used by run_analysis.m.
    spacing = [f(p, f"phase_spacing_m_{i}") for i in range(1, 4)]
    distances = [abs(spacing[1] - spacing[0]), abs(spacing[2] - spacing[1]), abs(spacing[2] - spacing[0])]
    gmd = math.prod(distances) ** (1 / 3)
    n_sub = f(p, "bundle_subconductors")
    bundle_spacing = f(p, "bundle_spacing_m")
    gmr_bundle = math.sqrt(f(p, "conductor_gmr_m") * bundle_spacing)
    radius_bundle = math.sqrt(f(p, "conductor_diameter_m") / 2 * bundle_spacing)
    lpkm = 2e-4 * math.log(gmd / gmr_bundle)
    cpm = 2 * math.pi * 8.8541878128e-12 / math.log(gmd / radius_bundle)
    freq = f(p, "frequency_hz")
    length_km = f(p, "length_km")
    vll = f(p, "voltage_kv") * 1000
    vr = vll / math.sqrt(3)
    rphase = f(p, "conductor_rac75_ohm_km") / n_sub
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    for pf in sorted({float(r["fp"]) for r in electrical}):
        pdesign = max(float(r["P_MW"]) for r in electrical)
        qdesign = pdesign * math.tan(math.acos(pf))
        i_design = ((pdesign + 1j * qdesign) * 1e6 / (3 * vr)).conjugate()
        profile = []
        for fraction in np.linspace(0, 1, 61):
            zpart = (rphase + 1j * 2 * math.pi * freq * lpkm) * length_km * fraction
            ypart = 1j * 2 * math.pi * freq * cpm * length_km * 1000 * fraction
            apart = 1 + ypart * zpart / 2
            bpart = zpart * (1 + ypart * zpart / 4)
            profile.append(math.sqrt(3) * abs(apart * vr + bpart * i_design) / 1000)
        ax.plot(np.linspace(0, length_km, 61), profile, label=f"fp {pf:.2f}")
    ax.set(xlabel="Distância do terminal receptor (km)", ylabel="Tensão linha-linha (kV)", title="Perfil aproximado por segmentos do modelo nominal π")
    ax.grid(True, alpha=0.3)
    ax.legend()
    save(fig, "perfil-tensao.png")

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for load in sorted(set(loads)):
        mask = np.isclose(loads, load)
        order = np.argsort(pfs[mask])
        ax.plot(pfs[mask][order], losses[mask][order], "o-", label=f"P = {load:.0f} MW")
    ax.set(xlabel="Fator de potência", ylabel="Perdas estimadas (MW)", title="Sensibilidade das perdas ao fator de potência")
    ax.grid(True, alpha=0.3)
    ax.legend()
    save(fig, "sensibilidade-fp.png")

    span_cases = np.array([200, 250, 300, 350, 400, 450], dtype=float)
    temp_limit = f(p, "conductor_temperature_limit_c")
    sag_values = [sag_state(p, span, temp_limit, 0)[0] for span in span_cases]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(span_cases, sag_values, "o-", color="darkgreen")
    ax.set(xlabel="Vão uniforme hipotético (m)", ylabel="Flecha vertical calculada (m)", title="Sensibilidade mecânica ao comprimento do vão")
    ax.grid(True, alpha=0.3)
    save(fig, "sensibilidade-vaos.png")

    print(f"P24: 6 gráficos recriados; corrente máxima {imax:.2f} A; método de triagem simplificado.")


if __name__ == "__main__":
    main()
