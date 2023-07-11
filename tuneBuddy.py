import requests

url = 'https://api.musixmatch.com/ws/1.1/'
API_KEY = '236e0d15c2fdc11e1d9ffc90054e9c0b'

def songFinder(lyrics):
    params = {
        'apikey': API_KEY,
        'q_lyrics': lyrics,
        'q_track': '',
        'f_has_lyrics': 1,
        's_track_rating': 'desc',
        'page_size': 10,
        'page': 1
    }

    response = requests.get(url + 'track.search', params=params)

    if response.status_code == 200:
        data = response.json()
        track_list = data["message"]["body"]["track_list"]
        possible_songs = []
        if not(track_list == []):
            for i in range(3):
                track_name = data["message"]["body"]["track_list"][i]["track"]["track_name"]
                track_artist = data["message"]["body"]["track_list"][i]["track"]["artist_name"]
                song = track_name + " By: " + track_artist
                possible_songs.append(song)
        return possible_songs
