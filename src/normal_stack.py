import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Define target queues to use
valid_queues = ["normal", "long", "flat", "debug"]

# 2. Load and filter data
df_power = pd.read_pickle("processed_data.pkl")

# Filter only KNL nodes
df_knl = df_power[df_power["node_type"] == "knl"]
df_filtered = df_knl[df_knl["queue_name"].isin(valid_queues)].copy()

# 3. Define node ranges
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

# Define custom colors
custom_colors = [
    "#a08f56", "#e57c63", "#97c264", "#f2be5c", "#6cb1a5",
    "#f59a5a", "#b5563d", "#a6b38b", "#f0d264"
]

# Initialize range names and monthly count dictionary
range_names = list(node_ranges.keys())
monthly_counts = {}

# 4. Count the number of nodes used per range for each month
for _, row in df_filtered.iterrows():
    nodes = row["nodes"]
    year = row["start_year"]
    month = row["start_month"]
    month_key = f"{int(year)}-{int(month):02d}"

    if month_key not in monthly_counts:
        monthly_counts[month_key] = {k: 0 for k in range_names}

    for node in nodes:
        node_number = int(node.replace("node", ""))
        for range_name, node_range in node_ranges.items():
            if node_number in node_range:
                monthly_counts[month_key][range_name] += 1
                break

# 5. Convert the counts to a DataFrame and sort by time
monthly_counts_df = pd.DataFrame.from_dict(monthly_counts, orient='index')
monthly_counts_df.index = pd.to_datetime(monthly_counts_df.index)
monthly_counts_df = monthly_counts_df.sort_index()

# 6. Create labels for legend (Range 0 ~ 8)
range_labels = [f"Range {i}" for i in range(len(monthly_counts_df.columns))]

# 7. Create the plot
fig, ax = plt.subplots(figsize=(12, 6.5))
stacked = ax.stackplot(
    monthly_counts_df.index,
    monthly_counts_df.T.values,
    labels=range_labels,
    colors=custom_colors
)

# 8. Draw white boundary lines between stacked areas
cumsum = np.cumsum(monthly_counts_df.T.values, axis=0)
for i in range(len(cumsum) - 1):
    ax.plot(
        monthly_counts_df.index,
        cumsum[i],
        color="white",
        linewidth=0.8,
        alpha=0.9
    )

# 9. Set labels, ticks, and style
plt.xlabel("Year-Month", fontsize=24, fontweight='bold')
plt.ylabel("Number of\nExecuted Jobs", fontsize=24, fontweight='bold')
plt.yticks([0, 100000, 200000, 300000, 400000], fontsize=23)
plt.xticks(fontsize=23, rotation=30)

# Customize the order of legend entries
custom_legend_order = [0, 5, 1, 6, 2, 7, 3, 8, 4]
custom_labels = [f"Range {i}" for i in custom_legend_order]
custom_colors_ordered = [custom_colors[i] for i in custom_legend_order]

# Create legend handles manually
from matplotlib.patches import Patch
legend_handles = [
    Patch(facecolor=color, edgecolor='black', label=label)
    for label, color in zip(custom_labels, custom_colors_ordered)
]

# Add customized legend
plt.legend(
    handles=legend_handles,
    loc='upper center',
    bbox_to_anchor=(0.4, 1.4),
    ncol=5,
    fontsize=19,
    frameon=True,
    facecolor="whitesmoke",
    edgecolor="gray"
)

# Set grid and axis options
ax.set_axisbelow(True)
ax.grid(visible=True, axis="y")
ax.grid(visible=False, axis="x")

plt.tight_layout()
plt.savefig("./results/normal_stack.pdf")
