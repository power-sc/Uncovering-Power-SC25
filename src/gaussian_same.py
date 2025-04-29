import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def draw_sine_wave_vertical(ax, side='right', amplitude=0.2, frequency=10, linewidth=1.5, color='k'):
    """
    Draw a vertical sine wave to represent a broken axis.
    
    ax : matplotlib axis
    side : 'left' or 'right'
    amplitude : amplitude of the sine wave
    frequency : number of waves
    linewidth : line width of the sine wave
    color : line color
    """
    y = np.linspace(0, 1, 500)  # Full range along the y-axis
    x_center = 1.0 if side == 'right' else 0.0
    x = x_center + amplitude * np.sin(2 * np.pi * frequency * y)

    ax.plot(x, y, transform=ax.transAxes, color=color, lw=linewidth, clip_on=False)

# Merge two datasets
df_combined = pd.concat([df_plot, df_plot_2], ignore_index=True)
print(len(df_combined))

# Create a broken x-axis subplot
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 2.5), width_ratios=[4, 6], sharey=True, gridspec_kw={'wspace': 0.15})

# Define masks for left and right plots
left_mask = (df_combined["cpu_percent"] >= 1655) & (df_combined["cpu_percent"] <= 1715)
right_mask = (df_combined["cpu_percent"] >= 6120) & (df_combined["cpu_percent"] <= 6160)

# Left plot
scatter_left = ax_left.scatter(
    x=df_combined.loc[left_mask, "cpu_percent"],
    y=df_combined.loc[left_mask, "mem_kb"],
    s=df_combined.loc[left_mask, "run_s"] * 0.01,
    c=df_combined.loc[left_mask, "wait_s"],
    cmap="coolwarm",
    alpha=0.6,
    vmin=50,
    vmax=df_combined["wait_s"].max(),
    zorder=2
)
ax_left.set_xlim(1655, 1715)
ax_left.set_ylim(20, 60)
ax_left.set_xticks([1660, 1680, 1700])
ax_left.tick_params(axis='x', labelsize=16)
ax_left.set_ylabel("Memory (GB)", fontsize=18, fontweight='bold')
ax_left.tick_params(axis='y', labelsize=16)
ax_left.grid(axis='y', linewidth=1, zorder=1)
ax_left.set_xlabel(" ")

# Right plot
scatter_right = ax_right.scatter(
    x=df_combined.loc[right_mask, "cpu_percent"],
    y=df_combined.loc[right_mask, "mem_kb"],
    s=df_combined.loc[right_mask, "run_s"] * 0.01,
    c=df_combined.loc[right_mask, "wait_s"],
    cmap="coolwarm",
    alpha=0.6,
    vmin=0,
    vmax=df_combined["wait_s"].max(),
    zorder=2
)
ax_right.set_xlim(6085, 6180)
ax_right.set_xticks([6100, 6120, 6140, 6160, 6180])
ax_right.tick_params(axis='x', labelsize=16)
ax_right.grid(axis='y', linewidth=1, zorder=1)
ax_right.set_xlabel(" ")
ax_right.tick_params(axis='y', left=False, labelleft=False)

# Shared colorbar
cbar = fig.colorbar(scatter_right, ax=[ax_left, ax_right], aspect=5, pad=0.04)
cbar.set_label("Wait Time (s)", fontsize=18, fontweight='bold')
cbar.ax.tick_params(labelsize=16)

# Add common x-axis label
fig.text(0.48, -0.1, "CPU (%)", ha='center', fontsize=18, fontweight='bold')

# Hide spines between the subplots
ax_left.spines['right'].set_visible(False)
ax_right.spines['left'].set_visible(False)

# Add sine waves to represent broken axes
draw_sine_wave_vertical(ax_left, side='right', amplitude=0.01, frequency=3)
draw_sine_wave_vertical(ax_right, side='left', amplitude=0.01, frequency=3)

# Highlight certain x-axis regions
ax_left.axvspan(1673, 1710, color='blue', alpha=0.05, zorder=0)
ax_right.axvspan(6115, 6170, color='red', alpha=0.05, zorder=0)

plt.tight_layout()
plt.savefig("./results/gaussian_same.pdf")
