import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.ticker import MaxNLocator
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Define the target accounts for analysis
target_accounts = ["vasp", "gaussian", "lammps"]

# Filter the data for the target accounts and node counts
df_filtered = df_power[
    df_power["account"].isin(target_accounts) &
    df_power["node_count"].isin([1, 2, 4, 8, 16, 32])
].copy()

# Classify queue types
df_filtered["queue_type"] = df_filtered["queue_name"].apply(
    lambda x: "Normal" if x in ["normal", "norm_skl"] else "Non-normal"
)

# Convert node_type to uppercase
df_filtered["node_type"] = df_filtered["node_type"].str.upper()

# Define color mapping
color_map = {"KNL": "#b5acd6", "SKL": "#f2c288"}

# Create a FacetGrid
g = sns.FacetGrid(
    df_filtered,
    col="account",
    hue="node_type",
    sharey=True,
    height=5,
    aspect=1.2,
    palette=color_map
)

# Function to draw violin plots
def draw_violin(data, color, **kwargs):
    ax = plt.gca()
    sns.violinplot(
        data=data,
        x="node_count",
        y="power_mean",
        hue="node_type",
        palette=color_map,
        order=[1, 2, 4, 8, 16, 32],
        cut=0,
        linewidth=2.0,
        ax=ax,
        split=False
    )
    # Remove duplicated hue legends
    if ax.get_legend():
        ax.legend_.remove()

# Map the violin plot drawing function to each subplot
g.map_dataframe(draw_violin)

# Set axis labels
g.set_axis_labels("Node Count", "Per-node Power Avg")
for i, ax in enumerate(g.axes.flatten()):
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', visible=True)
    ax.set_xlabel("Node Count", fontsize=37, fontweight="bold")
    ax.set_ylabel("Per-node Avg.\nJob Power (W)", fontsize=37, fontweight="bold")
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xticklabels([1, 2, 4, 8, 16, 32], fontsize=37)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))

    for label in ax.get_yticklabels():
        label.set_fontsize(37)

# Customize plot borders
for ax in g.axes.flatten():
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(1.0)
    ax.tick_params(axis='both', which='major', labelsize=37)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(34)

# Add and customize the legend
g.add_legend(
    title=None,
    loc="upper right",
    bbox_to_anchor=(0.99, 1.04),
    frameon=True
)
if g._legend is not None:
    g._legend.set_title("")
    for text in g._legend.get_texts():
        text.set_fontsize(37)
    g._legend.get_frame().set_edgecolor("gray")
    g._legend.get_frame().set_facecolor("whitesmoke")

# Remove facet titles
g.set_titles("")

# Make the violin plot borders bold
for ax in g.axes.flatten():
    for artist in ax.findobj(match=PolyCollection):
        artist.set_edgecolor("black")
        artist.set_linewidth(2.0)

# Adjust layout and save the figure
plt.tight_layout(rect=[0, 0, 1, 1.09])
plt.savefig("./results/application_distribution.pdf")
