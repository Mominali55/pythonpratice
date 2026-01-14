#!/usr/bin/env python3
from bcc import BPF
import time
import sys

# Define the BPF program
bpf_text = """
int hello_xdp(struct xdp_md *ctx) {
    bpf_trace_printk("Hello, XDP!\\n");
    return XDP_PASS;
}
"""

device = "lo"
flags = 0

try:
    print(f"Compiling and loading XDP program...")
    b = BPF(text=bpf_text)
    fn = b.load_func("hello_xdp", BPF.XDP)

    print(f"Attaching XDP program to {device}...")
    b.attach_xdp(device, fn, flags)
    
    print("XDP program loaded successfully!")
    print("Check /sys/kernel/debug/tracing/trace_pipe for output (optional).")
    print("Press Ctrl+C to detach and exit.")

    while True:
        try:
            # Just wait for KeyboardInterrupt
            time.sleep(1)
        except KeyboardInterrupt:
            break

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

finally:
    print(f"\nDetaching XDP program from {device}...")
    try:
        b.remove_xdp(device, flags)
        print("Detached successfully.")
    except Exception as e:
        print(f"Error detaching: {e}")
