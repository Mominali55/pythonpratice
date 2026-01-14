#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def process_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
        
    required_cols = ['Timestamp', 'Latency_ms']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: {file_path} missing required columns {required_cols}")
        print(f"Found: {df.columns.tolist()}")
        return None
        
    # Convert Latency to numeric, coerce errors (TIMEOUT) to NaN
    df['Latency_ms'] = pd.to_numeric(df['Latency_ms'], errors='coerce')
    
    # Normalize time
    if not df.empty:
        df['Timestamp'] = df['Timestamp'] - df['Timestamp'].iloc[0]
        
    return df

def plot_comparison():
    file_baseline = "results_baseline.csv"
    file_mitigation = "results_mitigation.csv"
    output_image = "comparison_graph.png"
    
    # 6. Error Handling
    if not os.path.exists(file_baseline) or not os.path.exists(file_mitigation):
        print("Error: Missing input files.")
        print(f"Please ensure '{file_baseline}' and '{file_mitigation}' exist.")
        print("Run the benchmark twice and rename 'results.csv' accordingly.")
        sys.exit(1)
        
    print("Loading data...")
    df_base = process_data(file_baseline)
    df_mit = process_data(file_mitigation)
    
    if df_base is None or df_mit is None:
        sys.exit(1)

    plt.figure(figsize=(10, 6))
    
    # 3. Visualization
    plt.plot(df_base['Timestamp'], df_base['Latency_ms'], label='Without XDP', color='red', alpha=0.7)
    plt.plot(df_mit['Timestamp'], df_mit['Latency_ms'], label='With XDP', color='green', alpha=0.7)
    
    plt.title('DDoS Mitigation Effectiveness: Latency Comparison')
    plt.xlabel('Time (s)')
    plt.ylabel('Latency (ms)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    # 4. Scaling
    max_latency = max(df_base['Latency_ms'].max(), df_mit['Latency_ms'].max())
    if max_latency > 1000:
        print(f"Max latency ({max_latency}ms) > 1000ms. Switching to log scale.")
        plt.yscale('log')
        plt.ylabel('Latency (ms) - Log Scale')
        
    print(f"Saving chart to {output_image}...")
    plt.savefig(output_image)
    print("Done.")

if __name__ == "__main__":
    plot_comparison()
