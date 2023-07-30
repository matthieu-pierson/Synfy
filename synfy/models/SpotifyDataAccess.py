import json
import math

import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta, time
import time


def median_date(data):
    sorted_data = sorted([datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in data])
    n = len(sorted_data)
    if n % 2 == 0:
        median = sorted_data[n // 2 - 1]
    else:
        median = sorted_data[n // 2]
    return datetime.strftime(median, '%Y-%m-%d %H:%M:%S')


def remove_key(obj, bad_key):
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key == bad_key:
                del obj[key]
            else:
                remove_key(obj[key], bad_key)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == bad_key:
                del obj[i]
            else:
                remove_key(obj[i], bad_key)
    else:
        pass


def wait_until(end_datetime):
    end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
    while True:
        diff = (end_datetime - datetime.now()).total_seconds()
        if diff < 0: return
        time.sleep(diff / 2)
        if diff <= 0.1: return


def remove_keys(obj, bad_keys):
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            # print(key)
            for bad_key in bad_keys:
                try:
                    if key == bad_key:
                        del obj[key]
                    else:
                        remove_keys(obj[key], bad_keys)
                except KeyError:
                    # print("Bad key : " + bad_key + " in dict")
                    pass
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            for bad_key in bad_keys:
                try:
                    if obj[i] == bad_key:
                        del obj[i]
                    else:
                        remove_keys(obj[i], bad_keys)
                except KeyError:
                    # print("Bad key : " + bad_key + " in list")
                    pass
    else:
        pass


def is_spotify_premium(client_id, client_secret, redirect_uri, scope):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                  scope=scope))
    try:
        subscription_level = sp.current_user()["product"]
    except KeyError:
        print("Error: Could not retrieve subscription level.")
        return False
    is_premium = (subscription_level == "premium")
    return is_premium


def remove_extra_characters(value):
    return value.replace("(", "").replace(")", "").replace("[", "").replace("]", "")


def get_uris_albums_list(liked_list):
    list_of_songs_uri = {}
    for album in liked_list:
        album_songs = album['album']['tracks']['items']
        for song in album_songs:
            track_artists = []
            for artist in song['artists']:
                # if "/" in artist['name']:
                #     print("artist containing / : ", artist['name'])
                #     new_artist = artist['name'].split("/")
                #     track_artists += new_artist
                # else:
                track_artists.append(artist['name'])
            track_name = song['name']
            add_values_in_dict(list_of_songs_uri, song['uri'], [track_name, sorted(track_artists)])
    return list_of_songs_uri


def get_uris_songs_list(liked_list):
    list_of_songs_uri = {}
    for item in liked_list:
        track_artists = []
        print(item)
        for artist in item['track']['artists']:
            # if "/" in artist['name']:
            #     print("artist containing / : ", artist['name'])
            #     new_artist = artist['name'].split("/")
            #     track_artists += new_artist
            # else:
            track_artists.append(artist['name'])
        track_name = item['track']['name']
        add_values_in_dict(list_of_songs_uri, item['track']['uri'], [track_name, sorted(track_artists)])
    return list_of_songs_uri


def add_values_in_dict(sample_dict, key, list_of_values):
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict


def remove_duplicates_from_dictionary(spotify_library_uris):
    new_dict = {}
    for uri, value in spotify_library_uris.items():
        if value not in new_dict.values():
            print('Add in playlist : ', value[0], ' - ', value[1])
            new_dict[uri] = value
        else:
            print('Already in playlist : ', value[0], ' - ', value[1])
    return new_dict


def remove_local_songs_from_dict(spotify_dict, local_dict):
    final_dict = spotify_dict
    for nb, values in local_dict.items():
        remove_keys_by_value(final_dict, values)
    return final_dict


def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o


def clean_artists(data):
    new_list = []
    for value in traverse(data):
        new_list.append(remove_extra_characters(value).lower())
    return sorted(new_list)


def clean_title(data):
    return remove_extra_characters(data).lower()


