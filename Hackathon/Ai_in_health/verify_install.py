import sys
import importlib

def check_library(name):
    try:
        lib = importlib.import_module(name)
        version = getattr(lib, '__version__', 'Unknown')
        print(f"[OK] {name:<15} : {version}")
        return lib
    except ImportError:
        print(f"[FAIL] {name:<13} : Not installed")
        return None

def main():
    print("--- Environment Verification ---\n")
    
    # Check Python version
    print(f"Python Version: {sys.version.split()[0]}")
    
    # Check Key Libraries
    libraries = [
        'numpy', 'pandas', 'scipy', 'sklearn', 
        'matplotlib', 'seaborn', 'tqdm', 'requests', 'torch'
    ]
    
    libs = {}
    for lib_name in libraries:
        libs[lib_name] = check_library(lib_name)
        
    # Check PyTorch & CUDA
    torch_lib = libs['torch']
    if torch_lib:
        print("\n--- PyTorch & Compute ---")
        cuda_available = torch_lib.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        
        if cuda_available:
            print(f"CUDA Version: {torch_lib.version.cuda}")
            device_count = torch_lib.cuda.device_count()
            print(f"GPU Count: {device_count}")
            for i in range(device_count):
                print(f"  GPU {i}: {torch_lib.cuda.get_device_name(i)}")
                
            try:
                x = torch_lib.rand(5, 3).cuda()
                print(f"\n[OK] Tensor allocation on GPU successful: {x.shape}")
            except Exception as e:
                print(f"\n[FAIL] Tensor allocation on GPU failed: {e}")
        else:
            print("Running on CPU.")
            try:
                x = torch_lib.rand(5, 3)
                print(f"\n[OK] Tensor allocation on CPU successful: {x.shape}")
            except Exception as e:
                 print(f"\n[FAIL] Tensor allocation on CPU failed: {e}")

if __name__ == "__main__":
    main()
