#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_results():
    input_file = "results.csv"
    output_image = "benchmark_graph.png"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        sys.exit(1)
        
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
        
    required_columns = ['Time', 'Latency', 'Scenario']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: CSV must contain columns: {required_columns}")
        print(f"Found: {df.columns.tolist()}")
        # Temporary compatibility check for benchmark.py output which is Timestamp, Latency_ms, Status
        # but the prompt specifically requested Time, Latency, Scenario for this script.
        # I will assume the user has formatted the CSV correctly or merged multiple runs.
        sys.exit(1)

    # Convert Latency to numeric, coercing errors to NaN (handling 'TIMEOUT')
    df['Latency'] = pd.to_numeric(df['Latency'], errors='coerce')
    
    # Handle Time relative to start
    df['Time'] = df['Time'] - df['Time'].min()

    plt.figure(figsize=(12, 6))
    
    scenarios = df['Scenario'].unique()
    for scenario in scenarios:
        subset = df[df['Scenario'] == scenario].sort_values('Time')
        plt.plot(subset['Time'], subset['Latency'], label=scenario, marker='o', markersize=2)

    plt.title('DDoS Attack Latency Comparison')
    plt.xlabel('Time (s)')
    plt.ylabel('Latency (ms)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Check if we should use log scale
    # If max latency is very high relative to min (e.g. > 100x), or user explicitly asked check
    if not df['Latency'].dropna().empty:
        max_lat = df['Latency'].max()
        min_lat = df['Latency'].min()
        if max_lat > 0 and (min_lat <= 0 or max_lat / min_lat > 100):
             plt.yscale('log')
             plt.ylabel('Latency (ms) - Log Scale')

    print(f"Saving graph to {output_image}...")
    plt.savefig(output_image)
    print("Done.")

if __name__ == "__main__":
    plot_results()
