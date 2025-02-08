import psycopg2
import json
import os
from psycopg2 import sql
from psycopg2 import extras

def connect_to_spotify_dataset(json_file='security_details.json'):
    """Connects to a PostgreSQL database and returns the connection object."""
    try:
        # Resolve the path relative to the current file (connection.py)
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, json_file)

        # Load connection parameters from JSON file
        with open(json_path, 'r') as file:
            config = json.load(file)
        
        # Establish the connection
        connection = psycopg2.connect(
            host=config.get('host'),
            port=config.get('port'),
            database=config.get('database'),
            user=config.get('user'),
            password=config.get('password')
        )
        print("Connection successful")
        return connection
    except FileNotFoundError:
        print(f"Error: The file '{json_file}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file}' contains invalid JSON.")
        return None
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
    except psycopg2.Error as e:
        print(f"Error executing delete query: {e}")
    finally:
        connection.close()
        print("Connection closed.")
        return 
        
def add_columns(connection,query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except psycopg2.Error as e:
        print(f"Error adding columns to table: {e}")
    finally:
        print("Added Columns to db")
        return 
        
def batch_update(connection,query,update_values):
    try:
        with connection.cursor() as cursor:
            extras.execute_batch(cursor, query, update_values)  # Execute batch updates

            connection.commit()
            
    except psycopg2.Error as e:
        print(f"Error updating database: {e}")
        
    finally:
        connection.close()
        print("Connection closed.")
        print("Database update complete.")
        return

