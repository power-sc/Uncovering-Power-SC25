import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# 1. Define a function to label 3-hour time blocks
def get_hour_block(hour):
    blocks = [
        (0, 3, "00-03"), (3, 6, "03-06"), (6, 9, "06-09"), (9, 12, "09-12"),
        (12, 15, "12-15"), (15, 18, "15-18"), (18, 21, "18-21"), (21, 24, "21-24"),
    ]
    for start, end, label in blocks:
        if start <= hour < end:
            return label
    return "Unknown"

# 2. Preprocessing: remove rows where power_mean is zero
df_power = pd.read_pickle("processed_data.pkl")
df_power = df_power[df_power["power_mean"] != 0].copy()

# 3. Feature generation
df_power["submit_time"] = pd.to_datetime(df_power["submit_time"])
df_power["hour"] = df_power["submit_time"].dt.hour
df_power["hour_block"] = df_power["hour"].apply(get_hour_block)
df_power["weekday"] = df_power["submit_time"].dt.day_name()

# 4. Define sorting orders
hour_order = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_short = {
    "Monday": "Mon.", "Tuesday": "Tue.", "Wednesday": "Wed.",
    "Thursday": "Thu.", "Friday": "Fri.", "Saturday": "Sat.", "Sunday": "Sun."
}

# 5. Create pivot tables
pivot_power = (
    df_power
    .groupby(["weekday", "hour_block"])["power_mean"]
    .mean()
    .unstack(fill_value=0)
    .reindex(index=weekday_order, columns=hour_order)
)

pivot_wait = (
    df_power
    .groupby(["weekday", "hour_block"])["wait_s"]
    .mean()
    .unstack(fill_value=0)
    .reindex(index=weekday_order, columns=hour_order)
)

# 6. Plot two heatmaps side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

# Heatmap for power_mean
sns.heatmap(
    pivot_power,
    annot=False,
    cmap="YlOrBr",
    linewidths=0.5,
    cbar_kws={"label": "Per-node Avg. Power (W)"},
    ax=ax1
)
cbar1 = ax1.collections[0].colorbar
cbar1.ax.tick_params(labelsize=20)
cbar1.ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
cbar1.set_label("Per-node Avg.\nJob Power (W)", fontsize=23, weight='bold')

ax1.set_xlabel("Time Interval (3-Hour)", fontsize=24, fontweight='bold')
ax1.set_ylabel("Day of Week", fontsize=24, fontweight='bold')
ax1.set_xticklabels(hour_order, fontsize=20, rotation=45)
ax1.set_yticklabels([weekday_short[wd] for wd in weekday_order], fontsize=20, rotation=0)

# Heatmap for wait_s
sns.heatmap(
    pivot_wait,
    annot=False,
    cmap="YlOrBr",
    linewidths=0.5,
    cbar_kws={"label": "Wait Time (s)", "aspect": 11},
    ax=ax2
)
cbar2 = ax2.collections[0].colorbar
cbar2.ax.tick_params(labelsize=20)
cbar2.ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
cbar2.set_label("Wait Time (s)", fontsize=23, weight='bold')

ax2.set_xlabel("Time Interval (3-Hour)", fontsize=24, fontweight='bold')
ax2.set_xticklabels(hour_order, fontsize=20, rotation=45)

# Overall adjustments
plt.tight_layout()
plt.savefig("./results/week_power_wait.pdf")
