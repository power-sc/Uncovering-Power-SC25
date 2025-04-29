import numpy as np
import pandas as pd

def normalize_power(row):
    power_data = row["power_consumption_cal"]
    
    # Check if power_consumption is a list; if not, convert to list
    if not isinstance(power_data, list):
        power_data = [power_data]
    
    # Normalize each value by node_count, keeping NaNs unchanged
    return [float(x) / row["node_count"] if pd.notna(x) else np.nan for x in power_data]
