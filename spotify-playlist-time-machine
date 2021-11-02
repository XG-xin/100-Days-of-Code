from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

response = requests.get(URL + date)

soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
songs_list = [song.getText() for song in songs]
print(songs_list)

scope = "user-library-read,playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))

user_id = sp.current_user()["id"]

uri_list = []
for item in songs_list:
    urn = f"track: {item} year: 2010"
    try:
        a = sp.search(urn)["tracks"]["items"][0]["uri"]
        uri_list.append(a)
    except IndexError:
        print(f"{item} is not aviliable.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)
sp.playlist_add_items(playlist["id"], items=uri_list)
