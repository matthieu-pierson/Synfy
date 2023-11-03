import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def contains_FR_ors_is_empty(country_list):
    return 'FR' in country_list or len(country_list) == 0


def get_value_from_json(json_data, key):
    if isinstance(json_data, dict):
        if key in json_data:
            return json_data[key]
        else:
            for sub_key, sub_value in json_data.items():
                result = get_value_from_json(sub_value, key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = get_value_from_json(item, key)
            if result is not None:
                return result
    return None


class SpotifyDataAccess:
    def __init__(self, propertiesBuilder):
        self.liked_songs_from_album = []
        self.liked_songs_list = []
        self.client_id = propertiesBuilder.client_id
        self.client_secret = propertiesBuilder.client_secret
        self.playlist_id = None
        self.redirect_uri = propertiesBuilder.redirect_uri
        self.scope = propertiesBuilder.scope
        print(self.scope)
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=self.redirect_uri,
                                                            scope=self.scope))

    def get_liked_albums(self):
        STEP = 50
        offset = 0
        albums = "Empty"
        final_list = []
        while albums:
            print(offset)
            results = self.sp.current_user_saved_albums(limit=STEP, offset=offset)
            albums = results['items']
            for album in albums:
                current_album = album['album']['tracks']['items']
                for song in current_album:
                    final_list.append(song["uri"])
            offset += STEP
        # print("nb songs final_list : " + str(len(final_list)))
        return final_list

    def get_liked_songs(self):
        STEP = 20
        offset = 0
        songs = "Empty"
        final_list = []
        while songs:
            print(offset)
            results = self.sp.current_user_saved_tracks(limit=STEP, offset=offset)
            songs = results['items']
            self.liked_songs_list += songs
            offset += STEP
        print(len(self.liked_songs_list))
        for song in self.liked_songs_list:
            final_list.append(song["track"]["uri"])
        return final_list

    def create_playlist_from_uri_list(self, list_uris, playlist_name):
        user_id = self.sp.current_user()["id"]
        self.delete_spotify_playlist_by_name(playlist_name)
        playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        chunk_size = 100
        list_uris_chunked = [list_uris[i:i + chunk_size] for i in range(0, len(list_uris), chunk_size)]
        self.playlist_id = playlist["id"]
        for chunk_uris in list_uris_chunked:
            self.sp.playlist_add_items(playlist_id=playlist["id"], items=chunk_uris)

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

    def get_playlist_link(self, playlist_name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_uri = playlist['uri']
                if playlist_uri:
                    return "https://open.spotify.com/playlist/" + playlist_uri.replace("spotify:playlist:", "")
                else:
                    print(f"Playlist '{playlist_name}' not found.")

    def get_playlist_name(self, playlist_url):
        playlist_uri = playlist_url.replace("https://open.spotify.com/playlist/", "spotify:playlist:")
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['uri'] == playlist_uri:
                return playlist['name']
        print(f"Playlist '{playlist_url}' not found.")
