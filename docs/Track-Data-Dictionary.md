# Data Dictionary: `track_data` Table

## Overview

The `track_data` table contains a modified version of the Spotify dataset from Kaggle, storing track metadata, popularity, and audio features. The table is structured for efficient querying in a **PostgreSQL cluster**. The data types mentioned in the following dictionary are the supported data types in PostgreSQL.

## Columns & Descriptions

| Column Name    | Data Type | Nullable | Description                                                                        |
| -------------- | --------- | -------- | ---------------------------------------------------------------------------------- |
| `id`           | `text`    | NOT NULL | Unique identifier for each track on Spotify.                                       |
| `name`         | `text`    | NOT NULL | Name of the track.                                                                 |
| `popularity`   | `integer` | Yes      | Popularity score of the track (0-100), based on Spotify's algorithm.               |
| `duration_ms`  | `integer` | Yes      | Duration of the track in milliseconds.                                             |
| `explicit`     | `boolean` | Yes      | Indicates whether the track contains explicit lyrics (`true` = Yes, `false` = No). |
| `artists`      | `text[]`  | Yes      | Array of artist names associated with the track.                                   |
| `id_artists`   | `text[]`  | Yes      | Array of unique artist IDs on Spotify.                                             |
| `release_date` | `text`    | Yes      | Release date of the track (formatted as YYYY-MM-DD or YYYY-MM).                    |

### **Audio Features**

These numerical attributes describe various musical properties of the track.

| Column Name        | Data Type          | Nullable | Description                                                                                   |
| ------------------ | ------------------ | -------- | --------------------------------------------------------------------------------------------- |
| `danceability`     | `double precision` | Yes      | Measures how suitable a track is for dancing (0.0 = least danceable, 1.0 = most danceable).   |
| `energy`           | `double precision` | Yes      | Represents intensity and activity of the track (0.0 = low energy, 1.0 = high energy).         |
| `key`              | `integer`          | Yes      | The key of the track (0 = C, 1 = C#/Db, ..., 11 = B).                                         |
| `loudness`         | `double precision` | Yes      | The overall loudness of the track in decibels (dB). Negative values indicate quieter songs.   |
| `mode`             | `boolean`          | Yes      | Indicates major (`true`) or minor (`false`) key.                                              |
| `speechiness`      | `double precision` | Yes      | Detects the presence of spoken words in a track (higher values = more spoken content).        |
| `acousticness`     | `double precision` | Yes      | Measures how acoustic a track is (0.0 = not acoustic, 1.0 = completely acoustic).             |
| `instrumentalness` | `double precision` | Yes      | Predicts whether a track has vocals (values closer to 1.0 suggest more instrumental content). |
| `liveness`         | `double precision` | Yes      | Estimates the presence of a live audience (values above 0.8 indicate live performances).      |
| `valence`          | `double precision` | Yes      | Describes the musical positivity of the track (0.0 = sad/negative, 1.0 = happy/positive).     |
| `tempo`            | `double precision` | Yes      | Estimated tempo of the track in beats per minute (BPM).                                       |
| `time_signature`   | `integer`          | Yes      | Time signature of the track (e.g., 3 = waltz, 4 = common time).                               |

## Indexes

- **Primary Key:** `"track_data_pkey"` (btree index on `id`).

## Notes

- Some tracks may have missing values in `popularity`, `artists`, or audio features.
- `mode` is now a boolean (`true` for major, `false` for minor), instead of an integer.
- The `artists` and `id_artists` columns are stored as arrays, making it easier to query multiple associated artists.

## Source

This dataset is a modified version of the Kaggle dataset: [Spotify Dataset 1921-2020, 600k+ Tracks](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks).
