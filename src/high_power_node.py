import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Filter only KNL nodes
df_knl = df_power[df_power["node_type"] == "knl"]
print(np.mean(df_knl['power_mean']))

# 1. Filter jobs with power_mean greater than the overall mean
power_mean_threshold = df_knl["power_mean"].mean()
high_power_df = df_knl[df_knl["power_mean"] > power_mean_threshold]

# 2. Define node ranges
node_ranges = {
    "node0000~node0999": range(0, 1000),
    "node1000~node1999": range(1000, 2000),
    "node2000~node2999": range(2000, 3000),
    "node3000~node3999": range(3000, 4000),
    "node4000~node4999": range(4000, 5000),
    "node5000~node5999": range(5000, 6000),
    "node6000~node6999": range(6000, 7000),
    "node7000~node7999": range(7000, 8000),
    "node8000~node8305": range(8000, 8306)
}

# 3. Initialize counts for each node range
node_range_counts = {key: 0 for key in node_ranges.keys()}

# 4. Count how many times nodes from each range were used
for _, row in high_power_df.iterrows():
    for node in row["nodes"]:
        node_num = int(node.replace("node", ""))
        for range_name, range_vals in node_ranges.items():
            if node_num in range_vals:
                node_range_counts[range_name] += 1
                break


custom_colors = [
    "#a08f56",  # olive mustard
    "#e57c63",  # bright terracotta
    "#97c264",  # vivid light green
    "#f2be5c",  # warm yellow ochre
    "#6cb1a5",  # bright mint blue
    "#f59a5a",  # fresh apricot orange
    "#b5563d",  # soft clean red
    "#a6b38b",  # sage gray
    "#f0d264"   # saturated mustard yellow
]

# 5. Set color palette
colors = custom_colors[:len(node_range_counts)]

# 6. Create pie chart
plt.figure(figsize=(8.5, 8))
wedges, texts = plt.pie(
    node_range_counts.values(),
    startangle=90,
    colors=colors,
    wedgeprops=dict(edgecolor='white')
)

# 7. Create custom labels for legend
labels = []
total = sum(node_range_counts.values())
for i, (name, count) in enumerate(node_range_counts.items()):
    percent = 100 * count / total
    labels.append(f"Range {i} ({percent:.1f}%)")

# 8. Add legend 
plt.legend(
    wedges,
    labels,
    title=None,
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=22,
    frameon=True,
    facecolor="whitesmoke",
    edgecolor="gray"
)

plt.axis('equal')  # Make pie chart a circle
plt.tight_layout()
plt.savefig("./results/high_power_node.pdf")
