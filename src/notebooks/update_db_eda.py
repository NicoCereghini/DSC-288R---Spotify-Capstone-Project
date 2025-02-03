# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ### This file updates the postgres database with the preprocessing and cleaning of features - make sure to input database password into the psycopg2 connections

# +
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
# -

connection = connect_to_spotify_dataset() #Insert db password
if not connection:
    print("Connection Error")
tds = select(connection, "SELECT * FROM track_data") 

# +
columns = ["id", "name", "popularity", "duration_ms", "explicit", "artists", "id_artists", "release_date",
"danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", 
"instrumentalness", "liveness", "valence", "tempo", "time_signature"]
    
# Create the DataFrame
df = pd.DataFrame(tds, columns=columns)
    
# Remove tracks with durations longer than 20 min - ~1000 tracks removed
df2 = df[df["duration_ms"] <= 20 * 60 * 1000]
    
#Convert the artist column to a type that allows for similarity checks in dedup process
df2['artists'] = df2['artists'].apply(tuple)
df_deduplicated = df2.drop_duplicates(subset=['name', 'artists'], keep='first')
    
# Left Anti-join: Get rows in df that are NOT in df_deduplicated i.e. the dupes and outliers
df_duplicates = df.merge(df_deduplicated, on="id", how="left", indicator=True)

df_to_delete = df_duplicates[df_duplicates["_merge"] == "left_only"][["id"]]
delete_ids = tuple(df_to_delete['id'].tolist())

connection = connect_to_spotify_dataset() #Insert db password
if not connection:
    print("Connection Error")
delete(connection, f"DELETE FROM track_data WHERE id in {delete_ids}")


# +
# Decade Binning
def standardize_date(date_str):
    try:
        # Try to parse the full date format (e.g., '1928-01-01')
        return pd.to_datetime(date_str, format='%Y-%m-%d')
    except ValueError:
        try:
            # If it only contains year and month (e.g., '1956-03'), add '-01' for the day
            return pd.to_datetime(date_str + '-01', format='%Y-%m-%d')
        except ValueError:
            # If it only contains the year, create a date with January 1st
            return pd.to_datetime(date_str + '-01-01', format='%Y-%m-%d')
            
df_deduplicated['release_date'] = df_deduplicated['release_date'].apply(standardize_date)            
df_deduplicated["release_date"] = pd.to_datetime(df_deduplicated["release_date"])
df_deduplicated["release_year"] = df_deduplicated["release_date"].dt.year
df_deduplicated["decade"] = (df_deduplicated["release_year"] // 10) * 10
df_deduplicated["decade"] = df_deduplicated["decade"].astype(int)

# Combined feature index creation
df_deduplicated["mood_index"] = 0.5 * df_deduplicated["valence"] + 0.3 * df_deduplicated["danceability"] + 0.2 * df_deduplicated["energy"]
df_deduplicated["emotion_index"] = 0.4 * df_deduplicated["valence"] + 0.3 * df_deduplicated["energy"] + 0.3 * df_deduplicated["loudness"].abs()
df_deduplicated["party_index"] = 0.5 * df_deduplicated["danceability"] + 0.5 * df_deduplicated["energy"]
df_deduplicated["chill_index"] = 0.6 * df_deduplicated["acousticness"] + 0.4 * (1 - df_deduplicated["energy"])

connection = connect_to_spotify_dataset() #Insert db password
if not connection:
    print("Connection Error")


# Add new columns to the PostgreSQL table
add_columns_query = """
ALTER TABLE track_data 
ADD COLUMN IF NOT EXISTS decade INT,
ADD COLUMN IF NOT EXISTS mood_index FLOAT,
ADD COLUMN IF NOT EXISTS emotion_index FLOAT,
ADD COLUMN IF NOT EXISTS party_index FLOAT,
ADD COLUMN IF NOT EXISTS chill_index FLOAT;
"""
add_columns(connection,add_columns_query)

# Prepare batch update query
update_query = """
    UPDATE track_data
    SET 
        decade = %s,
        mood_index = %s,
        emotion_index = %s,
        party_index = %s,
        chill_index = %s
    WHERE id = %s;
"""

# Create list of tuples for batch update
update_values = list(map(tuple, df_deduplicated[["decade", "mood_index", "emotion_index", "party_index", "chill_index", "id"]].values))
batch_update(connection,update_query,update_values)
