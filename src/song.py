class Song:
    def __init__(self, name: str, artist: str, time_left: int, cover_url: str, genres: list[str]):
        self.name = name
        self.artist = artist
        self.time_left = time_left
        self.cover_url = cover_url
        self.genres = genres

    def format_song(self):
        return f"{self.name} - {self.artist}"

    def __str__(self):
        return self.format_song()
