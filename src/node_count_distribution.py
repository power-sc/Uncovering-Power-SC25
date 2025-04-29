import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Define the list of target node counts to analyze
target_nodes = [1, 2, 4, 8, 16, 32]

# Classify queue type into Normal and Non-normal
df_power["queue_type"] = df_power["queue_name"].apply(
    lambda x: "Normal" if x in ["normal", "norm_skl", "long", "flat", "debug", "commercial"] else "Non-normal"
)

# Filter the data for the target node counts
df_filtered = df_power[df_power["node_count"].isin(target_nodes)]

# Initialize the figure
plt.figure(figsize=(12, 4))

# Define custom color palette
custom_palette = {
    "Normal": "#6BA292",
    "Non-normal": "#B04A30"
}

# Define common boxplot properties
box_kwargs = dict(
    boxprops=dict(edgecolor='black', linewidth=2),
    whiskerprops=dict(color='black', linewidth=2),
    capprops=dict(color='black', linewidth=2),
    medianprops=dict(color='black', linewidth=2),
    showfliers=False
)

# Create the boxplot for power_mean by node_count and queue_type
sns.boxplot(
    data=df_filtered,
    x="node_count",
    y="power_mean",
    hue="queue_type",
    order=target_nodes,
    palette=custom_palette,
    linewidth=1.2,
    **box_kwargs
)

# Set axis labels and legend
plt.xlabel("Node Count", fontsize=24, fontweight='bold')
plt.ylabel("Per-node Avg.\nJob Power (W)", fontsize=24, fontweight='bold')
plt.legend(title=None, fontsize=20)

# Customize plot borders
ax = plt.gca()
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.0)

# Apply transparency (alpha) to box colors
for patch in ax.patches:
    facecolor = patch.get_facecolor()
    patch.set_facecolor((*facecolor[:3], 0.8))  # RGB + alpha

# Customize grid and ticks
ax.yaxis.set_major_locator(ticker.MaxNLocator(4))
ax.grid(axis='x', visible=False)
ax.grid(axis='y', visible=True)
ax.tick_params(
    axis='both',
    which='both',
    direction='out',
    length=6,
    width=1.5,
    color='black',
    top=False,
    bottom=True,
    left=True,
    right=False
)

# Set tick label sizes
plt.xticks(fontsize=23)
plt.yticks(fontsize=23)

plt.tight_layout()
plt.savefig("./results/node_count_distribution.pdf")
