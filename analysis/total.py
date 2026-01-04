import pandas as pd
import matplotlib.pyplot as plt
import os
from js_energy_core import ENGINE_ALIAS, FIGURES_DIR, compute_energy_per_run, STEADY_RUNS

df = pd.read_csv('1000-runs.csv')
df = df[df['engine'].isin(ENGINE_ALIAS.keys())]
df = df[df['runs']==STEADY_RUNS]
df['engine_alias'] = df['engine'].map(ENGINE_ALIAS)
df = compute_energy_per_run(df)

pivot = df.pivot(index='file', columns='engine_alias', values='energy_per_run')
pivot.columns.name = "Engine Alias"
pivot.to_csv(os.path.join(FIGURES_DIR,'total_energy.csv'))

plt.rcParams.update({'font.size':12})
plt.figure(figsize=(14,6))
pivot.plot(kind='bar',figsize=(14,6))
plt.ylabel('Energy per run (J)')
plt.xlabel('Benchmark')
plt.title('Total energy per run per main engine (most recent versions)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR,'total_energy.png'))
plt.close()

print(f"Finish total.py")
