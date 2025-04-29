import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# 1. Load preprocessed data and basic preprocessing
df_power = pd.read_pickle("processed_data.pkl")
df_power = df_power[df_power["power_mean"] != 0].copy()
df_power["submit_time"] = pd.to_datetime(df_power["submit_time"])
df_power["hour"] = df_power["submit_time"].dt.hour
df_power["hour_block"] = df_power["hour"].apply(lambda h: 
    ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"][h // 3]
)
df_power["weekday"] = df_power["submit_time"].dt.day_name()

# 2. Define the order for weekdays and hour blocks
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hour_order = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]

# 3. Create pivot tables for power_mean and wait_s
power_table = (
    df_power.groupby(["weekday", "hour_block"])["power_mean"]
    .mean()
    .unstack(fill_value=np.nan)
    .reindex(index=weekday_order, columns=hour_order)
)

wait_table = (
    df_power.groupby(["weekday", "hour_block"])["wait_s"]
    .mean()
    .unstack(fill_value=np.nan)
    .reindex(index=weekday_order, columns=hour_order)
)

# 4. Flatten pivot tables and remove NaN values
power_flat = power_table.values.flatten()
wait_flat = wait_table.values.flatten()
valid_mask = (~np.isnan(power_flat)) & (~np.isnan(wait_flat))

flat_df = (
    pd.DataFrame({
        "power_mean": power_table.values.flatten(),
        "wait_s": wait_table.values.flatten(),
        "weekday": np.repeat(weekday_order, len(hour_order)),
        "hour_block": hour_order * len(weekday_order)
    })
    .dropna()
)

# 5. Plot scatter plot with regression line
sns.set(style="whitegrid")
plt.figure(figsize=(12, 3.4))
sns.regplot(
    data=flat_df,
    x="power_mean",
    y="wait_s",
    scatter_kws={"alpha": 0.4},
    line_kws={"color": "darkolivegreen", "linewidth": 4.0},
)

# Axis labels and settings
plt.xlabel("Per-node Avg. Job Power (W)", fontsize=24, fontweight='bold')
plt.ylabel("Wait Time (s)", fontsize=24, fontweight='bold')
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

# Axis spine and grid settings
ax = plt.gca()
for spine in ['top', 'bottom', 'left', 'right']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_color('black')
    ax.spines[spine].set_linewidth(1.0)

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
ax.yaxis.set_ticks([5000, 15000, 25000])

# 6. Calculate and display Pearson correlation coefficient
corr_coef, p_value = pearsonr(flat_df["power_mean"], flat_df["wait_s"])

# Display Pearson r value at the top-right corner
plt.text(
    0.97, 0.96,
    f"Pearson r = {corr_coef:.2f}",
    fontsize=24,
    fontweight='bold',
    ha='right',
    va='top',
    transform=plt.gca().transAxes
)

# Final layout adjustment and save
plt.tight_layout()
plt.savefig("./results/wait_power.pdf")
