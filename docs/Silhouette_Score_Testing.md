# 🚀 DigitalOcean Droplet Performance Log

This document tracks the performance of different droplet configurations while calculating the silhouette score on a 500K Spotify track dataset.

## 📊 Droplet Testing Log

| **Dataset Size** | **Partitions Used** | **Droplet Type**                           | **Total Execution Time (s)** |
| ---------------- | ------------------- | ------------------------------------------ | ---------------------------- |
| 500,000          | 4                   | Standard (1vCPU, 1GB RAM) $0.012/hour      | 344.21s                      |
| 500,000          | 6                   | Standard (1vCPU, 1GB RAM) $0.012/hour      | 237.52s                      |
| 500,000          | 8                   | Standard (1vCPU, 1GB RAM) $0.012/hour      | 192.02s                      |
| 500,000          | 10                  | Standard (1vCPU, 1GB RAM) $0.012/hour      | 170.53s                      |
| 500,000          | 12                  | Standard (1vCPU, 1GB RAM) $0.012/hour      |                              |
| 500,000          | 16                  | CPU-Optimized (2vCPU, 4GB RAM) $0.048/hour |                              |

## 🛠️ Notes

- **Goal:** Identify the optimal number of partitions and droplet configuration for silhouette score calculations.
- **Metrics to Track:** Execution time, cost efficiency, and consistency.
- **Next Steps:** Start with 4-6 standard droplets and scale based on performance observations.

🔍 **Observations**:

- \*\*\*Increasing paritions only helps LOL.
- \*\*\*I have a droplet limit of 10. I requested an increase to 16
