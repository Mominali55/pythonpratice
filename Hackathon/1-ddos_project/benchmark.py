#!/usr/bin/env python3
import time
import os
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from topo import DDoSTopo

# Helper script for latency monitoring (to be run on h3)
latency_monitor_code = """
import time
import requests
import sys
import csv

target_url = sys.argv[1]
output_file = "results.csv"

print(f"Monitoring latency to {target_url}...")

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Latency_ms", "Status"])
    csvfile.flush()
    
    start_time = time.time()
    while time.time() - start_time < 30:  # Run for 30 seconds
        try:
            req_start = time.time()
            resp = requests.get(target_url, timeout=2)
            req_end = time.time()
            latency = (req_end - req_start) * 1000
            writer.writerow([time.time(), f"{latency:.2f}", resp.status_code])
            csvfile.flush()
        except requests.exceptions.Timeout:
            writer.writerow([time.time(), "TIMEOUT", "TIMEOUT"])
            csvfile.flush()
        except Exception as e:
            writer.writerow([time.time(), "ERROR", str(e)])
            csvfile.flush()
        
        time.sleep(0.5)
"""

def run_benchmark():
    # Write the latency monitor script to disk so h3 can use it
    with open("latency_monitor.py", "w") as f:
        f.write(latency_monitor_code)

    topo = DDoSTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    
    print(f"h1 IP: {h1.IP()}")
    print(f"h2 IP: {h2.IP()}")
    print(f"h3 IP: {h3.IP()}")

    # 1. Start HTTP Server on h1
    print("\nStarting HTTP Server on h1...")
    h1.cmd('python3 -m http.server 80 > /dev/null 2>&1 &')
    time.sleep(2) # Wait for server to start

    # Start mitigation (optional, uncomment if needed, but requires loader.py to block correct IPs)
    print("Starting Mitigation on h1...")
    h1.cmd('python3 loader.py h1-eth0 > mitigation.log 2>&1 &')

    # 3. Start Latency Monitor on h3
    print("Starting Latency Monitor on h3...")
    h3.cmd(f'python3 latency_monitor.py http://{h1.IP()}:80 &')

    print("collecting baseline data for 5 seconds...")
    time.sleep(5)

    # 2. Start hping3 flood from h2
    print("\n[ATTACK] Starting UDP flood from h2 -> h1...")
    # Using UDP flood to saturate link
    h2.cmd(f'hping3 --flood --udp -p 80 {h1.IP()} > /dev/null 2>&1 &')

    print("Attack running for 15 seconds...")
    time.sleep(15)

    print("\nStopping attack...")
    h2.cmd('killall hping3')

    print("Collecting recovery data for 5 seconds...")
    time.sleep(5)

    print("\nStopping network...")
    net.stop()
    
    print("\nBenchmark complete. Results saved to 'results.csv'.")
    if os.path.exists("latency_monitor.py"):
        os.remove("latency_monitor.py")

if __name__ == '__main__':
    setLogLevel('info')
    if os.geteuid() != 0:
        print("Error: This script must be run with sudo.")
        exit(1)
    run_benchmark()
