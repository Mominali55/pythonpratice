
import sys
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from algorithms.dbn import DBN, RBM

def verify_dbn():
    print("--- Verifying DBN and RBM Implementation ---")
    
    # 1. Setup Data
    # Create simple binary data pattern
    # Pattern 1: [1, 1, 1, 0, 0, 0] -> Class 0
    # Pattern 2: [0, 0, 0, 1, 1, 1] -> Class 1
    
    data = []
    labels = []
    for _ in range(50):
        data.append([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        labels.append(0)
        data.append([0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
        labels.append(1)
        
    X = torch.tensor(data, dtype=torch.float32) # (100, 6)
    y = torch.tensor(labels, dtype=torch.long)
    
    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=10, shuffle=True)
    
    print(f"Data Shape: {X.shape}")
    
    # 2. Initialize DBN
    # Input: 6, Hidden: [4, 2], and Head -> 2 classes
    dbn = DBN(input_dim=6, hidden_dims=[4, 2], output_dim=2, k=1)
    
    print("\n[INFO] DBN Initialized:")
    print(dbn)
    
    # 3. Test Pretraining
    print("\n--- Testing Pretraining ---")
    try:
        dbn.pretrain(loader, epochs=5, lr=0.1)
        print("[OK] Pretraining completed.")
    except Exception as e:
        print(f"[FAIL] Pretraining failed: {e}")
        # import traceback
        # traceback.print_exc()
        return

    # 4. Test Forward Pass
    print("\n--- Testing Forward Pass ---")
    try:
        logits = dbn(X)
        print(f"Output Shape: {logits.shape}")
        if logits.shape == (100, 2):
            print("[OK] Output shape correct.")
        else:
            print(f"[FAIL] Incorrect output shape: {logits.shape}")
            
        # Check if gradients flow (just to verify nn.Module compatibility)
        loss_fn = nn.CrossEntropyLoss()
        loss = loss_fn(logits, y)
        loss.backward()
        
        # Check if RBM weights have grad
        if dbn.rbm_layers[0].W.grad is not None:
             print("[OK] Gradients computed for RBM weights (compatible with fine-tuning).")
        else:
             print("[FAIL] No gradients for RBM weights.")
             
    except Exception as e:
         print(f"[FAIL] Forward pass failed: {e}")
         return
         
    print("\n[SUCCESS] DBN verification complete.")

if __name__ == "__main__":
    verify_dbn()
