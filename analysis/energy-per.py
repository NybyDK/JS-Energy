import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.ticker import FuncFormatter, LogLocator
from js_energy_core import MAIN_ENGINES, ENGINE_ALIAS, FIGURES_DIR, compute_energy_per_run

df = pd.read_csv("1000-runs.csv")
df = df[df["engine"].isin(MAIN_ENGINES)]
df["engine_alias"] = df["engine"].map(ENGINE_ALIAS)
df = compute_energy_per_run(df)

early_runs = df[df["runs"] <= 10]
normalized_early = early_runs.groupby(["engine_alias","file","runs"], as_index=False)["energy_per_run"].mean()
later_runs = df[df["runs"] > 10]
df_normalized = pd.concat([normalized_early, later_runs], ignore_index=True)
df_normalized = df_normalized.sort_values(["file","engine_alias","runs"])

def joule_formatter(y,_):
    if y >= 1: return f"{y:.0f} J"
    if y >= 0.1: return f"{y:.1f} J"
    return f"{y:.2f} J"

formatter = FuncFormatter(joule_formatter)

for benchmark in df_normalized["file"].unique():
    subset = df_normalized[df_normalized["file"]==benchmark]
    plt.figure(figsize=(10,5))
    ax = plt.gca()
    for engine in MAIN_ENGINES:
        alias = ENGINE_ALIAS[engine]
        engine_data = subset[subset["engine_alias"]==alias].sort_values("runs")
        if engine_data.empty: continue
        ax.plot(engine_data["runs"], engine_data["energy_per_run"], marker="o", linestyle="-", label=alias)
    ax.set_xlabel("Run #")
    ax.set_ylabel("Energy per run (J)")
    ax.set_title(f"Energy per run for benchmark: {benchmark}")
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(LogLocator(base=10.0, subs=None, numticks=6))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.linspace(1.0,10.0,4), numticks=10))
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_minor_formatter(formatter)
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    filename = f"{benchmark.replace('.', '_').replace('-', '_')}_comparison.png"
    plt.savefig(os.path.join(FIGURES_DIR, filename))
    plt.close()

print(f"Per-benchmark comparative line plots saved in '{FIGURES_DIR}/'.")
