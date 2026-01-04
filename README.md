# JS Energy
Benchmarking various JavaScript engines' energy consumption

# Just here for data?
[analysis/1000-runs.csv](analysis/1000-runs.csv)\
Reminder that entries with runs [1..10] are repeated 10 times

# Prerequisites
- Linux system with RAPL
- Installed JavaScript engines (I recommend [JSVU](https://github.com/GoogleChromeLabs/jsvu))
  - V8, SpiderMonkey, JavaScriptCore, GraalJS, Hermes, QuickJS, and Moddable XS
  - SpiderMonkey is currently hardcoded to sm-146.0, because the most recent installed version was a beta release. Just change it if needed
- Scripts folder with benchmarks (already supplied, but can just add more, they just need to have a runBenchmark() function and a function call)

# Execute script
If the bash script does not already have permission:\
`chmod +x run-benchmarks.sh`

Then:\
`./run-benchmarks.sh /scripts`

Hopefully Windows line endings don't screw you over

[benchmark.sh](benchmark.sh) needs to be edited if you change versions/engines, but it is intuitive in there\
If you want to run this while disconnected from SSH, I recommend [tmux](https://github.com/tmux/tmux/wiki), start session, start script, deattach from session and you can come back and reattach any time

# Analysis
The analysis scripts are provided as-is with no promises\
They currently assume the input file is in the analysis/ folder and is named 1000-runs. Just change it if needed\
Run with `python file.py` (assuming you changed directory to analysis folder) and install missing packages with pip\
`normalize-total.py` requires the output of `total.py`
