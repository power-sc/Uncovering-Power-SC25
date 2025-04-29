import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the preprocessed data
df_power = pd.read_pickle("processed_data.pkl")

# Initialize the figure
plt.figure(figsize=(14.5, 5))

# Plot CDF for each node count
for node in [1, 2, 4, 8, 16, 32]:
    data = df_power[df_power["node_count"] == node]["power_mean"]
    sns.ecdfplot(data=data, label=f"{node}", linewidth=4)

# Set axis labels
plt.xlabel("Per-node Avg. Job Power (W)", fontsize=26, fontweight='bold')
plt.ylabel("CDF", fontsize=26, fontweight='bold')

# Set legend above the plot
plt.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.3),  
    ncol=6,                   
    fontsize=25
)

# Customize plot borders and grid
ax = plt.gca()
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.0)

ax.grid(axis='x', visible=False)
ax.grid(axis='y', visible=True)

# Customize ticks and axis limits
plt.xticks(fontsize=25)
plt.xlim(0, 820)
plt.yticks(fontsize=25)

# Adjust layout to prevent overlap
plt.subplots_adjust(top=0.7)

plt.savefig("./results/node_count_cdf.pdf")
