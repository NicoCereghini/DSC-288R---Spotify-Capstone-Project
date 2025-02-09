#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:29:52 2025

@author: lianmartin
"""

import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import psycopg2.extras

root_path = Path().resolve().parent.parent
sys.path.append(str(root_path))

from src.dataset.connection import connect_to_spotify_dataset
from src.dataset.connection import select, delete, add_columns, batch_update

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import torch
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
# -

connection = connect_to_spotify_dataset() #Insert db password
if not connection:
    print("Connection Error")
tds = select(connection, "SELECT * FROM track_data") 

columns = [
    "id", "name", "popularity", "duration_ms", "explicit", "artists", "id_artists", "release_date",
    "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", 
    "instrumentalness", "liveness", "valence", "tempo", "time_signature","decade", "mood_index", "emotion_index", "party_index", "chill_index"
]
# Create the DataFrame
df = pd.DataFrame(tds, columns=columns)
df_kmeans = df[['duration_ms', 'tempo', 'decade', 'popularity', 'key', 'emotion_index', 'mode', 'chill_index']]

#pre-proc
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_kmeans)

#df_scaled= df_scaled[0]

#data = torch.tensor(df_scaled, dtype=torch.float32)  #convert to PyTorch tensor

#data = torch.from_numpy(df_scaled).float()

data_tensor = torch.from_numpy(df_scaled).float()
dataset = TensorDataset(data_tensor)
dataloader = DataLoader(dataset, batch_size=10, shuffle=True)  # Adjust batch size as needed

#data = torch.from_numpy(df_scaled).half()


