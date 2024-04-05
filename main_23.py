import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input('which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')

URL = 'https://www.billboard.com/charts/hot-100/'
url_dates = f'{URL}{date}/'
print(url_dates)
response = requests.get(url_dates)
page = response.text
soup = BeautifulSoup(page, 'html.parser')

songs = soup.select(selector= 'li ul li h3')
list_songs = [song.getText().strip() for song in songs]
print(len(list_songs))

client_id = 'fafbd41f09fd453a923db4bfd137ac73'
client_secret = 'd4da107bcc2d436e9659daf7d8f1eb3e'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username='Crypto Wolf', 
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in list_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
        
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)