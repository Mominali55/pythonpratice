#!/bin/bash

ENV_NAME="heart_disease_ai"
REQUIREMENTS_FILE="requirements.txt"

echo "--- Starting Environment Setup for $ENV_NAME ---"

# 1. Create Virtual Environment
if [ -d "$ENV_NAME" ]; then
    echo "Virtual environment '$ENV_NAME' already exists."
else
    echo "Creating virtual environment '$ENV_NAME'..."
    python3 -m venv $ENV_NAME
fi

# 2. Activate Environment and Install Dependencies
echo "Activating environment and installing dependencies..."
source $ENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    # Install torch specifically first if needed or let pip handle it from requirements
    # For this setup, we rely on requirements.txt handling the platform specific logic via indices if necessary,
    # but for simplicity we assume the requirements.txt has the correct index-url if needed.
    # Note: Standard PyTorch wheels from PyPI often come with CUDA.
    
    # We explicitly point to the pytorch-cu118 extra index if we want to ensure cu118 on linux,
    # but standard pip install often works. Let's stick to simple pip install -r.
    # However, to ensure cuda 11.8 specifically, we often need --extra-index-url.
    # The requirements.txt I generated earlier uses the standard names. 
    # To really ensure CUDA 11.8, we generally need specifically hosted wheels.
    # Let's add the command to install torch with the correct index URL for linux.
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Detected Linux. Installing PyTorch with CUDA 11.8 support..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        # Install the rest excluding torch packages if they are already installed, or just install over.
        pip install -r $REQUIREMENTS_FILE
    else
        echo "Non-Linux OS detected. Installing from requirements.txt..."
        pip install -r $REQUIREMENTS_FILE
    fi
else
    echo "Error: $REQUIREMENTS_FILE not found!"
    exit 1
fi

# 3. Create Directory Structure
echo "Creating directory structure..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p src/algorithms
mkdir -p src/utils
mkdir -p notebooks

# Initialize __init__.py for src modules
touch src/__init__.py
touch src/algorithms/__init__.py
touch src/utils/__init__.py

echo "--- Setup Complete ---"
echo "To activate the environment, run: source $ENV_NAME/bin/activate"
echo "To verify installation, run: python verify_install.py"
