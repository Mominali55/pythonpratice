#!/usr/bin/env python3
from bcc import BPF
import time
import sys
import socket
import struct
import joblib
import pandas as pd
import random
import os

# 1. Load the mitigation.c source code
device = "lo"
flags = 0

print(f"Loading XDP program mitigation.c...")
b = BPF(src_file="mitigation.c")
fn = b.load_func("xdp_filter", BPF.XDP)

# 2. Attach the xdp_filter function to the loopback interface (lo)
print(f"Attaching XDP program to {device}...")
b.attach_xdp(device, fn, flags)

blocklist = b.get_table("blocklist")

# Load ML Model
model_path = 'ddos_model.joblib'
if os.path.exists(model_path):
    print(f"Loading ML model from {model_path}...")
    model = joblib.load(model_path)
else:
    print(f"Warning: {model_path} not found. ML features disabled.")
    model = None

# 3. Helper function to block an IP
def block_ip(ip_str):
    try:
        ip_int = struct.unpack("I", socket.inet_aton(ip_str))[0]
        # ipv4 addresses in blocklist are keys (u32), value is drop count (u64)
        if ip_int not in blocklist:
            blocklist[b.Key(ip_int)] = b.Leaf(0)
            print(f"Build-in Firewall: Blocked IP: {ip_str}")
    except socket.error:
        print(f"Invalid IP address: {ip_str}")

def analyze_traffic():
    if model is None:
        return

    # Simulate extracting flow features (using random values for now)
    # Features: 'Flow Duration', 'Total Fwd Packets', 'Flow IAT Mean', 'Fwd Packet Length Std'
    features = {
        'Flow Duration': random.uniform(100, 100000),
        'Total Fwd Packets': random.randint(1, 100),
        'Flow IAT Mean': random.uniform(0, 5000),
        'Fwd Packet Length Std': random.uniform(0, 1500)
    }
    
    # Create DataFrame to match model input
    df = pd.DataFrame([features])
    
    # Predict
    prediction = model.predict(df)[0]
    
    # If prediction is 'Attack' (not 'Benign')
    if prediction != 'Benign':
        print(f"[ALERT] DDoS Attack Detected! Class: {prediction}")
        # Simulate an attacker IP
        attacker_ip = "10.0.0.2"
        print(f"Blocking malicious source: {attacker_ip}")
        block_ip(attacker_ip)
    else:
        # print("Traffic is Benign.")
        pass

# 4. Monitor function
def monitor():
    print("Monitoring dropped packets and analyzing traffic... Press Ctrl+C to stop.")
    while True:
        try:
            # Run ML analysis
            analyze_traffic()

            # Print stats
            total_drops = 0
            for k, v in blocklist.items():
                total_drops += v.value
            
            # Only print if there are drops to avoid console spam, or print status periodically
            if total_drops > 0:
                print(f"Total dropped packets: {total_drops}")
            
            time.sleep(2)
        except KeyboardInterrupt:
            break

# 5. Handle KeyboardInterrupt to detach
try:
    monitor()
except KeyboardInterrupt:
    pass
finally:
    print(f"\nDetaching XDP program from {device}...")
    b.remove_xdp(device, flags)
    print("Detached successfully.")
