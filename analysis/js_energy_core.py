import os
import pandas as pd
import numpy as np

FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

MAIN_ENGINES = ["v8", "sm-146.0", "jsc", "graaljs", "hermes", "qjs", "xs"]

ENGINE_ALIAS = {
    "v8": "V8-0",
    "sm-146.0": "SM-0",
    "jsc": "JSC-0",
    "graaljs": "GJS-0",
    "hermes": "H-0",
    "qjs": "QJS-0",
    "xs": "XS-0",
}

VERSION_ALIAS = {
    "v8": "V8-0",
    "v8-13.3.404": "V8-1",
    "v8-12.2.149": "V8-2",
    "sm-146.0": "SM-0",
    "sm-127.0": "SM-1",
    "sm-114.0.1": "SM-2",
    "jsc": "JSC-0",
    "graaljs": "GJS-0",
    "graaljs-24.1.1": "GJS-1",
    "graaljs-23.0.2": "GJS-2",
    "hermes": "H-0",
    "hermes-0.12.0": "H-2",
    "qjs": "QJS-0",
    "quickjs-0.7.0": "QJS-1",
    "quickjs-0.1.0": "QJS-2",
    "xs": "XS-0",
    "xs-5.3.0": "XS-1",
    "xs-4.3.4": "XS-2",
}

STEADY_RUNS = 1000

def compute_energy_per_run(df):
    df = df.copy()
    df['energy_per_run'] = df['energy_uj'] / df['runs'] / 1e6
    return df

def aggregate_warmup(df, max_run=10):
    warmup_mask = df['runs'] <= max_run
    warmup_grouped = df[warmup_mask].groupby(['file','engine_alias']).agg({
        'energy_per_run': 'mean',
        'runs': 'max'
    }).reset_index()
    df_rest = df[~warmup_mask]
    return pd.concat([df_rest, warmup_grouped], ignore_index=True)

def normalize_row(row):
    engines = [float(x) for x in row[1:]]
    min_val = min(engines)
    max_val = max(engines)
    if max_val == min_val:
        normalized = [1.0 for _ in engines]
    else:
        normalized = [(max_val - x) / (max_val - min_val) for x in engines]
    return [row[0]] + normalized
