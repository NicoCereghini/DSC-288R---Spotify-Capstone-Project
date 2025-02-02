import psycopg2
from psycopg2 import sql

def connect_to_spotify_dataset(host="ucsd-postgresql-sfo2-do-user-18847016-0.m.db.ondigitalocean.com", 
        port="25060", database="spotify_dataset", user="doadmin", password="AVNS_kLeTuGCSss8LYr4Ocrp"):
    """Connects to a PostgreSQL database and returns the connection object."""
    try:
        # Establish the connection
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        print("Connection successful")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
    
def select(connection, query):
    try:
        with connection.cursor() as cursor:
            # Example query: Retrieve data from a table
            cursor.execute(query)
            rows = cursor.fetchall()  # Fetch all results
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
    finally:
        connection.close()
        print("Connection closed.")
        return rows

def delete(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()  # Commit the transaction to apply changes
            print(f"Successfully deleted rows with query: {query}")
    except psycopg2.Error as e:
        print(f"Error executing delete query: {e}")
    finally:
        connection.close()
        print("Connection closed.")


def deduplicate_and_outlier_removal(connection):
    tds = select(connection, "SELECT * FROM track_data") 

    columns = [
    "id", "name", "popularity", "duration_ms", "explicit", "artists", "id_artists", "release_date",
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
    df_duplicates = df.merge(df_deduplicated, on=["name", "artists"], how="left", indicator=True)

    df_to_delete = df_duplicates[df_duplicates["_merge"] == "left_only"][["id"]]
    
    delete_statements = [f"DELETE FROM track_data WHERE id = '{row['id']}';" for _, row in df_to_delete.iterrows()]
    
    # Loop through each delete statement and execute it
    for stmt in delete_statements:
        delete(connection, stmt)             
    return 


def clean_data(connection,df):
    
    # Decade Binning
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year
    df["decade"] = (df["release_year"] // 10) * 10
    
    # Combined feature index creation
    df["mood_index"] = 0.5 * df["valence"] + 0.3 * df["danceability"] + 0.2 * df["energy"]
    df["emotion_index"] = 0.4 * df["valence"] + 0.3 * df["energy"] + 0.3 * df["loudness"].abs()
    df["party_index"] = 0.5 * df["danceability"] + 0.5 * df["energy"]
    df["chill_index"] = 0.6 * df["acousticness"] + 0.4 * (1 - df["energy"])

    # Add new columns to the PostgreSQL table
    add_columns_query = """
    ALTER TABLE your_table 
    ADD COLUMN IF NOT EXISTS decade INT,
    ADD COLUMN IF NOT EXISTS mood_index FLOAT,
    ADD COLUMN IF NOT EXISTS emotion_index FLOAT,
    ADD COLUMN IF NOT EXISTS party_index FLOAT,
    ADD COLUMN IF NOT EXISTS chill_index FLOAT;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(add_columns_query)
            connection.commit()
    except psycopg2.Error as e:
        print(f"Error altering table: {e}")

    # Prepare batch update query
    update_query = """
        UPDATE your_table
        SET 
            decade = %s,
            mood_index = %s,
            emotion_index = %s,
            party_index = %s,
            chill_index = %s
        WHERE id = %s;
    """

    # Create list of tuples for batch update
    update_values = df[["decade", "mood_index", "emotion_index", "party_index", "chill_index", "id"]].values.tolist()

    try:
        with connection.cursor() as cursor:
            execute_batch(cursor, update_query, update_values)  # Execute batch updates
            connection.commit()
    except psycopg2.Error as e:
        print(f"Error updating database: {e}")

    print("Database update complete.")
    
    return df
    