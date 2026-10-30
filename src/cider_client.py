from os import getenv
from requests import get as http_get, post as http_post, HTTPError
from urllib.parse import quote

from src.song import Song


class CiderClient:
    def __init__(self):
        self.CIDER_TOKEN = getenv("CIDER_TOKEN", "")
        self.CIDER_PORT = getenv("CIDER_PORT", "10767")
        self.CIDER_BASE_URL = f"http://localhost:{self.CIDER_PORT}/api/v1"
        self.CIDER_HEADERS = {
            "content-type": "application/json",
            "apitoken": self.CIDER_TOKEN,
        }

    def get_now_playing(self) -> Song | None:
        try:
            resp = http_get(f"{self.CIDER_BASE_URL}/playback/now-playing", headers=self.CIDER_HEADERS)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != "ok":
                print("Réponse inattendue :", data)
                return None
            info = data.get("info")
            name = info.get("name")
            if name is None:
                return None
            artwork = info.get("artwork")
            cover_url = artwork.get("url")
            artist = info.get("artistName")
            time_left = info.get("remainingTime", 10000)
            genres = info.get("genreNames")
            return Song(name, artist, time_left, cover_url, genres)
        except HTTPError as err:
            print(err.response.text)
            return None
        except Exception as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def queue_next(self, song_id: str) -> bool:
        payload = {
            "type": "songs",
            "id": song_id,
        }
        try:
            resp = http_post(f"{self.CIDER_BASE_URL}/playback/play-next", json=payload, headers=self.CIDER_HEADERS)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"Erreur file d'attente : {e}")
            return False

    def search_song_id(self, query: str, storefront: str = "fr") -> str | None:
        path = f"/v1/catalog/{storefront}/search?term={quote(query.replace(" - ", " "))}&types=songs&limit=5"
        payload = {
            "path": path
        }
        try:
            resp = http_post(f"{self.CIDER_BASE_URL}/amapi/run-v3", json=payload, headers=self.CIDER_HEADERS)
            resp.raise_for_status()
            data = resp.json()
            songs = data["data"]["results"]["songs"]["data"]
            if not songs:
                return None
            return songs[0]["id"]
        except Exception as e:
            print(f"Erreur recherche : {e}")
            return None
