# DSC-288R---Spotify-Capstone-Project

This project is an analysis of 3 clustering approaches based on emotion used for playlist generation using Spotify API track metadata. :musical_note: :headphones:

### :fire: Steps to Run :fire: :rocket:

1. Ensure ```security_details.json``` is in the dataset folder. The tokens here are REQUIRED to fetch any data from the database or create compute for the silhouette score computation.
2. Go to the notebooks folder. <b>The following notebooks are ok to run:</b>

- eda.ipynb
- baseline-models.ipynb
- k-means.ipynb
- SoM.ipynb

<b> \*\*You must run all the cells in order for each notebook. Running cells out of order raises a high chance that things will break!\*\*</b>

For a demo of the sihlouette score calculation, simply run the "distributed_sihlouette.py" file.

### Droplet Issues
If you see an error when trying to compute the silhouette score that contains a phrase like "creating droplets will exceed your droplet limit", in a new cell please use an instance of the ```DistributedSilhouette``` class to run ```delete_all_droplets(self, api_token)``` with the result of calling the other instance function ```fetch_di_secret()```.

For examplem if your DistributedSilhouette object is called "distributed_silhouette", run ```distributed_silhouette.delete_all_droplets(fetch_di_secret()) ```
and then retry computing the silhouette score after it finishes deleting the clones. This is very unlikely to happen, but just incase :)
