from urllib import parse
from os import getenv
from requests import get as http_get, post as http_post, HTTPError

from src.song_status_dto import SongStatusDto


class ApiClient:
    def __init__(self):
        self.API_URL = getenv("API_URL", "http://localhost:8000")
        self.AUTH_TOKEN = getenv("AUTH_TOKEN", "")
        self.API_HEADERS = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.AUTH_TOKEN}",
        }

    def rate_songs(self, better_song, worse_song) -> None:
        payload = {
            "better_song": better_song,
            "worse_song": worse_song
        }
        for i in range(3):
            try:
                resp = http_post(f"{self.API_URL}/rate", json=payload, headers=self.API_HEADERS)
                resp.raise_for_status()
                content = resp.json().get("response")
                print(content)
                return
            except HTTPError as err:
                print(f"Attempt {i}: {err.response.text}")
            except Exception as e:
                print(f"Attempt {i}: {e}")

    def get_rates(self):
        try:
            resp = http_get(f"{self.API_URL}/rate", headers=self.API_HEADERS)
            resp.raise_for_status()
            rates = resp.json().get("rates")
            return rates
        except HTTPError as err:
            print(err.response.text)
            return None
        except Exception as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def get_status_between_songs(self) -> SongStatusDto | None:
        try:
            resp = http_get(f"{self.API_URL}/status", headers=self.API_HEADERS)
            resp.raise_for_status()
            data = resp.json()
            song_status = SongStatusDto(message=data.get("message"), is_compared=data.get("is_compared"))
            return song_status
        except HTTPError as err:
            print(err.response.text)
            return None
        except Exception as e:
            print(f"Erreur lors de la requête : {e}")
            return None

    def get_next_song(self, current_song: str) -> str | None:
        try:
            resp = http_get(parse.quote(f"{self.API_URL}/next_song/{current_song}"), headers=self.API_HEADERS)
            resp.raise_for_status()
            if resp.text == "":
                return None
            return resp.text
        except HTTPError as err:
            print(err.response.text)
            return None
        except Exception as e:
            print("Erreur lors de la requête :", e)
            return None
