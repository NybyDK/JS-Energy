import pandas as pd
import os
from js_energy_core import FIGURES_DIR, STEADY_RUNS, compute_energy_per_run

LATEST_ENGINE_VERSION = {
    "v8": "V8-0",
    "sm-146.0": "SM-0",
    "jsc": "JSC-0",
    "graaljs": "GJS-0",
    "hermes": "H-0",
    "qjs": "QJS-0",
    "xs": "XS-0",
}

MULTI_IMPL_BENCHMARKS = {
    "mandelbrot": ["mandelbrot.js","mandelbrot-2.js","mandelbrot-8.js"],
    "fasta": ["fasta.js","fasta-8.js"],
    "spectral-norm": ["spectral-norm.js","spectral-norm-8.js"]
}

df = pd.read_csv('1000-runs.csv')
df = compute_energy_per_run(df)
df = df[df['runs']==STEADY_RUNS].copy()
df['engine_alias'] = df['engine'].map(LATEST_ENGINE_VERSION)
df = df.dropna(subset=['engine_alias'])

for benchmark_group, files in MULTI_IMPL_BENCHMARKS.items():
    rows = []
    for engine_alias in df['engine_alias'].unique():
        subset = df[(df['engine_alias']==engine_alias)&(df['file'].isin(files))]
        if subset.empty: continue
        subset = subset.set_index('file').reindex(files)
        energies = subset['energy_per_run'].values.tolist()
        deltas = [100*(energies[i]-energies[i-1])/energies[i-1] for i in range(1,len(energies))]
        row = {"Engine": engine_alias}
        for f,e in zip(files,energies): row[f]=e
        for i,d in enumerate(deltas,start=2): row[f"Delta {i} vs {i-1} (%)"]=d
        rows.append(row)
    rq3_df = pd.DataFrame(rows)
    out_path = os.path.join(FIGURES_DIR,f'RQ3_{benchmark_group}.csv')
    rq3_df.to_csv(out_path,index=False)
    print(f"Saved CSV for {benchmark_group} as '{out_path}'")
