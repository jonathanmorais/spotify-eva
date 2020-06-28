import secrets
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'My Opeth'

client_id = secrets.CLIENT_ID
client_secret = secrets.CLIENT_SECRET

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.user_playlists(search_str)
pprint.pprint(result)