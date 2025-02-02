# Data Transformation Steps

## Overview

This document outlines the data transformation steps involved in processing the dataset. Each step details its purpose, input and output signatures, dependencies, and tools used.

## Transformation Steps

| Step    | Purpose of Step                           | Input Signature                                                   | Input Providing Step       | Output Signature                                           | Tool Used                                                   |
| ------- | ----------------------------------------- | ----------------------------------------------------------------- | -------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------- |
| Step 1  | Format Kaggle dataset for PostgreSQL      | Entire raw data (CSV)                                             | None, first transformation | CSV with reformatted data                                  | Pandas                                                      |
| Step 2  | Ingestion to PostgreSQL database          | Entire data (CSV)                                                 | Step 1                     | "track_data" table with dataset converted to schema format | PostgreSQL                                                  |
| Step 3  | Extraction                                | PostgreSQL table "track_data"                                     | Step 2                     | DataFrame with dataset in pandas supported types           | [connection.py](connection.py)                              |
| Step 4  | Deduplication                             | (Dataframe, "name", "artists")                                    | Step 3                     | DataFrame with reduced records                             | Pandas                                                      |
| Step 5  | Add column “decade”                       | (Dataframe, "release_date", "release_year")                       | Step 4                     | DataFrame with New Feature "decade"                        | Pandas                                                      |
| Step 6  | Add column “mood_index”                   | (Dataframe, "valence", "danceability", "energy")                  | Step 5                     | DataFrame with New Feature "mood_index"                    | Pandas                                                      |
| Step 7  | Add column “emotion_index”                | (Dataframe, "valence", "loudness", "energy")                      | Step 6                     | DataFrame with New Feature "emotion_index"                 | Pandas                                                      |
| Step 8  | Add column “party_index”                  | (Dataframe, "danceability", "energy")                             | Step 7                     | DataFrame with New Feature “party_index”                   | Pandas                                                      |
| Step 9  | Add column ‘chill_index”                  | (Dataframe, "acousticness", "energy")                             | Step 8                     | DataFrame with New Feature "chill_index”                   | Pandas                                                      |
| Step 10 | Ingestion of new features into PostgreSQL | (Dataframe, "decade", "mood_index", “party_index”, "chill_index”) | Step 8                     | track_data table with New Features for each record         | Python-defined helper module [connection.py](connection.py) |

## Notes

- Steps can be modified or expanded based on new requirements.
- Tools used may vary depending on specific implementations and optimizations.

## Source

This table serves as a structured documentation of data transformation for better reproducibility and pipeline tracking.
