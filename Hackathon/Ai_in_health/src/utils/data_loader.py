
import os
import requests
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class HeartDiseaseDataLoader:
    """
    Robust data loader for the Cleveland Heart Disease dataset.
    Handles downloading, cleaning, normalizing, and creating PyTorch DataLoaders.
    """

    DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    COLUMN_NAMES = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]

    def __init__(self, data_dir="data/raw"):
        """
        Initialize the data loader.
        
        Args:
           data_dir (str): Directory to save/load the raw data.
        """
        self.data_dir = data_dir
        self.data_path = os.path.join(data_dir, "processed.cleveland.data")
        self.df = None
        self.train_loader = None
        self.test_loader = None
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

    def download_data(self):
        """
        Downloads data from UCI repository. Falls back to local file if download fails.
        """
        if os.path.exists(self.data_path):
            print(f"[INFO] Data found locally at {self.data_path}")
            return

        print(f"[INFO] Downloading data from {self.DATA_URL}...")
        try:
            response = requests.get(self.DATA_URL, timeout=10)
            response.raise_for_status()
            with open(self.data_path, 'wb') as f:
                f.write(response.content)
            print("[INFO] Download successful.")
        except requests.RequestException as e:
            print(f"[ERROR] Download failed: {e}")
            print("[WARN] Checking if file exists locally as fallback...")
            if not os.path.exists(self.data_path):
                 raise FileNotFoundError(f"Data not found at {self.data_path} and download failed.")

    def load_data(self):
        """
        Loads the data into a Pandas DataFrame and assigns column names.
        """
        self.download_data()
        try:
            self.df = pd.read_csv(self.data_path, names=self.COLUMN_NAMES, na_values="?")
            print(f"[INFO] Data loaded. Shape: {self.df.shape}")
        except Exception as e:
            raise RuntimeError(f"Failed to load data from {self.data_path}: {e}")

    def clean_data(self):
        """
        Cleans the dataset:
        - Replaces '?' with NaN (handled by read_csv na_values, but good to ensure).
        - Imputes missing 'ca' and 'thal' with mode.
        - Imputes other missing continuous values with mean.
        - Binarizes the target column (Disease: 1, No Disease: 0).
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Impute missing values
        # ca and thal are categorical/discrete, use mode
        for col in ['ca', 'thal']:
            if self.df[col].isnull().any():
                # mode_val = self.df[col].mode()[0]
                # self.df[col] = self.df[col].fillna(mode_val)
                mode_val = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(mode_val)
        
        # Continuous/others use mean
        for col in self.df.columns:
             if self.df[col].isnull().any():
                 mean_val = self.df[col].mean()
                 self.df[col] = self.df[col].fillna(mean_val)

        # Binarize target
        # Target: 0 = no disease, 1,2,3,4 = degree of disease. 
        # Requirement: > 0 becomes 1.
        self.df['target'] = self.df['target'].apply(lambda x: 1 if x > 0 else 0)

        # Ensure all types are float32 for PyTorch compatibility
        self.df = self.df.astype('float32')
        
        print("[INFO] Data cleaned and imputed.")

    def normalize_features(self):
        """
        Normalizes feature columns using StandardScaler.
        Target column is excluded.
        """
        if self.df is None:
             raise ValueError("Data not loaded. Call load_data() first.")
        
        features = self.df.columns.drop('target')
        scaler = StandardScaler()
        self.df[features] = scaler.fit_transform(self.df[features])
        print("[INFO] Features normalized.")

    def get_loaders(self, batch_size=32, split_ratio=0.8):
        """
        Splits data into train/test sets and returns PyTorch DataLoaders.
        
        Args:
            batch_size (int): Batch size for the loader.
            split_ratio (float): Ratio of training data.
            
        Returns:
            train_loader (DataLoader), test_loader (DataLoader)
        """
        if self.df is None:
             raise ValueError("Data not loaded. Call load_data() first.")

        X = self.df.drop('target', axis=1).values
        y = self.df['target'].values

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=split_ratio, random_state=42, stratify=y
        )

        # Convert to Tensors
        X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1) # [Batch, 1]
        
        X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

        # Create DataSets
        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

        # Create Loaders
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        print(f"[INFO] DataLoaders created. Train size: {len(X_train)}, Test size: {len(X_test)}")
        return self.train_loader, self.test_loader

if __name__ == "__main__":
    # Simple manual test when running this file directly
    loader = HeartDiseaseDataLoader()
    loader.load_data()
    loader.clean_data()
    loader.normalize_features()
    train_loader, test_loader = loader.get_loaders()
    
    data, target = next(iter(train_loader))
    print(f"Batch Shape: Data={data.shape}, Target={target.shape}")
