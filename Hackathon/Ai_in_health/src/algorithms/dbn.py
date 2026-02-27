
import torch
import torch.nn as nn
import torch.nn.functional as F

class RBM(nn.Module):
    """
    Restricted Boltzmann Machine (RBM) implementation.
    """
    def __init__(self, visible_units, hidden_units, k=1):
        """
        Initialize RBM parameters.
        
        Args:
            visible_units (int): Number of visible units.
            hidden_units (int): Number of hidden units.
            k (int): Number of Contrastive Divergence (CD) steps.
        """
        super(RBM, self).__init__()
        self.visible_units = visible_units
        self.hidden_units = hidden_units
        self.k = k
        
        # Initialize weights and biases
        # Weights: (hidden, visible) or (visible, hidden)?
        # Usually W is (visible, hidden) in literature, but nn.Linear uses (out, in).
        # Let's use shape (visible, hidden) explicitly as requested for manual updates?
        # Prompt said "Initialize weights W". Let's use nn.Parameter to ensure it registers.
        # Let's use shape (visible_units, hidden_units) for W.
        
        self.W = nn.Parameter(torch.randn(visible_units, hidden_units) * 0.01)
        self.visible_bias = nn.Parameter(torch.zeros(visible_units))
        self.hidden_bias = nn.Parameter(torch.zeros(hidden_units))

    def forward(self, v):
        """
        Returns hidden probabilities given visible state v.
        p(h=1|v) = sigmoid(v @ W + b_h)
        """
        return torch.sigmoid(torch.matmul(v, self.W) + self.hidden_bias)

    def sample_hidden(self, v):
        """
        Returns hidden probabilities and sampled binary states.
        """
        h_prob = self.forward(v)
        h_sample = torch.bernoulli(h_prob)
        return h_prob, h_sample

    def sample_visible(self, h):
        """
        Returns reconstruction probabilities and samples given hidden state h.
        p(v=1|h) = sigmoid(h @ W.T + b_v)
        """
        v_prob = torch.sigmoid(torch.matmul(h, self.W.t()) + self.visible_bias)
        v_sample = torch.bernoulli(v_prob)
        return v_prob, v_sample

    def contrastive_divergence(self, input_data):
        """
        Perform one step of Gibbs sampling (CD-k) and return positive and negative associations.
        
        Args:
            input_data (Tensor): Batch of visible units (Batch, Visible).
            
        Returns:
            pos_association: v0.T @ p(h0|v0)
            neg_association: vk.T @ p(hk|vk)
            ... wait, for batch, we return the expectation over batch?
            Or return the batch of associations to sum later?
            Usually we compute gradients based on <vh>_data - <vh>_model.
            The prompt asks for "positive and negative phase associations for weight updates".
            Let's return the components needed to compute the update: 
            pos_assoc = v0.t() @ h0_prob (or h0_sample?)
            neg_assoc = vk.t() @ hk_prob
            
            Actually, typical CD uses h0_prob for positive phase and hk_prob for negative phase.
        """
        # Positive Phase with v0
        v0 = input_data
        h0_prob, h0_sample = self.sample_hidden(v0)
        
        # We need positive association: v0_T * h0_prob
        # For batch: torch.matmul(v0.T, h0_prob)
        pos_association = torch.matmul(v0.t(), h0_prob)
        
        # Negative Phase (Gibbs Sampling k steps)
        vk = v0
        hk = h0_sample # Start chain from sampled hidden
        
        for _ in range(self.k):
            # h -> v
            vk_prob, vk_sample = self.sample_visible(hk)
            vk = vk_sample # Update visible
            
            # v -> h
            hk_prob, hk_sample = self.sample_hidden(vk)
            hk = hk_sample # Update hidden
            
        # Technically negative association uses the probability of hidden at step k given visible at step k?
        # Or sample? Hinton's guide says use probabilities for the negative phase to reduce variance.
        neg_association = torch.matmul(vk.t(), hk_prob)
        
        return pos_association, neg_association, v0, vk

