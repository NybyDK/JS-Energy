#!/bin/bash

BENCH_DIR="$1"
OUT="results.csv"

if [ ! -d "$BENCH_DIR" ]; then
    echo "Usage: $0 <benchmarks_dir>"
    exit 1
fi

RUN_COUNTS=(1 1 1 1 1 1 1 1 1 1
    2 2 2 2 2 2 2 2 2 2
    3 3 3 3 3 3 3 3 3 3
    4 4 4 4 4 4 4 4 4 4
    5 5 5 5 5 5 5 5 5 5 
    6 6 6 6 6 6 6 6 6 6
    7 7 7 7 7 7 7 7 7 7
    8 8 8 8 8 8 8 8 8 8
    9 9 9 9 9 9 9 9 9 9
    10 20 30 40 50 60 70 80 90 100 200 300 400 500 600 700 800 900 1000)
# RUN_COUNTS=(1 2 3)
ENGINES=("v8" "v8-13.3.404" "v8-12.2.149"
    "sm-146.0" "sm-127.0" "sm-114.0.1"
    "jsc"
    "graaljs" "graaljs-24.1.1" "graaljs-23.0.2"
    "hermes" "hermes-0.12.0"
    "qjs" "quickjs-0.7.0" "quickjs-0.1.0"
    "xs" "xs-5.3.0" "xs-4.3.4")
NEEDS_WRAPPER=("v8" "v8-13.3.404" "v8-12.2.149"
    "sm-146.0" "sm-127.0" "sm-114.0.1"
    "jsc"
    "graaljs" "graaljs-24.1.1" "graaljs-23.0.2")
WRAPPER="jit-wrapper.js"

RAPL="/sys/class/powercap/intel-rapl:0/energy_uj"
MAX_ENERGY=$(cat /sys/class/powercap/intel-rapl:0/max_energy_range_uj)

if [ ! -f "$RAPL" ]; then
    echo "RAPL not available at $RAPL"
    exit 1
fi

echo "Starting benchmarks from ${RUN_COUNTS[0]} to ${RUN_COUNTS[-1]} iterations..."

echo "file,engine,runs,energy_uj,real_sec,user_sec,sys_sec" > "$OUT"

for RUNS in "${RUN_COUNTS[@]}"; do
    echo "=== Running benchmarks with $RUNS iterations ==="

    for BENCH in "$BENCH_DIR"/*.js; do
        [ -e "$BENCH" ] || continue
        NAME=$(basename "$BENCH")

        for ENGINE in "${ENGINES[@]}"; do
            sleep 10
            command -v "$ENGINE" >/dev/null || continue

            ENERGY_BEFORE=$(cat "$RAPL")

            if [[ " ${NEEDS_WRAPPER[@]} " =~ " $ENGINE " ]]; then
                TIME_OUTPUT=$( { /usr/bin/time -f "%e %U %S" \
                     taskset -c 0 "$ENGINE" -e "var __BENCH_ARGS__ = ['$BENCH','$ENGINE',$RUNS]; load('$WRAPPER');"; } 2>&1 >/dev/null )
            else
                TIME_OUTPUT=$( { /usr/bin/time -f "%e %U %S" \
                     taskset -c 0 bash -c "for ((r=1;r<=$RUNS;r++)); do $ENGINE $BENCH >/dev/null 2>&1; done"; } 2>&1 >/dev/null )
            fi

            ENERGY_AFTER=$(cat "$RAPL")
            DELTA=$((ENERGY_AFTER - ENERGY_BEFORE))
            [ "$DELTA" -lt 0 ] && DELTA=$((DELTA + MAX_ENERGY))

            REAL=$(echo "$TIME_OUTPUT" | awk '{print $1}')
            USER=$(echo "$TIME_OUTPUT" | awk '{print $2}')
            SYS=$(echo "$TIME_OUTPUT" | awk '{print $3}')

            echo "[$ENGINE] $RUNS x $NAME: Energy Avg: $((DELTA / RUNS)) uJ | $REAL s"

            echo "$NAME,$ENGINE,$RUNS,$DELTA,$REAL,$USER,$SYS" >> "$OUT"
        done
    done
done

echo "Done > $OUT"
