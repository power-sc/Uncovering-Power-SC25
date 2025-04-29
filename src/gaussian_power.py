import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np

# Load the preprocessed data
df_cluster = pd.read_pickle("clustered_data.pkl")

# 1. Filter for user_id='one_user' and account='gaussian'
df_filtered = df_cluster[(df_cluster["user_id"] == "one_user") & (df_cluster["account"] == "gaussian")].copy()

# 2. Randomly select exactly 2 clusters
clusters = df_filtered["combined_cluster"].dropna().unique()
np.random.seed(42)  # To ensure reproducibility
selected_clusters = np.random.choice(clusters, size=2, replace=False)

# Color list (up to 4 jobs)
color_list = [
    "#BC8F8F",  # RosyBrown
    "#6B8E23",  # OliveDrab
    "#C04000",  # Mahogany-like Brown Orange
    "#DAA520",  # Goldenrod
]

# 3. Plot each cluster separately
for idx, cluster_id in enumerate(selected_clusters):
    df_cluster_selected = df_filtered[df_filtered["combined_cluster"] == cluster_id].copy()
    df_cluster_selected = df_cluster_selected.reset_index(drop=True)

    # Create color mapping
    color_dict = dict(zip(df_cluster_selected.index, color_list))
    handles = [
        Line2D([0], [0], color=color_dict[i], linewidth=8)
        for i in df_cluster_selected.index
    ]

    # Label: A - Job or B - Job
    label_prefix = 'A' if idx == 0 else 'B'
    labels = [f"{label_prefix} - Job {i}" for i in range(len(df_cluster_selected))]

    plt.figure(figsize=(13, 4.8))

    for i, (index, row) in enumerate(df_cluster_selected.iterrows()):
        plt.plot(row["normalized_power"], color=color_dict[index], linewidth=2)

    # Set axis labels and limits
    plt.xlabel("Job Execution Time (s)", fontsize=24, fontweight='bold')
    plt.ylabel("Per-node Power (W)", fontsize=24, fontweight='bold')
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.ylim(210, 360)

    # Customize axis spines
    ax = plt.gca()
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(1.0)

    # Customize grid
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', visible=True)
    ax.set_yticks([200, 250, 300, 350])
    ax.set_xticks([0, 800, 1600, 2400])

    # Add legend
    legend = plt.legend(
        handles=handles,
        labels=labels,
        loc='lower center',
        ncol=4,
        fontsize=20,
        title_fontsize=24,
        frameon=True
    )
    legend.get_frame().set_linewidth(1.5)

    plt.tight_layout()

    # Save figure
    if idx == 0:
        plt.savefig("./results/gaussian_power.pdf")
    else:
        plt.savefig("./results/gaussian_power2.pdf")

    plt.close()
