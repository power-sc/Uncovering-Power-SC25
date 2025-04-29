import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Filter the dataset for a specific user and account
df_vasp = df_power[
    (df_power["user_id"] == "optpar04") &
    (df_power["account"] == "vasp")
].copy()

# Convert data types
df_vasp["exit_code"] = df_vasp["exit_code"].astype(str)
df_vasp["cpus"] = df_vasp["cpus"].astype(int)

# Define the desired order of exit codes
exit_order = ["0.0", "255.0", "271.0"]

# Calculate the average power for each exit code (maintaining the specified order)
exit_avg = (
    df_vasp
    .groupby("exit_code")["power_mean"]
    .mean()
    .reindex(exit_order)
)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 3.5))

# Draw the violin plot
sns.violinplot(
    data=df_vasp,
    x="exit_code",
    y="power_mean",
    order=exit_order,
    color="#d8a3a3",
    linewidth=2.0,
    cut=0,
    inner="box",
    ax=ax
)

# Make the violin plot edges thicker and black
for artist in ax.findobj(match=PolyCollection):
    artist.set_edgecolor("black")
    artist.set_linewidth(2.0)

# Plot the mean line with markers
ax.plot(
    range(len(exit_order)),
    exit_avg.values,
    marker='o',
    markersize=13,
    markeredgecolor="#4a2f25",
    linestyle='-',
    color="#4a2f25",
    linewidth=5.0,
    label="Mean"
)

# Set axis labels and formatting
ax.set_xlabel("Exit Code", fontsize=24, fontweight='bold')
ax.set_ylabel("Per-node Avg.\nJob Power (W)", fontsize=24, fontweight='bold')
ax.set_xticks(range(len(exit_order)))
ax.set_xticklabels(exit_order, fontsize=22)
ax.tick_params(axis='y', labelsize=22, direction='out', length=6, width=1.2)

# Add grid lines
ax.grid(axis='x', visible=False)
ax.grid(axis='y', visible=True)

# Set visible and styled axis borders
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.0)

# Final layout adjustments and save the figure
plt.tight_layout()
plt.savefig("./results/vasp_exit.pdf")
