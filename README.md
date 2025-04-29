# Uncovering Power Consumption Variability in Production HPC Systems

This repository provides the artifact for the SC'25 paper titled:

**"Uncovering Power Consumption Variability in Production HPC Systems through Application and Node-Level Empirical Analysis"**

The artifact includes all scripts and resources necessary to reproduce the figures and results from our paper, which investigates job-level and node-level power consumption variability in a production HPC system.

---

## Overview

This work presents an empirical analysis of power consumption variability in a real-world HPC system ranked 11th on the TOP500 list. Our analysis focuses on:

- Temporal factors (month, day, time-of-day)
- Node characteristics (architecture, allocation scale)
- Application behavior (configuration, user-defined options, exit status)
- Node placement effects via clustering-based analysis

We propose a two-stage clustering method that reveals hidden spatial imbalance in node usage and its influence on power efficiency.

---

## Key Contributions

- **C1**: Temporal variability analysis (month, day of week, time-of-day)
- **C2**: Node architecture and allocation scale-based power variability
- **C3**: Application-specific and user-level configuration impacts
- **C4**: Cluster-based analysis revealing spatial power variability across node ranges

---

## Artifact Contents

| File | Description |
|------|-------------|
| `monthly_job_distribution.pdf`, `queue_power.pdf`, `week_power_wait.pdf`, `wait_power.pdf` | Power variability over time and queues (C1) |
| `node_type_distribution.pdf`, `node_count_distribution.pdf`, `node_count_cdf.pdf` | Node architecture and allocation scale analysis (C2) |
| `application_distribution.pdf`, `user_vasp_distribution.pdf`, `vasp_exit.pdf` | User configuration and exit status effects within application (C3) |
| `gaussian_same.pdf`, `gaussian_power.pdf`, `gaussian_power2.pdf` | Intra-cluster per-node job power variability |
| `high_power_node.pdf`, `low_power_node.pdf`, `normal_stack.pdf`, `all_stack.pdf` | Job power distribution across node ranges (C4) |
| `normal_node_monthly.pdf`, `non_normal_node_monthly.pdf`, `power_456.pdf`, `power_non_normal_456.pdf` | Temporal node-range-specific power analysis (C4) |

---

## Setup Instructions

### Hardware Requirements

- CPU: Intel Core i5-12400 (6 cores, 12 threads)
- RAM: 64 GB

### Software Requirements

| Package     | Version |
|-------------|---------|
| Python      | 3.9.19  |
| seaborn     | 0.13.2  |
| numpy       | 1.26.4  |
| pandas      | 2.2.2   |
| matplotlib  | 3.8.4   |

---

## Workflow

The artifact consists of the following main tasks:

| Task | Description |
|------|-------------|
| `T1` | Load input data, preprocess, compute per-node job power |
| `T2` | Analyze temporal, node-level, and application-level variability |
| `T3` | Perform two-stage clustering and analyze spatial variability |


All output `.pdf` files will be saved in the `results/` directory.

---

## Expected Execution Time

| Stage | Estimated Time |
|-------|----------------|
| Setup (package installation) | ~5 minutes |
| Task T1 + T2 + T3            | ~87 minutes total |

---

## Dataset Description

- **System**: 8,437 compute nodes (Intel Xeon Phi 7250 [KNL] and Intel Xeon Gold 6148 [SKL])
- **Period**: September 19, 2023 – June 30, 2024
- **Power data**: Collected at 1-minute intervals from chassis-level power supplies
- **Job/system metadata**: Extracted from PBSPro and Lustre Monitoring Tool (LMT)

---
