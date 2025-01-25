import base64
import asyncio
import aiohttp
from requests import post
import json

client_id = "021a86cb66bd46c5a327ef75abd802f3"
client_secret = "ce920fd1efd948e69cf0e2794a54cd84"

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


def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"

async def refresh_token():
    while True:
        print("Refreshing token...")
        # Replace the following with your token fetching logic
        token = await get_token()  # token fetch
        print("Token refreshed.")
        print("Token is:", token)
        await asyncio.sleep(10*60)  # Wait for 10 minutes before refreshing again (10*60)

async def main():
    print("Starting application...")
    # Start the token refresher task
    asyncio.create_task(refresh_token())

    # Main application logic continues here
    while True:
        print("Main application is running.")
        await asyncio.sleep(5)  # Simulate other work in the main application

if __name__ == "__main__":
    asyncio.run(main())  # Starts the asyncio event loop and runs the main coroutine
