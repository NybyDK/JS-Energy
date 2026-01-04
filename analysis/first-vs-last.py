import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from js_energy_core import MAIN_ENGINES, ENGINE_ALIAS, FIGURES_DIR, compute_energy_per_run

df = pd.read_csv('1000-runs.csv')
df = df[df['engine'].isin(MAIN_ENGINES)]
df['engine_alias'] = df['engine'].map(ENGINE_ALIAS)
df = compute_energy_per_run(df)

runs1 = df[df['runs']==1]
runs1_avg = runs1.groupby(['engine_alias','file'], as_index=False)['energy_per_run'].mean()
runs1000 = df[df['runs']==1000][['engine_alias','file','energy_per_run']]
merged = pd.merge(runs1_avg, runs1000, on=['engine_alias','file'], suffixes=('_first','_last'))

summary = merged.groupby('engine_alias').agg(
    avg_first_run=('energy_per_run_first','mean'),
    avg_last_run=('energy_per_run_last','mean')
).reset_index()
summary['delta_percent'] = 100*(summary['avg_first_run']-summary['avg_last_run'])/summary['avg_first_run']
summary.to_csv(os.path.join(FIGURES_DIR,'first_vs_last_run_summary.csv'), index=False)

print("Average per engine:")
print(summary)

plt.figure(figsize=(12,6))
x = np.arange(len(summary['engine_alias']))
width = 0.35
plt.bar(x - width/2, summary['avg_first_run'], width, label='First Run')
plt.bar(x + width/2, summary['avg_last_run'], width, label='Last Run')
plt.xticks(x, summary['engine_alias'], rotation=45)
plt.ylabel('Energy per run (J)')
plt.title('First vs Last Run Energy per Engine')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR,'first_vs_last_run_bar.png'))
plt.close()

print(f"\nAnalysis complete. CSVs and bar chart saved in '{FIGURES_DIR}/'.")
