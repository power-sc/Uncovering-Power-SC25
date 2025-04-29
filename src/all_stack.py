import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# 1. Load and filter the data
df_power = pd.read_pickle("processed_data.pkl")

# Filter only KNL nodes
df_knl = df_power[df_power["node_type"] == "knl"]

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

# 3. Define custom color palette
custom_colors = [
    "#a08f56",  # olive mustard
    "#e57c63",  # lively terracotta
    "#97c264",  # vivid light green
    "#f2be5c",  # warm yellow ochre
    "#6cb1a5",  # bright mint blue
    "#f59a5a",  # fresh apricot orange
    "#b5563d",  # clean soft red
    "#a6b38b",  # sage grey
    "#f0d264"   # saturated mustard yellow
]

# 4. Initialize range names and dictionary to store monthly counts
range_names = list(node_ranges.keys())
monthly_counts = {}

# 5. Count node usage per month for each range
for _, row in df_knl.iterrows():
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

# 6. Convert the monthly counts dictionary to a DataFrame and sort by date
monthly_counts_df = pd.DataFrame.from_dict(monthly_counts, orient='index')
monthly_counts_df.index = pd.to_datetime(monthly_counts_df.index)
monthly_counts_df = monthly_counts_df.sort_index()

# 7. Create labels for each range
range_labels = [f"Range {i}" for i in range(len(monthly_counts_df.columns))]

# 8. Create the plot
fig, ax = plt.subplots(figsize=(12, 4))
stacked = ax.stackplot(
    monthly_counts_df.index,
    monthly_counts_df.T.values,
    labels=range_labels,
    colors=custom_colors
)

# 9. Draw white boundary lines between stacked areas
cumsum = np.cumsum(monthly_counts_df.T.values, axis=0)
for i in range(len(cumsum) - 1):
    ax.plot(
        monthly_counts_df.index,
        cumsum[i],
        color="white",
        linewidth=0.8,
        alpha=0.9
    )

# 10. Set labels, ticks, and style
plt.xlabel("Year-Month", fontsize=24, fontweight='bold')
plt.ylabel("Number of\nExecuted Jobs", fontsize=24, fontweight='bold')
plt.yticks([0, 200000, 400000, 600000, 800000], fontsize=23)
plt.xticks(fontsize=23, rotation=30)

ax.set_axisbelow(True)
ax.grid(visible=True, axis="y")
ax.grid(visible=False, axis="x")

# 11. Final layout and save
plt.tight_layout()
plt.savefig("./results/all_stack.pdf")
