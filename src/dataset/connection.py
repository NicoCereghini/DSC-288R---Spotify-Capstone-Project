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
            deletions = cursor.fetchall()
            print(f"Successfully deleted rows with query: {query}")
    except psycopg2.Error as e:
        print(f"Error executing delete query: {e}")
    finally:
        connection.close()
        print("Connection closed.")
        return deletions
        
def add_columns(connection,query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except psycopg2.Error as e:
        print(f"Error adding columns to table: {e}")
        
def batch_update(connection,query,update_values):
    try:
        with connection.cursor() as cursor:
            execute_batch(cursor, query, update_values)  # Execute batch updates
            connection.commit()

            updates = cursor.fetchall()
            
    except psycopg2.Error as e:
        print(f"Error updating database: {e}")
        
    finally:
        connection.close()
        print("Connection closed.")
        return deletions
    print("Database update complete.")
    return updates

