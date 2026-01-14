#!/bin/bash

# Exit on any error
set -e

echo "Updating package lists..."
sudo apt-get update

echo "Installing eBPF/XDP dependencies..."
sudo apt-get install -y \
    bpfcc-tools \
    linux-headers-$(uname -r) \
    clang \
    llvm \
    python3-bpfcc

echo "Installation complete."