def remove_keys_by_value(d, value):
    keys_to_remove = []
    for k, v in d.items():
        v[0] = clean_title(v[0])
        value[0] = clean_title(value[0])
        if v == value:
            keys_to_remove.append(k)
    for k in keys_to_remove:
        del d[k]


def parse_artists(data):
    artists = data['artists']
    artist_names = [artist['name'] for artist in artists]
    return artist_names


class SpotifyDataAccess:
    def __init__(self,propertiesBuilder):
        self.albumList = None
        self.liked_songs_list = None
        self.client_id = propertiesBuilder.client_id
        self.client_secret = propertiesBuilder.client_secret
        self.playlist_id = None
        self.redirect_uri = propertiesBuilder.redirect_uri
        self.scope = "user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative " \
                     "user-follow-read user-read-playback-state user-modify-playback-state user-read-private user-read-email"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=self.redirect_uri,
                                                            scope=self.scope))

    def get_liked_albums(self):
        STEP = 50
        offset = 0
        albums = "Empty"
        liked_albums_list = []
        while albums:
            print(offset)
            results = self.sp.current_user_saved_albums(limit=STEP, offset=offset)
            albums = results['items']
            liked_albums_list += albums
            offset += STEP
        self.albumList = liked_albums_list
        return get_uris_albums_list(liked_albums_list)

    def get_liked_songs(self):
        STEP = 20
        offset = 0
        songs = "Empty"
        liked_songs_list = []
        while songs:
            print(offset)
            results = self.sp.current_user_saved_tracks(limit=STEP, offset=offset)
            songs = results['items']
            liked_songs_list += songs
            offset += STEP
        self.liked_songs_list = liked_songs_list
        return get_uris_songs_list(liked_songs_list)

    def create_playlist_from_uri_list(self, list_uris):
        user_id = self.sp.current_user()["id"]
        playlist_name = "All library w/ duplicates"
        self.delete_spotify_playlist_by_name(playlist_name)
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        chunk_size = 100
        list_uris_chunked = [list_uris[i:i + chunk_size] for i in range(0, len(list_uris), chunk_size)]
        self.playlist_id = playlist["id"]
        for chunk_uris in list_uris_chunked:
            self.sp.playlist_add_items(playlist_id=playlist["id"], items=chunk_uris)

    def get_spotify_song_metadata(self, track_id):
        track_data = json.dumps(self.sp.track(track_id)).replace("'", "\'").replace("True", "true").replace("False",
                                                                                                            "false")  # fix ' in title
        track_data = json.loads(track_data)
        keys_to_remove = ["copyrights",
                          "images",
                          "label",
                          "popularity",
                          "disc_number",
                          "duration_ms",
                          "explicit",
                          "is_local",
                          "preview_url",
                          "href"]
        remove_keys(track_data, keys_to_remove)
        return track_data

    def get_current_song_uri(self):
        current_track = self.sp.current_playback()
        if current_track is None:
            print("No song is currently playing")
            return None
        else:
            track_uri = current_track["item"]["uri"]
            return track_uri

    def get_current_song_name(self, uri):
        current_track = self.sp.current_playback()
        if current_track is None:
            print("No song is currently playing")
            return None
        else:
            track = self.sp.track(uri)
            song_name = track["name"]
            return song_name

    def get_current_song_artists(self, uri):
        current_track = self.sp.current_playback()
        if current_track is None:
            print("No song is currently playing")
            return None
        else:
            track = self.sp.track(uri)
            song_artists = track["artists"]
            artists = ""
            for artist in song_artists:
                artists += artist["name"] + "; "
            artists = "".join([artists[i] for i in range(len(artists) - 2)])
            return artists

    def get_song_length(self, uri):
        track = self.sp.track(uri)
        length_ms = track['duration_ms']
        length_sec = math.ceil(length_ms / 1000)
        return length_sec

    def get_song_end_time(self):
        end_times = []
        for i in range(3):
            current_track = self.sp.current_playback()
            if current_track is not None and current_track['is_playing']:
                timestamp_ms = current_track['progress_ms']
                duration_ms = current_track['item']['duration_ms']
                start_time = datetime.now() - timedelta(milliseconds=timestamp_ms)
                end_time = start_time + timedelta(milliseconds=duration_ms)
                end_times.append(end_time.strftime('%Y-%m-%d %H:%M:%S'))
            # elif current_track is not None and not current_track['is_playing']:
            #     return 'The song is currently paused.'
            else:
                return None
            time.sleep(0.25)
        return median_date(end_times)

    # def play_spotify_song(self, song_uri):
    #     # need premium
    #     devices = self.sp.devices()
    #     if not devices['devices']:
    #         print("No device found.")
    #         return
    #     device_id = devices['devices'][0]['id']
    #     self.sp.shuffle(state=False, device_id=device_id)
    #     self.sp.repeat(state="off", device_id=device_id)
    #     self.sp.start_playback(device_id=device_id, context_uri=song_uri, uris=[song_uri])

    def play_spotify_song(self, song_uri):
        self.sp.shuffle(state=False)
        self.sp.repeat(state="off")
        self.sp.start_playback(context_uri=song_uri, uris=[song_uri])

    def pause_spotify_song(self):
        current_track = self.sp.current_playback()
        if current_track is not None:
            is_playing = current_track['is_playing']
            if is_playing:
                self.sp.pause_playback()

    def is_playing(self):
        current_track = self.sp.current_playback()
        if current_track is not None:
            is_playing = current_track['is_playing']
            if is_playing:
                return True
            else:
                return False

    def get_song_uri(self, artist_name, track_name):
        results = self.sp.search(q=f'{artist_name} {track_name}', type='track')
        if len(results['tracks']['items']) > 0:
            uri = results['tracks']['items'][0]['uri']
            return uri
        else:
            print(f"No results found for {artist_name} - {track_name}")
            return None

    def check_song_finished(self, track_id, pool_rate_s):
        current_track = self.sp.current_playback()
        while current_track is not None:
            if current_track["item"]["id"] == track_id and current_track["is_playing"]:
                time_remaining = current_track["item"]["duration_ms"] - current_track["progress_ms"]
                if time_remaining <= 0:
                    return True
            time.sleep(pool_rate_s)
            current_track = self.sp.current_playback()
        return False

    def get_playlist_tracks(self, playlist_url):
        STEP = 50
        offset = 0
        tracks = "Empty"
        trackList = []
        while tracks:
            results = self.sp.playlist_tracks(playlist_url, limit=STEP, offset=offset,
                                              fields='items(track(id,name,uri))')
            tracks = results['items']
            trackList += tracks
            offset += STEP
            print(offset)
        return trackList

    def play_tracks(self, tracks):
        for track in tracks:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                                client_secret=self.client_secret,
                                                                redirect_uri=self.redirect_uri,
                                                                scope=self.scope,
                                                                cache_path=".spotifycache",
                                                                show_dialog=True))
            track_id = track['track']['id']
            track_uri = track['track']['uri']
            track_info = self.sp.track(track_id)
            print("track_id " + track_id)
            print("track_uri " + track_uri)
            device_id = self.get_device_id()
            hours, minutes = self.get_playlist_duration()
            print("Time remaining : " + str(hours) + "h" + str(minutes) + "m")
            self.sp.start_playback(device_id=device_id, uris=[track_uri])
            time.sleep(1)
            self.set_volume_to(device_id=device_id, volume_percent=100)
            print('Playing :', track_info['name'])
            time.sleep(3)
            song_end_time = self.get_song_end_time()
            print(track_info['name'] + " ends at " + song_end_time)
            wait_until(song_end_time)
            # while True:
            #     track_status = self.sp.current_playback()
            #     print(track_status)
            #     if not track_status or (track_status['is_playing'] == False):
            #         break
            #     time.sleep(0.25)
            self.remove_track_from_playlist(track_uri)
            print("Pause for 3s...")
            time.sleep(3)


    def is_device_connected(self):
        device_name = os.environ['COMPUTERNAME']
        devices = self.sp.devices()['devices']
        for device in devices:
            if device['name'] == device_name:
                return True
        return False

    def get_device_id(self):
        device_name = os.environ['COMPUTERNAME']
        devices = self.sp.devices()['devices']
        for device in devices:
            if device['name'] == device_name:
                return device['id']
        return None

    def delete_spotify_playlist_by_name(self, playlist_name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                if playlist_id:
                    self.sp.current_user_unfollow_playlist(playlist_id)
                    print(f"Playlist '{playlist_name}' deleted successfully.")
                else:
                    print(f"Playlist '{playlist_name}' not found.")

    def get_playlist_uri(self, playlist_name="All library w/ duplicates"):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_uri = playlist['uri']
                if playlist_uri:
                    return playlist_uri
                else:
                    print(f"Playlist '{playlist_name}' not found.")

    def remove_track_from_playlist(self, track_uri):
        playlist_name = "All library w/ duplicates"
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=[track_uri])

    def set_volume_to(self, device_id, volume_percent):
        self.sp.volume(volume_percent)
        print("Volume set to ", volume_percent)

    def get_playlist_duration_ms(self):
        STEP = 100
        offset = 0
        items = "Empty"
        total_duration_ms = 0
        while items:
            print(offset)
            response = self.sp.playlist_items(self.playlist_id, fields='items(track(name, duration_ms))', limit=STEP,
                                              offset=offset)
            duration_ms = sum([track['track']['duration_ms'] for track in response['items']])
            if duration_ms is not None:
                total_duration_ms += duration_ms
            items = response['items']
            offset += STEP
        return total_duration_ms

    def get_playlist_duration(self):
        total_duration_ms = self.get_playlist_duration_ms()
        total_duration_sec = total_duration_ms / 1000
        total_duration_min = total_duration_sec // 60
        total_duration_hours = total_duration_min // 60
        return int(total_duration_hours), int(total_duration_min % 60)

    def remove_unavailable_tracks_from_list(self, dict_uris):
        final_uris = dict_uris
        unavailable_uris = []
        for uri in final_uris.keys():
            track_id = uri.split(':')[-1]
            track_metadata = self.get_spotify_song_metadata(track_id)
            if len(track_metadata['available_markets']) == 0:
                print("unavailable uri " + uri)
                unavailable_uris.append(uri)
        for uri in unavailable_uris:
            del final_uris[uri]
        return final_uris

    def get_metadata_song(self, song_id):
        song = self.sp.track(song_id)
        artist = parse_artists(song)
        title = song['name']
        album = song['album']['name']
        genres = self.get_genre(artist, title)
        release_date = song['album']['release_date']
        release_year = release_date.split('-')[0]
        return {
            'artist': artist,
            'title': title,
            'album': album,
            'genre': genres,
            'year': release_year
        }

    def get_genre(self, artist, title):
        genres = self.get_song_genre(artist, title)
        if genres is None or not genres:
            genres = self.get_artist_genre(artist)
        return genres

    def get_song_genre(self, artist, title):
        result = self.sp.search(q=', '.join(artist) + ' ' + title, type='artist')
        print("get_song_genre result :", result)
        if result['artists']['items']:
            artist = result['artists']['items'][0]
            genres = artist['genres']
            return genres
        return None

    def get_artist_genre(self, artist):
        result = self.sp.search(q='artist:' + artist[0], type='artist')
        print("get_artist_genre result :", result)
        if result['artists']['items']:
            artist = result['artists']['items'][0]
            genres = artist['genres']
            return genres
        return None

    def get_spotify_artwork(self, track_id):
        track_info = self.sp.track(track_id)
        artwork_url = track_info['album']['images'][0]['url']
        response = requests.get(artwork_url)
        artwork_data = response.content
        return artwork_data
