from requests import get as http_get, post as http_post, HTTPError
from time import sleep
from keyboard import KEY_DOWN, read_event
from dotenv import load_dotenv
from os import getenv

from song import Song


load_dotenv()

API_URL = getenv("API_URL", "http://localhost:8000")
AUTH_TOKEN = getenv("AUTH_TOKEN", "")
API_HEADERS = {
    "content-type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

CIDER_TOKEN = getenv("CIDER_TOKEN", "")
CIDER_PORT = getenv("CIDER_PORT", "10767")
CIDER_URL = f"http://localhost:{CIDER_PORT}/api/v1/playback/now-playing"
CIDER_HEADERS = {
    "content-type": "application/json",
    "apitoken": CIDER_TOKEN,
}


def get_now_playing() -> Song | None:
    try:
        resp = http_get(CIDER_URL, headers=CIDER_HEADERS)
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
        time_left = info.get("remainingTime")
        genres = info.get("genreNames")
        return Song(name, artist, time_left, cover_url, genres)
    except HTTPError as err:
        print(err.response.text)
        return None
    except Exception as e:
        print("Erreur lors de la requête :", e)
        return None


def rate_songs(better_song, worse_song):
    try:
        payload = {
            "better_song": better_song,
            "worse_song": worse_song
        }
        resp = http_post(f"{API_URL}/rate", json=payload, headers=API_HEADERS)
        resp.raise_for_status()
        content = resp.json().get("response")
        return content
    except HTTPError as err:
        print(err.response.text)
        return None
    except Exception as e:
        print("Erreur lors de la requête :", e)
        return None


def get_rates():
    try:
        resp = http_get(f"{API_URL}/rate", headers=API_HEADERS)
        resp.raise_for_status()
        rates = resp.json().get("rates")
        return rates
    except HTTPError as err:
        print(err.response.text)
        return None
    except Exception as e:
        print("Erreur lors de la requête :", e)
        return None


if __name__ == "__main__":
    last_song = ""
    current_song = ""

    while True:
        current = get_now_playing()
        if not current:
            sleep(2)
            continue
        elif current.format_song() == current_song:
            sleep(min(15, abs(current.time_left)))
            continue

        last_song = current_song
        current_song = current.format_song()
        print(current_song)

        if last_song != "":
            is_rated = False
            while not is_rated:
                event = read_event()
                if event.event_type == KEY_DOWN:
                    if event.name == "page up":
                        response = rate_songs(current_song, last_song)
                    elif event.name == "page down":
                        response = rate_songs(last_song, current_song)
                    else:
                        continue
                    print(response)
                    is_rated = True
