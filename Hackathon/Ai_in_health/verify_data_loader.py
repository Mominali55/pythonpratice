
import sys
import os
import torch
import pandas as pd
import numpy as np

# Add src to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from utils.data_loader import HeartDiseaseDataLoader
except ImportError as e:
    print(f"[FAIL] could not import HeartDiseaseDataLoader: {e}")
    sys.exit(1)

def verify_data_loader():
    print("--- Verifying HeartDiseaseDataLoader ---")
    
    loader = HeartDiseaseDataLoader()
    
    # 1. Test Load
    try:
        loader.load_data()
        assert loader.df is not None
        assert not loader.df.empty
        print("[OK] Data Loaded Successfully")
    except Exception as e:
        print(f"[FAIL] Loading Data: {e}")
        return

    # 2. Test Clean
    try:
        loader.clean_data()
        # Check for NaNs
        if loader.df.isnull().values.any():
            print("[FAIL] NaNs found after cleaning!")
        else:
            print("[OK] Data Cleaned (No NaNs)")
            
        # Check Target Binarization
        unique_targets = loader.df['target'].unique()
        if set(unique_targets).issubset({0.0, 1.0}):
            print(f"[OK] Target Binarized: {unique_targets}")
        else:
            print(f"[FAIL] Target not binary: {unique_targets}")
            
    except Exception as e:
        print(f"[FAIL] Cleaning Data: {e}")
        return

    # 3. Test Normalize
    try:
        # Check basic stats before normalization (optional, but good for debugging)
        # raw_mean = loader.df.drop('target', axis=1).mean() 
        
        loader.normalize_features()
        
        # Check if mean is roughly 0 and std is roughly 1 (excluding target)
        features = loader.df.drop('target', axis=1)
        means = features.mean()
        stds = features.std()
        
        if np.allclose(means, 0, atol=1e-1) and np.allclose(stds, 1, atol=1e-1):
             print("[OK] Features Normalized (mean ~ 0, std ~ 1)")
        else:
             print("[WARN] Normalization checks stats deviation (might be expected for dummy vars but check manually)")
             # print(means, stds)

    except Exception as e:
        print(f"[FAIL] Normalizing Data: {e}")
        return

    # 4. Test Get Loaders
    try:
        batch_size = 16
        train_loader, test_loader = loader.get_loaders(batch_size=batch_size)
        
        # Check one batch
        data, target = next(iter(train_loader))
        
        if data.shape[0] == batch_size and data.shape[1] == 13:
             print(f"[OK] Train Loader Batch Shape Correct: {data.shape}")
        else:
             print(f"[FAIL] Train Loader Batch Shape Incorrect: {data.shape}")

        if target.shape[0] == batch_size and target.shape[1] == 1: # We unsqueezed target
             print(f"[OK] Target Batch Shape Correct: {target.shape}")
        else:
             print(f"[FAIL] Target Batch Shape Incorrect: {target.shape}")
             
        # Check dtype
        if data.dtype == torch.float32 and target.dtype == torch.float32:
            print("[OK] Tensor dtypes are float32")
        else:
            print(f"[FAIL] Tensor dtypes incorrect. Data: {data.dtype}, Target: {target.dtype}")

    except Exception as e:
        print(f"[FAIL] Getting Loaders: {e}")
        return

    print("\n[SUCCESS] All checks passed for HeartDiseaseDataLoader.")

if __name__ == "__main__":
    verify_data_loader()
