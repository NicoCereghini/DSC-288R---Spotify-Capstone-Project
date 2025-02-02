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


def deduplicate(connection, df):
    #Convert the artist column to a type that allows for similarity checks in dedup process
    df['artists'] = df['artists'].apply(tuple)
    df_deduplicated = df.drop_duplicates(subset=['name', 'artists'], keep='first')
    
    # Left Anti-join: Get rows in df_original that are NOT in df_deduplicated i.e. the dupes
    df_duplicates = df.merge(df_deduplicated, on=["name", "artists"], how="left", indicator=True)

    df_to_delete = df_duplicates[df_duplicates["_merge"] == "left_only"][["id"]]
    
    delete_statements = [f"DELETE FROM your_table WHERE id = '{row['id']}';" for _, row in df_to_delete.iterrows()]
    
    # Loop through each delete statement and execute it
    for stmt in delete_statements:
        delete(connection, stmt)             
    return 

# Call after deduplication and before clean data (for efficiency)
def outlier_removal(connection,df):
    # Remove tracks with durations longer than 20 min - 1000 tracks removed
    return
    
def clean_data(connection,df):
    # Decade Binning
    # Combined feature index creation
    # Add columns to db - DONT OVERWRITE ROWS
    return
    