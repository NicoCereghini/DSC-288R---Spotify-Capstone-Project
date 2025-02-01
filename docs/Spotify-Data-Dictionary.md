# Spotify Dataset (1921-2020) - Data Dictionary

## Overview

This dataset contains over **600,000 tracks** from **Spotify** spanning from **1921 to 2020**. It includes metadata, popularity scores, and various audio features that help analyze music trends over time.

## Columns & Descriptions

| Column Name    | Data Type | Description                                                             |
| -------------- | --------- | ----------------------------------------------------------------------- |
| `id`           | `string`  | Unique identifier for each track on Spotify.                            |
| `name`         | `string`  | Name of the track.                                                      |
| `artists`      | `string`  | List of artist(s) who performed the track.                              |
| `album`        | `string`  | Album name in which the track appears.                                  |
| `release_date` | `string`  | Release date of the track (YYYY-MM-DD or YYYY-MM format).               |
| `duration_ms`  | `integer` | Duration of the track in milliseconds.                                  |
| `explicit`     | `boolean` | Indicates whether the track contains explicit lyrics (1 = Yes, 0 = No). |
| `popularity`   | `integer` | Popularity score of the track (0-100), based on Spotify's algorithm.    |

### **Audio Features**

These features are extracted from Spotify's audio analysis and describe the musical and acoustic properties of each track.

| Column Name        | Data Type | Description                                                                                   |
| ------------------ | --------- | --------------------------------------------------------------------------------------------- |
| `danceability`     | `float`   | Measures how suitable a track is for dancing (0.0 = least danceable, 1.0 = most danceable).   |
| `energy`           | `float`   | Represents intensity and activity of the track (0.0 = low energy, 1.0 = high energy).         |
| `key`              | `integer` | The key of the track (0 = C, 1 = C#/Db, 2 = D, ..., 11 = B).                                  |
| `loudness`         | `float`   | The overall loudness of the track in decibels (dB). Negative values indicate quieter songs.   |
| `mode`             | `integer` | 0 = Minor key, 1 = Major key.                                                                 |
| `speechiness`      | `float`   | Detects the presence of spoken words in a track (higher values = more spoken content).        |
| `acousticness`     | `float`   | Measures how acoustic a track is (0.0 = not acoustic, 1.0 = completely acoustic).             |
| `instrumentalness` | `float`   | Predicts whether a track has vocals (values closer to 1.0 suggest more instrumental content). |
| `liveness`         | `float`   | Estimates the presence of a live audience (values above 0.8 indicate live performances).      |
| `valence`          | `float`   | Describes the musical positivity of the track (0.0 = sad/negative, 1.0 = happy/positive).     |
| `tempo`            | `float`   | Estimated tempo of the track in beats per minute (BPM).                                       |
| `time_signature`   | `integer` | Time signature of the track (e.g., 3 = waltz, 4 = common time).                               |

### **Additional Metadata**

| Column Name | Data Type | Description                                |
| ----------- | --------- | ------------------------------------------ |
| `year`      | `integer` | Year in which the track was released.      |
| `genre`     | `string`  | Primary genre of the track (if available). |

## Notes

- Some tracks might have missing values in `genre` as not all tracks are tagged with a genre.
- The `popularity` metric is dynamic and changes over time.
- `tempo` is an estimated value and might not match the exact BPM of the song.

## Source

Dataset retrieved from Kaggle: [Spotify Dataset 1921-2020, 600k+ Tracks](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks)
