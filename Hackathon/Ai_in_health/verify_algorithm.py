
import sys
import os
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from algorithms.sparse_fcm import SparseFCM

def verify_sparse_fcm():
    print("--- Verifying SparseFCM Implementation ---")
    
    # 1. Generate Synthetic Data
    # 2 informative features, 3 noise features
    n_samples = 200
    n_features = 5
    n_informative = 2
    centers = 3
    
    X, y = make_blobs(n_samples=n_samples, n_features=n_informative, centers=centers, random_state=42, cluster_std=1.0)
    
    # Add noise features
    np.random.seed(42)
    noise = np.random.normal(0, 10, (n_samples, n_features - n_informative)) # High variance noise
    X_full = np.hstack([X, noise])
    
    # Normalize (important for distance-based methods)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_full)
    
    print(f"Data Shape: {X_scaled.shape} (First {n_informative} features are informative)")
    
    # 2. Train Model
    # Use higher lambda to penalize the high-variance noise features?
    # Actually, high variance noise within cluster -> high R -> low p -> low weight.
    # But wait, noise was normal(0,10), so global variance is high. 
    # If clusters are mixed in noise dimensions, R is high.
    
    model = SparseFCM(n_clusters=centers, m=2.0, max_iter=50, lambda_reg=0.01)
    
    print("\nTraining SparseFCM...")
    try:
        model.fit(X_scaled)
        print("[OK] Training completed without errors.")
    except Exception as e:
        print(f"[FAIL] Training failed: {e}")
        return

    # 3. Check Weights
    print("\nFeature Weights:")
    print(model.w)
    
    # Expect informative features (0, 1) to have higher weights than noise (2, 3, 4)
    # Note: Depending on lambda and data, noise weights might not be exactly zero, 
    # but should be lower if the intra-cluster variance of noise is high.
    # Actually, blobs are separated in dims 0,1. Intra-cluster variance in 0,1 is small (std=1).
    # Noise features have variance 100. Intra-cluster variance will be ~100.
    # So R for noise >> R for informative.
    # So W for noise << W for informative.
    
    informative_weights = model.w[:n_informative]
    noise_weights = model.w[n_informative:]
    
    print(f"\nAvg Informative Weight: {np.mean(informative_weights):.4f}")
    print(f"Avg Noise Weight:       {np.mean(noise_weights):.4f}")
    
    if np.mean(informative_weights) > np.mean(noise_weights):
        print("[OK] Informative features have higher weights.")
    else:
        print("[WARN] Feature weighting might not be working as expected.")

    # 4. Check Selection
    selected = model.get_selected_features(threshold=0.001)
    print(f"\nSelected Features (>0.001): {selected}")

    # 5. Check Prediction
    preds = model.predict(X_scaled)
    print(f"\nPredictions Shape: {preds.shape}")
    print(f"Unique Clusters Found: {np.unique(preds)}")
    
    if len(np.unique(preds)) == centers:
        print("[OK] Correct number of clusters predicted.")
    else:
        print(f"[WARN] Predicted {len(np.unique(preds))} clusters (expected {centers}).")
        
    print("\n[SUCCESS] SparseFCM verification pipeline finished.")

if __name__ == "__main__":
    verify_sparse_fcm()
