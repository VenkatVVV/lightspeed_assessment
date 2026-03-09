import pandas as pd
import os

def load_data(file_path):
    """
    Loads data from a CSV file into a Pandas DataFrame.
    Includes error handling for missing files.
    """
    if not os.path.exists(file_path):
        print(f"Warning: File not found at {file_path}. Returning empty DataFrame.")
        return pd.DataFrame()
    
    print(f"Loading data from {file_path}...")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()