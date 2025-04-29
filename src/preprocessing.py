import sqlite3
import pandas as pd
import numpy as np
import ast
from parse_float_list import parse_float_list
from normalize_power import normalize_power

# Connect to database and load the table
conn = sqlite3.connect('./your_db.db')
query = "SELECT * FROM your_table"
df = pd.read_sql(query, conn)
conn.close()

# Convert time-related columns to datetime format
df['start_time'] = pd.to_datetime(df['start_time'])
df['submit_time'] = pd.to_datetime(df['submit_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Compute average power consumption from comma-separated list
df["power_consumption_avg"] = df["power_consumption_cal"].astype(str).apply(
    lambda x: sum(map(float, x.split(','))) / len(x.split(',')) 
    if x and ',' in x else float(x) 
    if x.replace('.', '', 1).isdigit() else None
)

# Convert node list strings to Python lists and count number of nodes
df["nodes"] = df["nodes"].apply(ast.literal_eval)
df["node_count"] = df["nodes"].apply(len)

# Convert selected columns to string type (for formatting or joining)
columns_to_convert = [
    "start_year", "start_month", "start_day", "start_min", 
    "end_year", "end_month", "end_day", "end_min"
]
df[columns_to_convert] = df[columns_to_convert].astype(str)

# Parse power_consumption_cal into list of floats
df["power_consumption_cal"] = df["power_consumption_cal"].astype(str).apply(parse_float_list)

# Normalize power by node count
df["normalized_power"] = df.apply(normalize_power, axis=1)

# Select numeric features, excluding 'exit_code'
numeric_features = df.select_dtypes(include=["number"]).columns.tolist()
numeric_features = [col for col in numeric_features if col != "exit_code"]

# Filter out rows with zero power consumption and rows with -1 in numeric columns
df_filtered = df[
    (df["power_consumption_avg"] != 0) & 
    (~df[numeric_features].eq(-1).any(axis=1))
]

# Compute per-row mean of normalized power (excluding NaNs)
df_filtered['power_mean'] = df_filtered['normalized_power'].apply(
    lambda x: np.nanmean(np.array(x)) if isinstance(x, list) else np.nan
)

# Save processed DataFrame to a pickle file
df_filtered.to_pickle("./processed_data.pkl")
