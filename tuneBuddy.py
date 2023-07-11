import requests

url = 'https://api.musixmatch.com/ws/1.1/'
API_KEY = '236e0d15c2fdc11e1d9ffc90054e9c0b'

def songFinder(lyrics, artist_name = "", genre = ""):
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

    artist_name = artist_name.lower()
    genre = genre.lower()
    if response.status_code == 200:
        data = response.json()
        track_list = data["message"]["body"]["track_list"]
        possible_songs = []
        possible_tracks = []
        if not(track_list == []):
            for i in range(5):
                track = data["message"]["body"]["track_list"][i]["track"]
                possible_tracks.append(track)
            if artist_name == "" and genre == "":
                for i in range(5):
                    track_name = possible_tracks[i]["track_name"]
                    track_artist = possible_tracks[i]["artist_name"]
                    song = track_name + " By: " + track_artist
                    possible_songs.append(song)
            elif not(artist_name == "") and genre == "":
                for i in range(5):
                    track_name = possible_tracks[i]["track_name"]
                    track_artist = possible_tracks[i]["artist_name"]
                    song = track_name + " By: " + track_artist
                    track_artist = track_artist.lower()
                    if track_artist == artist_name:
                        possible_songs.append(song)
            elif artist_name == "" and not(genre == ""):
                for i in range(5):
                    track_name = possible_tracks[i]["track_name"]
                    track_artist = possible_tracks[i]["artist_name"]
                    track_genre = possible_tracks[i]["primary_genres"]["music_genre_list"][0]["music_genre"]["music_genre_name"].lower()
                    song = track_name + " By: " + track_artist
                    if track_genre == genre:
                        possible_songs.append(song)
            elif not(artist_name == "") and not(genre == ""):
                for i in range(5):
                    track_name = possible_tracks[i]["track_name"]
                    track_artist = possible_tracks[i]["artist_name"]
                    track_genre = possible_tracks[i]["primary_genres"]["music_genre_list"][0]["music_genre"]["music_genre_name"].lower()
                    song = track_name + " By: " + track_artist
                    track_artist = track_artist.lower()
                    if track_artist == artist_name and track_genre == genre:
                        possible_songs.append(song)

        if len(possible_songs) == 5 or len(possible_songs) == 4:
            return possible_songs[0:3]
        while not(len(possible_songs) == 3):
            possible_songs.append("None")
        return possible_songs

# print(songFinder("save your tears for another day", "Someone", "Electronic"))