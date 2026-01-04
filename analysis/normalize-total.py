import os
import csv
from js_energy_core import FIGURES_DIR, normalize_row

INPUT_FILE = os.path.join(FIGURES_DIR,"total_energy.csv")
OUTPUT_FILE = os.path.join(FIGURES_DIR,"total_normalized.csv")

with open(INPUT_FILE,newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    rows = list(reader)

normalized_rows = [normalize_row(row) for row in rows]

with open(OUTPUT_FILE,'w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(normalized_rows)

print(f"Normalized CSV saved to '{OUTPUT_FILE}'.")
