import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# 1. Remove rows where mdsCPUStart or mdsOPSStart are -1
df_power_filtered = df_power[(df_power["mdsCPUStart"] != -1) & (df_power["mdsOPSStart"] != -1)].copy()

# 2. Create initial clusters based on unique combinations of selected columns
df_knl_stage1 = df_power_filtered[["queue_name", "account", "exit_code", "node_count", "cpus", "node_type"]].drop_duplicates().copy()

# 3. Assign cluster_stage1 ID to each unique combination
df_knl_stage1["cluster_stage1"] = range(len(df_knl_stage1))

# 4. Merge the assigned cluster_stage1 back to the filtered original data
df_knl = df_power_filtered.merge(
    df_knl_stage1,
    on=["queue_name", "account", "exit_code", "node_count", "cpus", "node_type"],
    how="left"
)

# Copy the merged data
df_knl_stage2 = df_knl.copy()

# Select MDS-related numerical features
numerical_columns_stage4 = ["mdsCPUStart", "mdsOPSStart", "mem_kb", "cpu_t", "cpu_percent", "wait_s"]

# Normalize the numerical features
scaler = StandardScaler()
df_knl_stage2[numerical_columns_stage4] = scaler.fit_transform(df_knl_stage2[numerical_columns_stage4])

# List to store clustering results for stage 2
all_stage2_clusters8 = []

# Perform K-Means clustering separately for each cluster_stage1 group
unique_clusters_stage1 = df_knl_stage2["cluster_stage1"].unique()

for cluster_id in unique_clusters_stage1:
    # Filter the data for the current stage1 cluster
    df_subset = df_knl_stage2[df_knl_stage2["cluster_stage1"] == cluster_id].copy()

    num_samples = len(df_subset)
    
    # If not enough samples, skip clustering and assign -1
    if num_samples < 3:
        df_subset["cluster_stage2"] = -1
        all_stage2_clusters8.append(df_subset)
        continue

    # Find the optimal number of clusters using the Elbow method
    max_clusters = min(10, num_samples)
    distortions = []
    cluster_range = range(3, max_clusters + 1)

    for k in cluster_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df_subset[numerical_columns_stage4])
        distortions.append(kmeans.inertia_)

    # Select optimal number of clusters based on the minimum difference
    optimal_clusters = cluster_range[np.argmin(np.diff(distortions))] if len(distortions) > 1 else 2
    optimal_clusters = min(optimal_clusters, num_samples)

    # Perform K-Means clustering with the selected number of clusters
    kmeans_stage2 = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
    clusters_stage2 = kmeans_stage2.fit_predict(df_subset[numerical_columns_stage4])

    # Add cluster results to the subset
    df_subset["cluster_stage2"] = clusters_stage2

    # Store the result
    all_stage2_clusters8.append(df_subset)

# Concatenate all subsets after stage2 clustering
df_knl_stage2 = pd.concat(all_stage2_clusters8, ignore_index=True)

# Combine (cluster_stage1, cluster_stage2) into a single combined_cluster
df_knl_stage2["combined_cluster"] = df_knl_stage2["cluster_stage1"].astype(str) + "_" + df_knl_stage2["cluster_stage2"].astype(str)

# Save df_knl_stage2 to a pickle file
df_knl_stage2.to_pickle("./clustered_data.pkl")