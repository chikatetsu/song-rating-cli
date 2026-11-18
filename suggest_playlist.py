from dotenv import load_dotenv

from src.api_client import ApiClient


if __name__ == "__main__":
    load_dotenv()
    api_client = ApiClient()

    songs = set()
    last_song = None
    current_song = input("Please enter the song you want to listen right now (song - artist): ")
    next_song = api_client.get_next_song(current_song, last_song)
    last_song = current_song
    while next_song is not None and next_song not in songs:
        songs.add(last_song)
        print(next_song)
        new_next_song = api_client.get_next_song(next_song, last_song)
        for i in range(5):
            if new_next_song in songs:
                new_next_song = api_client.get_next_song(next_song, new_next_song)
        last_song = next_song
        next_song = new_next_song
