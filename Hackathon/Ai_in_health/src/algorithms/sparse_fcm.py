
import numpy as np

class SparseFCM:
    """
    Sparse Fuzzy C-Means (SparseFCM) Algorithm.
    
    This implementation incorporates feature weighting to perform simultaneous
    clustering and feature selection. Features with high intra-cluster variance
    (high dispersion) are down-weighted, and soft-thresholding is applied to
    encourage sparsity.
    """

    def __init__(self, n_clusters=2, m=2.0, epsilon=1e-5, max_iter=100, lambda_reg=0.1):
        """
        Initialize SparseFCM hyperparameters.
        
        Args:
            n_clusters (int): Number of clusters (c).
            m (float): Fuzziness parameter (usually > 1).
            epsilon (float): Convergence threshold.
            max_iter (int): Maximum number of iterations.
            lambda_reg (float): Regularization parameter for soft-thresholding weights.
        """
        self.n_clusters = n_clusters
        self.m = m
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.lambda_reg = lambda_reg
        
        # State
        self.u = None      # Membership matrix (N, n_clusters)
        self.v = None      # Cluster centers (n_clusters, D)
        self.w = None      # Feature weights (D,)
        self.trained = False

    def fit(self, X):
        """
        Train the SparseFCM model on data X.
        
        Args:
            X (np.ndarray): Input data of shape (N, D).
        """
        X = np.asarray(X)
        N, D = X.shape
        
        # 1. Initialize U randomly, row-normalized
        np.random.seed(42) # For reproducibility
        self.u = np.random.rand(N, self.n_clusters)
        self.u = self.u / self.u.sum(axis=1, keepdims=True)
        
        # 2. Initialize W uniformly
        self.w = np.ones(D) / D
        
        self.v = np.zeros((self.n_clusters, D))
        
        for iteration in range(self.max_iter):
            u_old = self.u.copy()
            
            # --- Step A: Update Centers (V) ---
            # v_j = (sum(u_ij^m * x_i)) / (sum(u_ij^m))
            # Shape: (C, D)
            um = self.u ** self.m  # (N, C)
            
            # Numerator: (C, N) @ (N, D) -> (C, D)
            # Denominator: (C, 1) through summation
            numerator = um.T @ X
            denominator = um.sum(axis=0, keepdims=True).T + 1e-10 # Avoid div-by-zero
            
            self.v = numerator / denominator
            
            # --- Step B: Update Weights (W) ---
            # Only used for logic that requires feature weighting. 
            # Calculate Dispersion R_k for each feature k.
            # R_k = sum_i sum_j (u_ij^m * (x_ik - v_jk)^2)
            
            # (N, C, D) = (N, 1, D) - (1, C, D)
            diff = X[:, np.newaxis, :] - self.v[np.newaxis, :, :] 
            dist_sq = diff ** 2 # (N, C, D)
            
            # Weighted sum over N and C
            # (N, C, 1) * (N, C, D) -> (N, C, D) --sum--> (D,)
            R = (um[:, :, np.newaxis] * dist_sq).sum(axis=(0, 1))
            
            # Inverse dispersion logic: 
            # We want w_k to be high if R_k is low.
            # Define raw importance p_k = 1 / (R_k + small_epsilon)
            p = 1.0 / (R + 1e-10)
            
            # Soft-thresholding
            # w_k = max(0, p_k - lambda)
            w_unnormalized = np.maximum(0, p - self.lambda_reg)
            
            if w_unnormalized.sum() == 0:
                # Fallback to uniform if all are thresholded to 0
                self.w = np.ones(D) / D
            else:
                self.w = w_unnormalized / w_unnormalized.sum()
                
            # --- Step C: Update Membership (U) ---
            # u_ij = 1 / sum_k ( (d_ij / d_ik)^(2/(m-1)) )
            # d_ij^2 = sum_dim ( w_dim * (x - v)^2 )
            
            # Re-calculate distances with new V and new W
            # dist_sq (N, C, D) already computed, but V changed? 
            # Actually, standard FCM iterates steps. V was updated in Step A.
            # So we use the new V to compute distances.
            
            # Note: We should technically update V using new W? 
            # Standard FCM updates V independent of W if metric is Euclidean, 
            # but for weighted distance, V update technically depends on W if W is matrix? 
            # If W is diagonal (vector), V formula remains standard weighted average 
            # because W factors out in the derivative dJ/dV = 0?
            # Yes, d/dv ( w * (x-v)^2 ) = 2w(x-v). 
            # sum u^m * w * (x-v) = 0 => v = sum(u^m w x) / sum(u^m w).
            # If w is constant for all clusters, it cancels out! 
            # So V update formula is correct as is.
            
            # Recalculate diff with NEW V (updated in Step A)
            diff = X[:, np.newaxis, :] - self.v[np.newaxis, :, :]
            dist_sq_component = diff ** 2  # (N, C, D)
            
            # Weighted Squared Euclidean Distance
            # Sum over D: (N, C, D) * (D,) -> (N, C)
            d_sq = (dist_sq_component * self.w).sum(axis=2)
            
            # Avoid zero distances (implies point is exactly at center)
            d_sq = np.maximum(d_sq, 1e-10)
            
            # Formula: u_ik = ( sum_j (d_ik^2 / d_ij^2) ^ (1/(m-1)) ) ^ -1
            #        = ( d_ik^2 ^ (1/(m-1)) * sum_j (1 / d_ij^2)^(1/(m-1)) ) ^ -1 ? NO.
            
            # Simpler: u_ik = 1 / sum_j ( (d_ik / d_ij) ^ (2/(m-1)) )
            # Let power p = 2 / (m - 1) implies distance, not squared distance in base.
            # Using squared distance D2: u_ik = 1 / sum_j ( (D2_ik / D2_ij) ^ (1/(m-1)) )
            
            exponent = 1.0 / (self.m - 1)
            
            # (N, C, 1) / (N, 1, C) -> (N, C, C) pairwise ratios for the sum?
            # Or just broadcast: 
            # d_sq shape (N, C).
            # We need for each i, k: sum_j (d_sq[i,k] / d_sq[i,j]) ** exponent
            
            # Expand d_sq to (N, C, 1) and (N, 1, C)
            # (d_ik / d_ij)
            ratio = d_sq[:, :, np.newaxis] / d_sq[:, np.newaxis, :] # (N, C, C)
            
            ratio_power = ratio ** exponent
            sum_ratios = ratio_power.sum(axis=2) # Sum over j -> (N, C)
            
            self.u = 1.0 / sum_ratios
            
            # --- Check Convergence ---
            u_diff = np.linalg.norm(self.u - u_old)
            if u_diff < self.epsilon:
                break
                
        self.trained = True

    def predict(self, X):
        """
        Predict cluster membership for new data X.
        
        Args:
            X (np.ndarray): shape (N, D)
            
        Returns:
            np.ndarray: Predicted cluster indices shape (N,)
        """
        if not self.trained:
            raise RuntimeError("Model needed to be trained before prediction.")
            
        X = np.asarray(X)
        N, D = X.shape
        
        # Calculate Weighted Distances to Centers
        # (N, 1, D) - (1, C, D)
        diff = X[:, np.newaxis, :] - self.v[np.newaxis, :, :]
        dist_sq_component = diff ** 2
        d_sq = (dist_sq_component * self.w).sum(axis=2)
        
        return np.argmin(d_sq, axis=1)

    def get_selected_features(self, threshold=0.01):
        """
        Return indices of features with weights > threshold.
        """
        if self.w is None:
            return []
        return np.where(self.w > threshold)[0]
