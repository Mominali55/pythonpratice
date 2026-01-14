# eBPF/XDP Setup with BCC

This repository contains scripts to set up an eBPF/XDP development environment on Ubuntu using the BCC framework.

## Prerequisites

- Ubuntu Linux
- Sudo privileges

## Installation

Run the setup script to install all necessary dependencies:

```bash
sudo ./setup.sh
```

This will install:
- `bpfcc-tools`
- `linux-headers` for your current kernel
- `clang` and `llvm`
- `python3-bpfcc`

## Verification

To verify that the installation was successful and that you can load XDP programs, run the verification script:

```bash
sudo python3 verify_xdp.py
```

If successful, you should see output indicating that the XDP program was loaded and attached to the loopback interface (`lo`).

Example output:
```
Compiling and loading XDP program...
Attaching XDP program to lo...
XDP program loaded successfully!
Check /sys/kernel/debug/tracing/trace_pipe for output (optional).
Press Ctrl+C to detach and exit.
```

Press `Ctrl+C` to stop the script and verify that it detaches cleanly.

## XDP Mitigation

The repository includes an XDP program to filter traffic based on a blocklist.

### 1. `mitigation.c`
Contains the eBPF/XDP logic:
- Parses Ethernet and IP headers.
- Checks if Source IP is in the `blocklist` map.
- Drops packet if found, passes otherwise.

### 2. `load_mitigation.py`
Loader script ensuring the XDP program is attached and map is accessible.

**Usage:**
```bash
sudo python3 load_mitigation.py [interface]
```
*Default interface is `lo`.*

To block an IP, you can programmatically interact with the `blocklist` map (examples in `load_mitigation.py` comments).

### 3. `loader.py`
Advanced loader with integrated **ML-based DDoS detection**.

**Usage:**
```bash
sudo python3 loader.py
```
- Attaches to `lo`.
- **Auto-Protection**: Loads `ddos_model.joblib` and simulates traffic analysis every 2 seconds.
- If an attack is detected, it automatically blocks a simulated IP and logs a warning.
- Prints drop stats.


## ML Model Training

To train the DDoS detection model:

```bash
python3 train_model.py
```

This script:
1. Loads `data/cicddos2019.csv`.
2. Cleans and filters the data ("Benign", "Syn", "UDP").
3. Trains a Random Forest Classifier.
4. Saves the model to `ddos_model.joblib`.
5. Prints a classification report.

## Mininet Simulation

To simulate the network topology:

```bash
sudo python3 topo.py
```

This starts a Mininet environment with:
- 1 Switch (`s1`)
- 3 Hosts (`h1`, `h2`, `h3`)
- 10Mbps bandwidth limits on links.

You will land in the Mininet CLI.
- Run `xterm h1 h2 h3` to open terminals for hosts.
- Use `pingall` to test connectivity.
- `exit` to stop the network.

## Benchmarking

To run the full DDoS simulation and gather latency metrics:

```bash
sudo python3 benchmark.py
```

This script will:
1. Start the Mininet topology.
2. Launch an HTTP server on `h1`.
3. Start a latency monitor on `h3` (logs to `results.csv`).
4. Launch an `hping3` flood attack from `h2` targeting `h1` (after 5 seconds).
5. Run for ~30 seconds and stop.

**Note:** For mitigation to be effective, you may need to manually trigger `loader.py` or ensure `h2`'s IP is blocked, as the current loader blocks simulated IPs given the random feature input.

## Analysis

To visualize the results:

```bash
python3 plot_results.py
```

**Requirement:** You must provide a `results.csv` file with columns `Time`, `Latency`, `Scenario`.
- This script generates `benchmark_graph.png`.
- It automatically uses a log scale if the latency variance is high.

### Comparative Analysis

To plot a direct comparison between "With XDP" and "Without XDP":

1. Run benchmark without XDP -> Rename `results.csv` to `results_baseline.csv`.
2. Run benchmark with XDP -> Rename `results.csv` to `results_mitigation.csv`.
3. Run:
```bash
python3 plot_comparison.py
```
This generates `comparison_graph.png` showing:
- **Red Line**: Baseline (No Protection)
- **Green Line**: Mitigation (XDP Enabled)







