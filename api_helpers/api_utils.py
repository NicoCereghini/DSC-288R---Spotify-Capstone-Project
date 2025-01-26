import base64
import aiohttp

client_id = "021a86cb66bd46c5a327ef75abd802f3"
client_secret = "ce920fd1efd948e69cf0e2794a54cd84"
token = ""  # This will be set by the token fetcher

async def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            json_result = await response.json()  # Parse the JSON response
            token = json_result["access_token"]
            return token

async def refresh_token():
    while True:
        print("Refreshing token...")
        # Replace the following with your token fetching logic
        token = await get_token()  # token fetch
        print("Token refreshed.")
        print("Token is:", token)
        await asyncio.sleep(10*60)  # Wait for 10 minutes before refreshing again (10*60)


def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

async def call_api(url, headers):
    async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()  # Parse JSON response
                    return data
                else:
                    print(f"Failed to fetch albums: {response.status}")
                    error_text = await response.text()
                    print(f"Error details: {error_text}")
                    return None
                
async def get_albums_for_artists(token, artist_ids):
    # artist_ids is a list, so we need to iterate over it
    albums = []
    for artist_id in artist_ids:
        # Fetch the albums for the artist
        artist_albums = await get_albums_for_artist(token, artist_id)
        #print("Albums for artist", artist_id, ":\n", artist_albums)
        # Get the "name" field from all indices in artist_albums in an array
        album_names = [album["id"] for album in artist_albums]
        albums.extend(album_names)
    return albums

async def get_albums_for_artist(token, artist_id):
    # lets first get the albums for the artist to spread our net wide!
    url = "https://api.spotify.com/v1/artists/"+artist_id+"/albums"
    headers = get_auth_headers(token)
    data = await call_api(url, headers)
    return data["items"]

async def get_tracks_for_album(token, album_id):
    url = "https://api.spotify.com/v1/albums/"+album_id+"/tracks"
    headers = get_auth_headers(token)
    data = await call_api(url, headers)
    return data["items"]