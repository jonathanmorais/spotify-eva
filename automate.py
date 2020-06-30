import json
import os
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from secrets import user_id, token


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like"
    )
    response = request.execute()

    for item in response["items"]:
        video_title = item['snippet']['title']
        youtube_id = "https://www.youtube.com/watch?v={}".format(item['id'])
        
        #extract info from videos without download
        video = youtube_dl.YoutubeDL({'nocheckcertificate': True}).extract_info(youtube_id, download=False)

        song   = video['track']
        artist = video['artist']

        songs_info[video_title] = {
            "youtube_id": youtube_id,
            "song": song,
            "artist": artist
        }


def spotify(song, artist):
    query = "https://api.spotify.com/v1/search?q={}&type={}%2Cartist&market=US&limit=10&offset=5".format(song, artist)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    response_json = response.json()
    songs = response_json["tracks"]["items"]

    uri = songs[0]["uri"]
    return uri 

def create_playlist():

    requests_body = json.dumps({
        "name": "Youtube Videos",
        "description": "Description",
        "public": False
    })

    query  = "https://api.spotify.com/v1/playlist/{}/tracks".format(user_id)

    response = requests.post(
        query,
        data=requests_body,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )


    response_json = response.json()

    return response_json['id']

       
def add_song():
    youtube()

    uris = []
    for song, info in youtube.songs_info.items():
        spotify_url = spotify(info['song_name'], info['artist'])
        uris.append(spotify_url)

    playlist_id = create_playlist()

    request_data = json.dumps(uris)
    query        = "https://api.spotify.com/v1/playlist/{}/tracks".format(playlist_id)

    response = requests.post(
        query,
        data=request_data,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    response_json = response.json()

    return response_json['id']
