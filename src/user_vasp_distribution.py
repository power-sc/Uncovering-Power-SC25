import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Filter the original data for a specific user and account
df_vasp = df_power[
    (df_power["user_id"] == "optpar04") &
    (df_power["account"] == "vasp")
].copy()

# Convert data types
df_vasp["exit_code"] = df_vasp["exit_code"].astype(str)
df_vasp["cpus"] = df_vasp["cpus"].astype(int)

# Remove CPU counts that appear fewer than 5 times (for the left plot)
valid_cpus = df_vasp["cpus"].value_counts()
valid_cpus = valid_cpus[valid_cpus > 5].index
df_cpus_filtered = df_vasp[df_vasp["cpus"].isin(valid_cpus)]

# Filter node counts to 1, 2, 4, 8 (for the right plot)
df_node_filtered = df_vasp[df_vasp["node_count"].isin([1, 2, 4, 8])]

# Create subplots
fig, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

# Common boxplot style settings
box_kwargs = dict(
    boxprops=dict(edgecolor='black', linewidth=2),
    whiskerprops=dict(color='black', linewidth=2),
    capprops=dict(color='black', linewidth=2),
    medianprops=dict(color='black', linewidth=2),
    showfliers=False
)

# Left plot: # of CPU cores vs. per-node average job power
sns.boxplot(
    data=df_cpus_filtered,
    x="cpus",
    y="power_mean",
    color="#e5b97b",
    ax=ax2,
    **box_kwargs
)
ax2.set_xlabel("# of CPU cores", fontsize=24, fontweight='bold')
ax2.set_ylabel("Per-node Avg.\nJob Power (W)", fontsize=24, fontweight='bold')
ax2.tick_params(axis='both', which='major', labelsize=22, direction='out', length=6, width=1.2)
ax2.grid(axis='x', visible=False)
ax2.grid(axis='y', visible=True)

# Set axis borders
for spine in ['top', 'bottom', 'left', 'right']:
    ax2.spines[spine].set_visible(True)
    ax2.spines[spine].set_color('black')
    ax2.spines[spine].set_linewidth(1.0)

# Right plot: # of nodes vs. per-node average job power
sns.boxplot(
    data=df_node_filtered,
    x="node_count",
    y="power_mean",
    color="#aac5a0",
    ax=ax3,
    **box_kwargs
)
ax3.set_xlabel("# of Nodes", fontsize=24, fontweight='bold')
ax3.set_ylabel("")
ax3.tick_params(axis='both', which='major', labelsize=22, direction='out', length=6, width=1.2)
ax3.grid(axis='x', visible=False)
ax3.grid(axis='y', visible=True)

# Set axis borders
for spine in ['top', 'bottom', 'left', 'right']:
    ax3.spines[spine].set_visible(True)
    ax3.spines[spine].set_color('black')
    ax3.spines[spine].set_linewidth(1.0)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("./results/user_vasp_distribution.pdf")
