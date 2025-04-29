import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load preprocessed data and generate necessary columns
df_power = pd.read_pickle("processed_data.pkl")

# Classify queue type based on queue_name
df_power["queue_type"] = df_power["queue_name"].apply(
    lambda x: "Normal" if x in ["normal", "norm_skl", "long", "flat", "debug", "commercial"] else "Non-normal"
)

# Boxplot style configuration
box_kwargs = dict(
    boxprops=dict(edgecolor='black', linewidth=2),
    whiskerprops=dict(color='black', linewidth=2),
    capprops=dict(color='black', linewidth=2),
    medianprops=dict(color='black', linewidth=2),
    showfliers=False
)

# Plotting
plt.figure(figsize=(12, 4.5))
ax = sns.boxplot(
    data=df_power,
    x="year_month",
    y="power_mean",
    hue="queue_type",
    hue_order=["Normal", "Non-normal"],
    palette={"Normal": "#6BA292", "Non-normal": "#B04A30"},
    linewidth=1.2,
    **box_kwargs
)

# Adjust transparency of box colors
for patch in ax.patches:
    facecolor = patch.get_facecolor()
    patch.set_facecolor((*facecolor[:3], 0.8))

# Axis and label settings
plt.xlabel("Year-Month", fontsize=21, fontweight='bold')
plt.ylabel("Per-node Avg.\nJob Power (W)", fontsize=21, fontweight='bold')
plt.xticks(rotation=30, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(title=None, fontsize=20)

# Axis spine settings
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.2)

# Grid and tick settings
ax.grid(axis='x', visible=False)
ax.grid(axis='y', visible=True)
ax.tick_params(axis='both', which='both', direction='out', length=6, width=1.2, colors='black')
ax.set_yticks([0, 200, 400, 600, 800])

# Layout adjustment and show plot
plt.tight_layout()
plt.savefig("./results/queue_power.pdf")
