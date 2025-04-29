import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Node range label mapping
node_ranges = {
    "node0000~node0999": "Range 0",
    "node1000~node1999": "Range 1",
    "node2000~node2999": "Range 2",
    "node3000~node3999": "Range 3",
    "node4000~node4999": "Range 4",
    "node5000~node5999": "Range 5",
    "node6000~node6999": "Range 6",
    "node7000~node7999": "Range 7",
    "node8000~node8305": "Range 8"
}

# Load processed data and filter KNL nodes
df_power = pd.read_pickle("processed_data.pkl")
df_knl = df_power[df_power["node_type"] == "knl"]

# Filter jobs executed only in April, May, and June
df_apr_jun = df_knl[df_knl["start_month"].isin(['4', '5', '6'])]
all_combinations = df_knl.groupby(["user_id", "account", "job_name"])["year_month"].unique()
unique_apr_jun_combinations = [
    (user_id, account, job_name)
    for (user_id, account, job_name), months in all_combinations.items()
    if set(months) == {"2024-04", "2024-05", "2024-06"}
]
df_filtered_456 = df_knl[
    df_knl[["user_id", "account", "job_name"]].apply(tuple, axis=1).isin(unique_apr_jun_combinations)
]

# Define node ranges 4–8 for filtering
node_ranges_select = {
    "node4000~node4999": range(4000, 5000),
    "node5000~node5999": range(5000, 6000),
    "node6000~node6999": range(6000, 7000),
    "node7000~node7999": range(7000, 8000),
    "node8000~node8305": range(8000, 8306)
}

# Select jobs using at least one node in Range 4–8
job_counts = {key: 0 for key in node_ranges}
matching_jobs = []
for _, row in df_filtered_456.iterrows():
    nodes = row["nodes"]
    matched = False
    for node in nodes:
        node_number = int(node.replace("node", ""))
        for range_name, node_range in node_ranges_select.items():
            if node_number in node_range:
                job_counts[range_name] += 1
                matched = True
                break
    if matched:
        matching_jobs.append(row[["user_id", "account", "queue_name", "job_name"]])

df_matching_jobs = pd.DataFrame(matching_jobs)
matching_user_accounts = df_matching_jobs[["user_id", "account", "job_name"]].drop_duplicates()

# Filter all jobs matching the selected user-account-job_name pairs
df_filtered_users = df_filtered_456.merge(matching_user_accounts, on=["user_id", "account", "job_name"], how="inner")
df_filtered_users["year_month"] = df_filtered_users["start_year"].astype(str) + "-" + df_filtered_users["start_month"].astype(str).str.zfill(2)

# Aggregate power_mean per node range per month
monthly_node_stats = {}
for _, row in df_filtered_users.iterrows():
    year_month = row["year_month"]
    nodes = row["nodes"]
    power_mean = row["power_mean"]
    queue_type = "normal" if row["queue_name"] == "normal" else "not_normal"

    if year_month not in monthly_node_stats:
        monthly_node_stats[year_month] = {
            key: {"normal": {"count": 0, "power_means": []},
                  "not_normal": {"count": 0, "power_means": []}} for key in node_ranges
        }

    for node in nodes:
        node_number = int(node.replace("node", ""))
        for range_name, node_range in node_ranges.items():
            if node_number in node_range:
                monthly_node_stats[year_month][range_name][queue_type]["count"] += 1
                monthly_node_stats[year_month][range_name][queue_type]["power_means"].append(power_mean)
                break

# Create a DataFrame from monthly statistics
df_power_means = []
for year_month, month_data in monthly_node_stats.items():
    for node_range, queue_data in month_data.items():
        df_power_means.append({
            "year_month": year_month,
            "node_range": node_range,
            "normal": np.nanmean(queue_data["normal"]["power_means"]) if queue_data["normal"]["power_means"] else np.nan,
            "not_normal": np.nanmean(queue_data["not_normal"]["power_means"]) if queue_data["not_normal"]["power_means"] else np.nan
        })

df_power_means = pd.DataFrame(df_power_means)
df_power_means["node_range"] = df_power_means["node_range"].map(node_ranges)

# Pivot for heatmap plotting
df_pivot_normal = df_power_means.pivot(index="year_month", columns="node_range", values="normal")
df_pivot_not_normal = df_power_means.pivot(index="year_month", columns="node_range", values="not_normal")

# Shared color scale
vmin = min(df_pivot_normal.min().min(), df_pivot_not_normal.min().min())
vmax = max(df_pivot_normal.max().max(), df_pivot_not_normal.max().max())
cmap = plt.get_cmap("YlOrRd").copy()
cmap.set_bad(color='black')

# Draw and save heatmap for normal queue
plt.figure(figsize=(9, 4.8))
ax = sns.heatmap(
    df_pivot_normal,
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    annot=False,
    linewidths=0.5,
    cbar_kws={"label": "Per-node Avg.\nJob Power (W)"}
)
ax.set_xlabel("Node Range", fontsize=24, fontweight='bold')
ax.set_ylabel("Year-Month", fontsize=24, fontweight='bold')
ax.tick_params(axis="both", labelsize=18)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("./results/power_456.pdf")
plt.close()

# Draw and save heatmap for non-normal queue
plt.figure(figsize=(9, 4.8))
ax = sns.heatmap(
    df_pivot_not_normal,
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    annot=False,
    linewidths=0.5,
    cbar_kws={"label": "Per-node Avg.\nJob Power (W)"}
)
ax.set_xlabel("Node Range", fontsize=24, fontweight='bold')
ax.set_ylabel("Year-Month", fontsize=24, fontweight='bold')
ax.tick_params(axis="both", labelsize=18)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("./results/power_non_normal_456.pdf")
plt.close()
