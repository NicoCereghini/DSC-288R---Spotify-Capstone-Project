import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from multiprocessing import Pool
import digitalocean
import time
import json
import os

# This class is a simple implementation of distributed silhouette score computation using DigitalOcean droplets.
# A good rule of thumb, don't touch these insatnce variables unless you know what you are doing LOL
class DistributedSilhouette:
    def __init__(self, M=10, droplets=None, droplet_size_default="s-1vcpu-1gb"):
        self.M = M
        self.droplets = droplets if droplets is not None else []
        self.droplet_size_default = droplet_size_default
        self.api_token = self.fetch_di_secret()

    def compute_partial_silhouette(self, part_data):
        """Compute silhouette score for a partition with a 1-hour timeout."""
        data, lbls = part_data
        result = silhouette_score(data, lbls)
        return result

    def compute_fast_silhouette(self, partitions, label_partitions):
        """Compute silhouette score in parallel using M droplets."""
        print("Setting up the droplet clones...")
        self.setup_droplets(self.api_token, droplet_count=self.M)

        # Prepare arguments for parallel execution
        partition_args = [(partitions[i], label_partitions[i]) for i in range(self.M)]

        print("We are ready to compute the score in parallel!")
        print("Calculating...")
        with Pool(self.M) as pool:
            partial_scores = pool.map(self.compute_partial_silhouette, partition_args)

        # Calculate global silhouette score
        global_silhouette = sum(partial_scores) / self.M

        print("Done! Cleaning up droplets...")
        self.destroy_droplets(self.droplets)
        
        return global_silhouette

    def split_data(self, data, labels):
        """Split data and labels into M partitions."""
        partitions = np.array_split(data, self.M)
        label_partitions = np.array_split(labels, self.M)
        return partitions, label_partitions

    def setup_droplets(self, api_token, droplet_count, region="sfo2"):
        for i in range(droplet_count):
            droplet = digitalocean.Droplet(
                token=api_token,
                name=f"silhouette-clone-{i}",
                region=region,
                image="ubuntu-22-04-x64",
                size_slug=self.droplet_size_default,
                ssh_keys=[],
                backups=False
            )
            droplet.create()
            self.droplets.append(droplet)
        return self.droplets

    def destroy_droplets(self, droplets):
        """Destroy all droplets."""
        to_remove = []
        for droplet in droplets:
            try:
                droplet.destroy()
                print(f"Destroyed droplet: {droplet.name}")
                if droplet in self.droplets:
                    to_remove.append(droplet)
            except Exception as e:
                print(f"[WARNING] Failed to destroy droplet {droplet.name}: {e}")
        for droplet in to_remove:
            self.droplets.remove(droplet)
        if len(self.droplets) == 0:
            print("Droplets destroyed, you are safe to terminate your code!")
        

    def fetch_di_secret(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
        json_path = os.path.join(parent_dir, "dataset", "security_details.json")
        # Load connection parameters from JSON file
        with open(json_path, 'r') as file:
            config = json.load(file)
        api_token = config.get('do_api_secret')
        return api_token

    def delete_all_droplets(self, api_token):
        """If you accidentally exit your program and need to cleanup running droplets, 
        use this by calling once manually."""
        manager = digitalocean.Manager(token=api_token)
        droplets = manager.get_all_droplets()
        self.destroy_droplets(droplets)

if __name__ == "__main__":
    # Small simulated example
    np.random.seed(42)
    df_scaled = np.random.rand(50000, 13)  # 50k rows, 13 features

    # Fit KMeans once to get labels
    k = 8
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(df_scaled)

    # Create an instance of DistributedSilhouette
    distributed_silhouette = DistributedSilhouette()

    # Split dataset into M partitions
    partitions, label_partitions = distributed_silhouette.split_data(df_scaled, labels)

    # Compute silhouette scores in parallel
    start_parallel = time.perf_counter()
    global_silhouette = distributed_silhouette.compute_fast_silhouette(partitions, label_partitions)
    end_parallel = time.perf_counter()

    print("#############################################")
    print(f"Dataset Size: {len(df_scaled)} M partitions: {distributed_silhouette.M}")
    print(f"Global Silhouette Score (Parallel): {global_silhouette:.4f}")
    print(f"Baseline Silhouette Score: {baseline_silhouette:.4f}")
    print(f"Baseline Time: {end_baseline - start_baseline:.2f} seconds")
    print(f"Parallel Time: {end_parallel - start_parallel:.2f} seconds")
    print(f"Compute just saved you {end_baseline - start_baseline - (end_parallel - start_parallel):.2f} seconds, WOW!!!")
    print("#############################################")