
import torch
import torch.nn as nn
from torch.nn.utils import parameters_to_vector, vector_to_parameters
import numpy as np

class TaylorBSAOptimizer:
    """
    Taylor-Bird Swarm Algorithm (Taylor-BSA) Optimizer.
    Uses a Taylor series expansion for position updates to enhance exploration/exploitation.
    """
    def __init__(self, model, population_size=20, prob_foraging=0.8, prob_flight=0.1, 
                 low=-1.0, high=1.0, device='cpu'):
        """
        Args:
            model (nn.Module): PyTorch model to optimize.
            population_size (int): Number of birds in the swarm.
            prob_foraging (float): Probability of foraging behavior.
            prob_flight (float): Probability of flight behavior.
            low (float or Tensor): Lower bound for initialization.
            high (float or Tensor): Upper bound for initialization.
            device (str): Device to run optimization on.
        """
        self.model = model
        self.pop_size = population_size
        self.prob_foraging = prob_foraging
        self.prob_flight = prob_flight
        self.device = device
        
        # Flatten parameters
        self.initial_params = parameters_to_vector(self.model.parameters()).detach().to(device)
        self.num_params = self.initial_params.numel()
        
        # Initialize Population
        # Random noise around initial weights or uniform initialization?
        # Prompt: "initialized with random noise around the model's current weights"
        # We'll use uniform noise around the initial weights.
        noise_range = 0.5 # Adjustable
        
        self.population = self.initial_params.unsqueeze(0).repeat(population_size, 1) # (N, D)
        noise = (torch.rand(population_size, self.num_params, device=device) * 2 - 1) * noise_range
        self.population += noise
        
        self.best_solution = self.initial_params.clone()
        self.best_fitness = float('inf')
        
        # History Buffer for Taylor Series
        # We need positions at t-1, t-2, t-3.
        # Initialize history with current position for all time steps initially.
        # Shape: (History_Depth, N, D)
        # Depth=4 (t, t-1, t-2, t-3). t is self.population.
        # We store t-1, t-2, t-3 explicitly.
        self.history = torch.stack([self.population.clone() for _ in range(3)]) # Indices 0->t-1, 1->t-2, 2->t-3
    
    def _evaluate_fitness(self, weights_vector, data_loader, loss_fn):
        """
        Evaluates fitness (loss) for a single weight vector.
        """
        # Load weights into model
        vector_to_parameters(weights_vector, self.model.parameters())
        
        self.model.eval()
        total_loss = 0.0
        with torch.no_grad():
            for data, target in data_loader:
                data, target = data.to(self.device), target.to(self.device)
                
                # Check for DBN forward method signature
                # Standard DBN forward might return logits
                output = self.model(data)
                
                loss = loss_fn(output, target)
                total_loss += loss.item()
        
        return total_loss / len(data_loader)

    def step(self, data_loader, loss_fn):
        """
        Execute one optimization step (epoch).
        
        Args:
            data_loader: Training data.
            loss_fn: Loss function.
            
        Returns:
            best_fitness (float): Best loss achieved so far.
        """
        current_fitnesses = []
        
        # 1. Evaluate Fitness of current population
        for i in range(self.pop_size):
            fitness = self._evaluate_fitness(self.population[i], data_loader, loss_fn)
            current_fitnesses.append(fitness)
            
            # Update Global Best
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = self.population[i].clone()
        
        current_fitnesses = torch.tensor(current_fitnesses, device=self.device)
        
        # 2. Update Positions
        new_population = self.population.clone()
        
        # History references
        # history[0] is t-1, history[1] is t-2, history[2] is t-3
        pos_t_minus_1 = self.history[0]
        pos_t_minus_2 = self.history[1]
        pos_t_minus_3 = self.history[2]
        
        for i in range(self.pop_size):
            r = np.random.rand()
            
            if r < self.prob_foraging:
                # --- Foraging (Taylor Series Update) ---
                # new_pos = 0.5*pos_t + 1.3591*pos_t_minus_1 - 1.359*pos_t_minus_2 + 0.6795*pos_t_minus_3
                # Coefficients from Alhassan (2020)
                update = 0.5 * self.population[i] + \
                         1.3591 * pos_t_minus_1[i] - \
                         1.359 * pos_t_minus_2[i] + \
                         0.6795 * pos_t_minus_3[i]
                         
                new_population[i] = update
                
            else:
                # --- Vigilance or Flight (Standard BSA) ---
                # Standard BSA logic for non-foraging behavior
                # Divide into vigilance and flight
                if np.random.rand() < self.prob_flight:
                    # Flight (Move towards random position or similar)
                    # BSA Flight: x_new = x + randn * x
                    # Or towards random other bird?
                    # Standard BSA Flight equation:
                    # x_new = x + FL * (best - x) ?? No that's PSO-ish.
                    # Simplified Flight: Move towards random position in search space.
                    # Let's use: x_new = x + randn * (best - x) + randn * (x - mean)
                    
                    # We'll use a simplified version: Random step
                    step_size = torch.randn(self.num_params, device=self.device)
                    new_population[i] = self.population[i] + step_size
                else:
                    # Vigilance
                    # Move towards best
                    k = np.random.randint(self.pop_size) # Random other bird
                    while k == i: k = np.random.randint(self.pop_size)
                    
                    # BSA Vigilance equation approximates:
                    # x_new = x + rand * (best - x) + rand * (best - x_k)
                    r1 = torch.rand(self.num_params, device=self.device)
                    r2 = torch.rand(self.num_params, device=self.device)
                    
                    diff_best = self.best_solution - self.population[i]
                    diff_other = self.best_solution - self.population[k]
                    
                    new_population[i] = self.population[i] + r1 * diff_best + r2 * diff_other

        # 3. Update History Buffer
        # Shift history: t-2 -> t-3, t-1 -> t-2, t -> t-1
        self.history[2] = self.history[1].clone()
        self.history[1] = self.history[0].clone()
        self.history[0] = self.population.clone()
        
        # 4. Apply Updates
        self.population = new_population
        
        # Optional: Boundary check? (Not specified, assuming unbounded or regularized by physics)
        
        # 5. Restore best weights to model at end of step (so we leave model in good state)
        vector_to_parameters(self.best_solution, self.model.parameters())
        
        return self.best_fitness
