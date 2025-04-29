import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Define node label mapping
node_ranges = {
    "node0000~node0999": "Range 0",
    "node1000~node1999": "Range 1",
    "node2000~node2999": "Range 2",
    "node3000~node3999": "Range 3",
    "node4000~node4999": "Range 4",
    "node5000~node5999": "Range 5",
    "node6000~node6999": "Range 6",
    "node7000~node7999": "Range 7",
    "node8000~node8305": "Range 8"
}
valid_queues = ["normal", "long", "flat", "debug"]

# 1. Load and filter data
df_power = pd.read_pickle("processed_data.pkl")
df_knl = df_power[df_power["node_type"] == "knl"]

# Initialize dictionary for storing per-node average power per range and queue type
node_power_means = {key: {"normal": [], "not_normal": []} for key in node_ranges}

# 2. Iterate through rows to populate dictionary
for _, row in df_knl.iterrows():
    start_year_month = f"{int(row['start_year'])}-{int(row['start_month']):02d}"
    nodes = row["nodes"]
    power_mean = row["power_mean"]
    queue_type = "normal" if row["queue_name"] in valid_queues else "not_normal"

    if start_year_month not in node_power_means:
        node_power_means[start_year_month] = {key: {"normal": [], "not_normal": []} for key in node_ranges}

    for node in nodes:
        node_number = int(node.replace("node", ""))
        for range_name in node_ranges:
            range_values = range(int(range_name[4:8]), int(range_name[13:]) + 1)
            if node_number in range_values:
                node_power_means[start_year_month][range_name][queue_type].append(power_mean)
                break

# 3. Compute average power per month per node range
power_mean_results = {
    year_month: {
        key: {
            "normal": np.mean(values["normal"]) if values["normal"] else np.nan,
            "not_normal": np.mean(values["not_normal"]) if values["not_normal"] else np.nan
        } 
        for key, values in node_power_means[year_month].items()
    }
    for year_month in node_power_means
}

# 4. Convert dictionary to DataFrame
df_power_means = []
for year_month, month_data in power_mean_results.items():
    for node_range, means in month_data.items():
        df_power_means.append({
            "year_month": year_month,
            "node_range": node_ranges[node_range],
            "normal": means["normal"],
            "not_normal": means["not_normal"]
        })

df_power_means = pd.DataFrame(df_power_means)

# 5. Pivot for heatmap
df_pivot_normal = df_power_means.pivot(index="year_month", columns="node_range", values="normal")
df_pivot_not_normal = df_power_means.pivot(index="year_month", columns="node_range", values="not_normal")

# 6. Set color range across both heatmaps
vmin = min(df_pivot_normal.min().min(), df_pivot_not_normal.min().min())
vmax = max(df_pivot_normal.max().max(), df_pivot_not_normal.max().max())

# 7. Configure colormap
cmap = plt.get_cmap("YlOrRd").copy()
cmap.set_bad(color='black')

# 8. Heatmap drawing function (with save path)
def draw_heatmap(data, label, save_path):
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(
        data,
        cmap=cmap,
        annot=False,
        vmin=vmin,
        vmax=vmax,
        linewidths=0.5,
        cbar_kws={"label": label}
    )
    plt.xlabel("Node Range", fontsize=30, fontweight='bold')
    plt.ylabel("Year-Month", fontsize=30, fontweight='bold')
    plt.xticks(fontsize=28, rotation=45)
    plt.yticks(fontsize=28, rotation=0)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=28)
    cbar.set_label(label, fontsize=30, fontweight='bold')

    plt.tight_layout()
    plt.savefig(save_path)

# 9. Generate and save heatmaps
draw_heatmap(df_pivot_normal, "Per-node Avg.\nJob Power (W)", "./results/normal_node_monthly.pdf")
draw_heatmap(df_pivot_not_normal, "Per-node Avg.\nJob Power (W)", "./results/non_normal_node_monthly.pdf")
