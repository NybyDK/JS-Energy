import pandas as pd
import os
from js_energy_core import FIGURES_DIR, STEADY_RUNS, VERSION_ALIAS, compute_energy_per_run

ENGINE_FAMILIES = {
    "V8": ["V8-0","V8-1","V8-2"],
    "SM": ["SM-0","SM-1","SM-2"],
    "JSC": ["JSC-0"],
    "GJS": ["GJS-0","GJS-1","GJS-2"],
    "H": ["H-0","H-1"],
    "QJS": ["QJS-0","QJS-1","QJS-2"],
    "XS": ["XS-0","XS-1","XS-2"]
}

df = pd.read_csv('1000-runs.csv')
df = df[df['runs']==STEADY_RUNS].copy()
df['engine_alias'] = df['engine'].map(VERSION_ALIAS)
df = df.dropna(subset=['engine_alias'])
df = compute_energy_per_run(df)

rows=[]
for engine_family, aliases in ENGINE_FAMILIES.items():
    subset = df[df['engine_alias'].isin(aliases)]
    if subset.empty: continue
    avg_energy = subset.groupby('engine_alias')['energy_per_run'].mean().reindex(aliases)
    baseline = avg_energy.iloc[0]
    for alias,value in avg_energy.items():
        rows.append({
            "Engine": engine_family,
            "Version": alias,
            "Avg_Energy_per_run_J": value,
            "Delta_percent_vs_first":100*(value-baseline)/baseline
        })

condensed_df = pd.DataFrame(rows)
out_path = os.path.join(FIGURES_DIR,'RQ3_versions_condensed.csv')
condensed_df.to_csv(out_path,index=False)
print(f"Condensed RQ3 table saved as '{out_path}'.")
print(f"Rows in condensed table: {len(condensed_df)}")
