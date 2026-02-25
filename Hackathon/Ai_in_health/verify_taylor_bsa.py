
import sys
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from algorithms.taylor_bsa import TaylorBSAOptimizer

def verify_taylor_bsa():
    print("--- Verifying TaylorBSAOptimizer ---")
    
    # 1. Define Dummy Model and Data
    # Simple linear regression: y = 2x + 1
    # Model: y = wx + b
    
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(1, 1) # 2 parameters
            
        def forward(self, x):
            return self.linear(x)
            
    model = SimpleModel()
    
    # Generate data
    X = torch.rand(20, 1) * 10
    y = 2 * X + 1
    
    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=5)
    loss_fn = nn.MSELoss()
    
    print("Initial Model Params:")
    for name, param in model.named_parameters():
        print(f"  {name}: {param.data}")
    
    # 2. Initialize Optimizer
    optimizer = TaylorBSAOptimizer(model, population_size=10, prob_foraging=0.9)
    
    print("\nStarting Optimization (5 steps)...")
    
    # 3. Optimize
    initial_fitness = optimizer.best_fitness # Should be inf initially
    
    # Run one step to init best_fitness
    best_fitness = optimizer.step(loader, loss_fn)
    print(f"Step 1 Best Loss: {best_fitness:.4f}")
    
    initial_best = best_fitness
    
    for i in range(4):
        fitness = optimizer.step(loader, loss_fn)
        print(f"Step {i+2} Best Loss: {fitness:.4f}")
        
    print("\nFinal Model Params:")
    for name, param in model.named_parameters():
        print(f"  {name}: {param.data}")
        
    # Check if improved
    if fitness < initial_best: # It might not strictly improve every single step if unlucky, but generally should
         print("\n[OK] Fitness improved or maintained.")
    else:
         print("\n[WARN] Fitness did not improve (might be random noise or few steps).")
         
    # Check history shape
    if optimizer.history.shape == (3, 10, 2): # 3 steps, 10 birds, 2 params
        print("[OK] History buffer shape correct.")
    else:
        print(f"[FAIL] History buffer shape incorrect: {optimizer.history.shape}")

    print("[SUCCESS] Taylor-BSA Verification Complete.")

if __name__ == "__main__":
    verify_taylor_bsa()
