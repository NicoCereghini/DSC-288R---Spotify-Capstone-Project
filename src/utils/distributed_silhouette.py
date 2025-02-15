import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from multiprocessing import Pool
import time
import digitalocean

# Default partitions if the user wishes to use the default value
# TODO: A good rule of thumb, try not to have the rows in a partition exceed the cores accross all droplets
M = 4 

def compute_partial_silhouette(part_data):
    """Compute silhouette score for a partition."""
    data, lbls = part_data
    return silhouette_score(data, lbls)

def compute_fast_silhouette(partitions, label_partitions, M, droplets):
    print("Setting up the army of droplets...")

    # Prepare arguments for parallel execution
    partition_args = [(partitions[i], label_partitions[i]) for i in range(M)]
    print("We are ready to compute the score in parallel!")

    with Pool(M) as pool:
        partial_scores = pool.map(compute_partial_silhouette, partition_args)

    # Calculate global silhouette score
    global_silhouette = sum(partial_scores) / M

    print("Done! Cleaning up droplets...")
    destroy_droplets(droplets)
    print("Droplets destroyed, you are safe to terminate your code!")

    return global_silhouette

def split_data(data, labels, M):
    """Split data and labels into M partitions."""
    partitions = np.array_split(data, M)
    label_partitions = np.array_split(labels, M)
    return partitions, label_partitions

def setup_droplets(api_token, droplet_count, droplet_size="s-1vcpu-1gb", region="nyc3"):
    droplets = []
    for i in range(droplet_count):
        droplet = digitalocean.Droplet(
            token=api_token,
            name=f"kmeans-worker-{i}",
            region=region,
            image="ubuntu-22-04-x64",
            size_slug=droplet_size,
            ssh_keys=[],
            backups=False
        )
        droplet.create()
        droplets.append(droplet)
    return droplets

def destroy_droplets(droplets):
    for droplet in droplets:
        droplet.destroy()



if __name__ == "__main__":

    # Simulate your dataset
    np.random.seed(42)
    df_scaled = np.random.rand(70000, 13)  # 50k rows, 13 features

    # Fit KMeans once to get labels
    k = 8
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(df_scaled)

    # Split dataset into M partitions
    df_scaled = split_data(df_scaled, labels, M=4)

    #Calculate the Baseline Silhouette Score
    start_baseline = time.perf_counter()
    baseline_silhouette = silhouette_score(df_scaled, labels)
    end_baseline = time.perf_counter()

    # Compute silhouette scores in parallel
    start_parallel = time.perf_counter()
    global_silhouette = compute_fast_silhouette(partitions, label_partitions)
    end_parallel = time.perf_counter()

    print("#############################################")
    print(f"Global Silhouette Score (Parallel): {global_silhouette:.4f}")
    print(f"Baseline Silhouette Score: {baseline_silhouette:.4f}")
    print(f"Baseline Time: {end_baseline - start_baseline:.2f} seconds")
    print(f"Parallel Time: {end_parallel - start_parallel:.2f} seconds")
    print(f"Compute just saved you {end_baseline - start_baseline - (end_parallel - start_parallel):.2f} seconds, WOW!!!")
    print("#############################################")
