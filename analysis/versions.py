import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
from js_energy_core import FIGURES_DIR, VERSION_ALIAS, compute_energy_per_run, aggregate_warmup

VERSION_COLORS = ['tab:blue','tab:orange','tab:green']
ENGINE_FAMILIES = {
    "V8":["V8-0","V8-1","V8-2"],
    "SM":["SM-0","SM-1","SM-2"],
    "JSC":["JSC-0"],
    "GJS":["GJS-0","GJS-1","GJS-2"],
    "H":["H-0","H-2"],
    "QJS":["QJS-0","QJS-1","QJS-2"],
    "XS":["XS-0","XS-1","XS-2"]
}

df = pd.read_csv("1000-runs.csv")
df['engine_alias'] = df['engine'].map(VERSION_ALIAS)
df = df.dropna(subset=['engine_alias'])
df = compute_energy_per_run(df)
df = aggregate_warmup(df,max_run=10)

for fam, aliases in ENGINE_FAMILIES.items():
    subset = df[df['engine_alias'].isin(aliases)]
    if subset.empty: continue
    benchmarks = subset['file'].unique()
    n_rows = int(np.ceil(len(benchmarks)/3))
    n_cols = min(3,len(benchmarks))
    fig, axes = plt.subplots(n_rows,n_cols,figsize=(15,4*n_rows),squeeze=False)
    for idx, benchmark in enumerate(benchmarks):
        r,c = divmod(idx,3)
        ax = axes[r,c]
        bench_df = subset[subset['file']==benchmark].sort_values('runs')
        for i, alias in enumerate(aliases):
            alias_df = bench_df[bench_df['engine_alias']==alias]
            ax.plot(alias_df['runs'], alias_df['energy_per_run'], label=alias, color=VERSION_COLORS[i])
        ax.set_title(benchmark)
        ax.set_xlabel("Runs")
        ax.set_ylabel("Energy per run (J)")
    for idx in range(len(benchmarks), n_rows*n_cols):
        r,c = divmod(idx,3)
        fig.delaxes(axes[r,c])
    handles=[Line2D([0],[0],color=VERSION_COLORS[i],lw=2,label=a) for i,a in enumerate(aliases)]
    fig.legend(handles=handles,title="Engine Version",loc='upper center',ncol=len(aliases),fontsize=10,title_fontsize=12)
    plt.tight_layout(rect=[0,0,1,0.95])
    plt.savefig(os.path.join(FIGURES_DIR,f"RQ3_appendix_{fam}.png"))
    plt.close()

print(f"RQ3 appendix plots complete. PNGs saved in '{FIGURES_DIR}/'.")
