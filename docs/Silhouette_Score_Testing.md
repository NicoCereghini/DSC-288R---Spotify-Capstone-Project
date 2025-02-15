# 🚀 DigitalOcean Droplet Performance Log

This document tracks the performance of different droplet configurations while calculating the silhouette score on a 500K Spotify track dataset.

## 📊 Droplet Testing Log

| **Dataset Size** | **Partitions Used** | **Droplet Type**               | **Total Execution Time (s)** |
| ---------------- | ------------------- | ------------------------------ | ---------------------------- |
| 500,000          | 4                   | Standard (1vCPU, 1GB RAM)      |                              |
| 500,000          | 6                   | Standard (1vCPU, 1GB RAM)      |                              |
| 500,000          | 8                   | Standard (1vCPU, 1GB RAM)      |                              |
| 500,000          | 10                  | Standard (1vCPU, 1GB RAM)      |                              |
| 500,000          | 12                  | Standard (1vCPU, 1GB RAM)      |                              |
| 500,000          | 16                  | CPU-Optimized (2vCPU, 4GB RAM) |                              |

## 🛠️ Notes

- **Goal:** Identify the optimal number of partitions and droplet configuration for silhouette score calculations.
- **Metrics to Track:** Execution time, cost efficiency, and consistency.
- **Next Steps:** Start with 4-6 standard droplets and scale based on performance observations.

🔍 **Observations**:

- ***
- ***
