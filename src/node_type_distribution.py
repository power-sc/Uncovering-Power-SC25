import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Classify queue type
df_power["queue_type"] = df_power["queue_name"].apply(
    lambda x: "Normal" if x in ["normal", "norm_skl"] else "Non-normal"
)

# Filter for 'knl' and 'skl' node types and convert to uppercase
df_filtered = df_power[df_power["node_type"].isin(["knl", "skl"])].copy()
df_filtered["node_type"] = df_filtered["node_type"].str.upper()  # 'KNL', 'SKL'

# Plot the violin plot
plt.figure(figsize=(8, 4))
sns.violinplot(
    data=df_filtered,
    x="node_type",
    y="power_mean",
    hue="queue_type",
    palette={"Normal": "#6BA292", "Non-normal": "#B04A30"},
    cut=0,
    split=True
)

# Set axis labels
plt.xlabel("Node Type", fontsize=16, fontweight='bold')
plt.ylabel("Per-node Avg. Power (W)", fontsize=16, fontweight='bold')

# Remove the legend
plt.legend().remove()

# Customize plot borders
ax = plt.gca()
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.0)

# Set axis and grid settings
ax.set_axisbelow(True)
ax.yaxis.set_major_locator(ticker.MaxNLocator(6))
ax.grid(axis='x', visible=False)
ax.grid(axis='y', visible=True)
ax.tick_params(axis='both', which='both', direction='out', length=6, width=1.2, colors='black')

# Set tick label size
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("./results/node_type_distribution.pdf")
