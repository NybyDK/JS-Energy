# JS Energy
Benchmarking various JavaScript engines' energy consumption

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

# Analysis
The analysis scripts are provided as-is with no promises\
They currently assume the input file is in the analysis/ folder and is named 1000-runs. Just change it if needed\
Run with `python file.py` (assuming you changed directory to analysis folder) and install missing packages with pip\
`normalize-total.py` requires the output of `total.py`