class DBN(nn.Module):
    """
    Deep Belief Network (DBN) constructed by stacking RBMs.
    """
    def __init__(self, input_dim, hidden_dims, output_dim=2, k=1):
        """
        Args:
            input_dim (int): Dimension of input data.
            hidden_dims (list of int): Dimensions of hidden layers for RBMs.
            output_dim (int): Number of classes for final classification.
            k (int): CD steps.
        """
        super(DBN, self).__init__()
        self.rbm_layers = nn.ModuleList()
        self.hidden_dims = hidden_dims
        
        # Create RBM layers
        prev_dim = input_dim
        for h_dim in hidden_dims:
            self.rbm_layers.append(RBM(prev_dim, h_dim, k=k))
            prev_dim = h_dim
            
        # Classification Head
        self.classifier = nn.Linear(prev_dim, output_dim)

    def pretrain(self, train_loader, epochs=10, lr=0.01):
        """
        Greedy layer-wise pretraining using Contrastive Divergence.
        Updates weights in-place without autograd.
        
        Args:
            train_loader (DataLoader): Training data.
            epochs (int): Number of epochs per layer.
            lr (float): Learning rate.
        """
        # We need to act on the full dataset or iterate through batches.
        # Since we have a loader, we iterate.
        # For layer i > 0, the input is the output probabilities(or samples) of layer i-1.
        
        # We cannot easily re-run the loader for inner layers if we transform on the fly every epoch?
        # Standard approach:
        # Train Layer 0 on raw data.
        # Generate dataset for Layer 1 by passing Layer 0 data through trained Layer 0.
        # Train Layer 1...
        # But if dataset is large, we might just run forward pass on the fly?
        # "Train RBM[i] using the input data (or output of RBM[i-1])"
        
        # Let's simplify: For each RBM layer...
        
        current_dataset_loader = train_loader
        
        for i, rbm in enumerate(self.rbm_layers):
            print(f"[INFO] Pretraining RBM Layer {i+1}/{len(self.rbm_layers)}")
            
            for epoch in range(epochs):
                total_error = 0
                for batch_idx, (data, _) in enumerate(current_dataset_loader):
                    # Data preparation
                    # If this is the first layer, data is raw input.
                    # If i > 0, we need to ensure we are receiving the transformed data?
                    # Ah, if we iterate layers sequentially, we need to transform the whole dataset first?
                    # Or we just do: when training RBM i, we verify that `train_loader` produces data for RBM i?
                    # The `train_loader` passed in is for the INPUT data. 
                    # If i > 0, we must effectively transform the data through previous layers on the fly in the loop.
                    
                    # Flatten input if needed (usually RBMs take flat vectors)
                    if i == 0:
                        v = data.view(data.size(0), -1)
                    else:
                        # We need to pass data through previous 'i' layers to get input for this layer.
                        # This is expensive re-computation every batch/epoch. 
                        # Better to transform dataset once if memory allows. 
                        # But user prompt implies just a function. Let's do on-the-fly for simplicity/memory safety.
                        with torch.no_grad():
                            v = data.view(data.size(0), -1)
                            for prev_rbm in self.rbm_layers[:i]:
                                v, _ = prev_rbm.sample_hidden(v) # Use samples or probs? usually probs for next layer input
                                # Hinton guide: "The hidden probabilities... are used as the data for training the next RBM" (Section 11)
                                # Wait, sample_hidden returns (prob, sample). Use prob?
                                # Actually, usually we use Sampled binary states as input to next layer?
                                # Hinton "A Practical Guide to Training RBMs": 
                                # "It is usually better to use the probabilities... as the data for the next RBM"
                                # Let's use the probability form for the 'input' to the next layer. v = h_prob
                                pass

                    # Now 'v' is the input for current 'rbm'
                    pos_assoc, neg_assoc, v0, vk = rbm.contrastive_divergence(v)
                    
                    # Update weights (In-place, no autograd)
                    # W_new = W_old + lr * (pos_assoc - neg_assoc) / batch_size
                    batch_size = v.size(0)
                    update_w = (pos_assoc - neg_assoc) / batch_size
                    update_vb = torch.sum(v0 - vk, dim=0) / batch_size
                    
                    # Usually hidden bias update depends on positive phase hidden prob and negative phase hidden prob?
                    # d/db_h = <h>_data - <h>_model
                    # We have h0_prob (from sample_hidden(v0)) ... wait, CD returns associations. 
                    # Let's recalculate or adapt CD method to return needed stats for biases too.
                    # RBM.contrastive_divergence returns v0, vk.
                    # We can get h0_prob = sigmoid(v0 W + b) and hk_prob = sigmoid(vk W + b).
                    
                    h0_prob = rbm.forward(v0)
                    hk_prob = rbm.forward(vk)
                    update_hb = torch.sum(h0_prob - hk_prob, dim=0) / batch_size
                    
                    with torch.no_grad():
                        rbm.W += lr * update_w
                        rbm.visible_bias += lr * update_vb
                        rbm.hidden_bias += lr * update_hb
                    
                    # Reconstruction error for monitoring
                    error = torch.mean(torch.sum((v0 - vk)**2, dim=1))
                    total_error += error.item()
                
                print(f"  Epoch {epoch+1}: Reconstruction Error = {total_error / len(train_loader):.4f}")

    def forward(self, x):
        """
        Forward pass through the entire DBN.
        
        Args:
            x (Tensor): Input data.
            
        Returns:
            Tensor: Class logits.
        """
        x = x.view(x.size(0), -1)
        
        # Pass through RBM layers
        for rbm in self.rbm_layers:
            # Deterministic forward pass usually uses probabilities
            x = rbm.forward(x)
        
        # Pass through classifier
        output = self.classifier(x)
        return output
