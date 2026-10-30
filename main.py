from time import sleep
from keyboard import KEY_DOWN, read_event
from dotenv import load_dotenv

from src.api_client import ApiClient
from src.cider_client import CiderClient


if __name__ == "__main__":
    load_dotenv()
    api_client = ApiClient()
    cider_client = CiderClient()
    last_song = ""
    current_song = ""

    while True:
        current = cider_client.get_now_playing()
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
                        api_client.rate_songs(current_song, last_song)
                    elif event.name == "page down":
                        api_client.rate_songs(last_song, current_song)
                    else:
                        continue
                    is_rated = True
