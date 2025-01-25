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