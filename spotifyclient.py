import random
import requests

from oauth2 import get_oauth2_token

FILE_NAME = "session.token"

class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, client_id: str, client_secret: str, user_id: str) -> None:
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        try:
            f = open(FILE_NAME)
            self._authorization_token = f.read()
            f.close()
        except FileNotFoundError:
            self._authorization_token = None

        while self._place_get_api_request('https://api.spotify.com/v1/me').status_code != 200:
            self._authorization_token = get_oauth2_token(client_id, client_secret)
        f = open(FILE_NAME, "w")
        f.write(self._authorization_token)
        f.close()

        self._user_id = user_id

    def random_fill_playlist(self, dst: str, src: str) -> None:
        # GET SOURCE PLAYLIST
        pl = self.get_songs_from_playlist(src)
        # SHUFFLE SOURCE
        random.shuffle(pl)
        # INSERT IN DST
        songs = self._get_songs_uris(pl, 100)
        print(f"Inserendo tracce...")
        pos = 0
        for song in songs:
            self._place_post_api_request(f"https://api.spotify.com/v1/playlists/{dst}/tracks",
                                         {
                                            "uris": [uri["uri"] for uri in song],
                                            "position": 100*pos
                                         }
                                        )
            pos += 1
        return

    def get_songs_from_playlist(self, playlist: str) -> list[str]:
        url = f"https://api.spotify.com/v1/playlists/{playlist}/tracks?limit=50"
        response = self._place_get_api_request(url).json()
        uris = []
        go = True
        print("Ottenendo le canzoni dalla playlist...")
        while go:
            try:
                for item in response["items"]:
                    uris.append(item["track"]["uri"])
                response = self._place_get_api_request(response["next"]).json()
            except requests.exceptions.MissingSchema:
                go = False
        
        return uris

    def empty_playlist(self, playlist: str) -> None:
        snap_id = self._place_get_api_request(f"https://api.spotify.com/v1/playlists/{playlist}").json()["snapshot_id"]
        songs = self._get_songs_uris(self.get_songs_from_playlist(playlist), 100)
        print(f"Eliminando tracce...")
        for uris in songs:
            self._place_delete_api_request(f"https://api.spotify.com/v1/playlists/{playlist}/tracks", None,
                                           {
                                               "tracks": uris,
                                               "snapshot_id": snap_id
                                           }
                                          ).json()
            snap_id = self._place_get_api_request(f"https://api.spotify.com/v1/playlists/{playlist}").json()["snapshot_id"]
        return

    def _get_auth_token(self, client_id: str, client_secret: str) -> str:
        return requests.post(f"https://accounts.spotify.com/api/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}",
                             headers={"Content-Type": "application/x-www-form-urlencoded"}
                            ).json()["access_token"]

    def _get_songs_uris(self, songs: list[str], cap: int) -> list[list[str]]:
        uris = []

        for i, song in enumerate(songs):
            if (i % cap) == 0:
                _ = []
                uris.append(_)
            _.append(dict(uri=song))

        if uris and uris[0] == []:
            uris.pop(0)

        return uris

    def _place_get_api_request(self, url: str) -> object:
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url: str, data: dict()) -> object:
        response = requests.post(
            url,
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response
    
    def _place_delete_api_request(self, url: str, data: dict(), json: dict()) -> object:
        response = requests.delete(
            url,
            data=data,
            json=json,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response