#!/usr/bin/env python3
from bcc import BPF
import time
import sys
import socket
import struct

# Default interface
device = "lo"
flags = 0

if len(sys.argv) > 1:
    device = sys.argv[1]

print(f"Loading XDP program mitigation.c on {device}...")
b = BPF(src_file="mitigation.c")
fn = b.load_func("xdp_filter", BPF.XDP)

print(f"Attaching to {device}...")
b.attach_xdp(device, fn, flags)

blocklist = b.get_table("blocklist")

print("XDP program loaded. Press Ctrl+C to stop.")
print("To block an IP, you can populate the map. (Example included in code comments)")

# Example: Block 1.2.3.4
# ip_to_block = struct.unpack("I", socket.inet_aton("1.2.3.4"))[0]
# blocklist[b.Key(ip_to_block)] = b.Leaf(0)

try:
    while True:
        time.sleep(2)
        print("--- Blocklist Stats ---")
        found = False
        for k, v in blocklist.items():
            print(f"IP {socket.inet_ntoa(struct.pack('I', k.value))}: {v.value} drops")
            found = True
        if not found:
            print("No IPs in blocklist (or no drops yet).")
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    print(f"Detaching from {device}...")
    b.remove_xdp(device, flags)
    print("Detached.")
