import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import numpy as np
import matplotlib.ticker as ticker

# 1. Preprocessing and column generation
df_power = pd.read_pickle("processed_data.pkl")

df_power = df_power[df_power["power_mean"] != 0].copy()
df_power["year_month"] = df_power["start_year"] + "-" + df_power["start_month"].str.zfill(2)

# 2. Monthly aggregation
result_jobs = df_power.groupby("year_month").size().reset_index(name="job_count")
result_power = df_power.groupby("year_month")["power_mean"].mean().reset_index()

# 3. Color mapping per month
year_month_order = result_power["year_month"].tolist()
num_points = len(year_month_order)
cmap = cm.get_cmap("BrBG", num_points)
colors_line = [cmap(i) for i in range(num_points)]
color_map = dict(zip(year_month_order, colors_line))

# 4. Prepare data for violin plot
df_power_violin = df_power[df_power["year_month"].isin(year_month_order)].copy()

# 5. Plot configuration
sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6), sharex=True, height_ratios=[4, 4])

# -------------------------
# ▶ Top: Boxplot (showfliers=False)
# -------------------------

# Common boxplot styling
box_kwargs = dict(
    boxprops=dict(edgecolor='black', linewidth=2),
    whiskerprops=dict(color='black', linewidth=2),
    capprops=dict(color='black', linewidth=2),
    medianprops=dict(color='black', linewidth=2),
    showfliers=False
)

sns.boxplot(
    data=df_power_violin,
    x="year_month",
    y="power_mean",
    order=year_month_order,
    palette=color_map,
    linewidth=1.2,
    ax=ax1,
    **box_kwargs
)

ax1.set_ylabel("Per-node Avg.\nJob Power (W)", fontsize=21, fontweight="bold")
ax1.set_xticks([])  # remove top axis ticks
ax1.set_xlim(-0.5, num_points - 0.5)
ax1.yaxis.set_major_locator(ticker.MaxNLocator(nbins=3, integer=True))
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))
ax1.tick_params(axis='both', which='both', direction='out', length=6, width=1.5, color='black')

for spine in ['top', 'bottom', 'left', 'right']:
    ax1.spines[spine].set_visible(True)
    ax1.spines[spine].set_color('black')
    ax1.spines[spine].set_linewidth(1.0)

ax1.set_yticklabels(ax1.get_yticks(), fontsize=22)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))

# -------------------------
# ▶ Bottom: Barplot (manually using ax.bar)
# -------------------------
x_ticks = np.arange(num_points)
bar_heights = result_jobs["job_count"].values
bar_colors = [color_map[month] for month in year_month_order]
ax2.bar(x_ticks, bar_heights, color=bar_colors, edgecolor='black')

# Set bar edge style
for patch in ax2.patches:
    patch.set_edgecolor('black')
    patch.set_linewidth(2.0)

ax2.set_xticks(x_ticks)
ax2.set_xticklabels(year_month_order, fontsize=22, rotation=30)
ax2.set_xlabel("Year-Month", fontsize=22, fontweight='bold')
ax2.set_ylabel("Job Count", fontsize=22, fontweight='bold')
ax2.set_xlim(-0.5, num_points - 0.5)
ax2.set_ylim(0, 260000)
ax2.yaxis.set_major_locator(ticker.MaxNLocator(nbins=3, integer=True))
ax2.tick_params(axis='both', which='both', direction='out', length=6, width=1.5, color='black')
ax2.grid(axis='x', visible=False)
ax2.grid(axis='y', visible=True)

# Annotate bar values
for i, height in enumerate(bar_heights):
    ax2.annotate(f"{int(height)}", (x_ticks[i], height + 5000),
                 ha='center', va='bottom', fontsize=19, color='black')

for spine in ['top', 'bottom', 'left', 'right']:
    ax2.spines[spine].set_visible(True)
    ax2.spines[spine].set_color('black')
    ax2.spines[spine].set_linewidth(1.0)

plt.yticks(fontsize=22)
plt.tight_layout()
plt.savefig("./results/monthly_job_distribution.pdf")
