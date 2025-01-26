import asyncio
from requests import post
import json
import sys
from pathlib import Path

# The below makes calling the dataset module possible
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from dataset.connection import connect_to_spotify_dataset
from dataset.connection import select
from api_helpers.api_utils import get_token
from api_helpers.api_utils import refresh_token
from api_helpers.api_utils import get_albums_for_artists
from api_helpers.api_utils import get_tracks_for_album

async def main():
    print("Starting application...")
    # Start the token refresher task
    connection = connect_to_spotify_dataset()
    if not connection:
        return
    
    token = await get_token()

    # The below is TEST ingestion logic
    tds = select(connection, "SELECT artists, id_artists FROM track_data LIMIT 1") 
    print("Data returned from db: ",tds)
    artists = tds[0][1] # get the first row of artists
    albums = await get_albums_for_artists(token, artists)
    print("Got the albums. Now fetching tracks...")
    for album in albums:
        tracks = await get_tracks_for_album(token, album)
        for track in tracks:
            #Harvest the attributes for a track
            #Upload to the cluster
            print("publising track: "+track["name"]+"to cluster")

    # End of TEST ignition logic
    asyncio.create_task(refresh_token())
    print("Starting ingestion...")

    # Main ingestion logic
    '''
    while True:
        print("The main ingestion is running.")
        await asyncio.sleep(5)  # Simulate other work in the main application
    '''

if __name__ == "__main__":
    asyncio.run(main())  # Starts the asyncio event loop and runs the main coroutine
