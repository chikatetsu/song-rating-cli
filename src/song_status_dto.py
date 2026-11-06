class SongStatusDto:
    def __init__(self, message: str, is_compared: bool):
        self.message = message
        self.is_compared = is_compared
