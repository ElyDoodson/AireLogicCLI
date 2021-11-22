class Song:
    def __init__(self, title: str):
        self.title = title
        self.has_wordcount = False
        self.lyrics = None

    def assign_lyrics(self, lyrics: str | None) -> None:
        """Assigns lyrics to the obejct, calculates the wordcount,
        and sets has_wordcount = True if lyrics != None

        :param lyrics: The lyrics the to assign to the song
        :type lyrics: None or str
        :None returns:
        """
        if lyrics != None:
            self.lyrics = lyrics
            self.wordcount = self.get_word_count()
            self.has_wordcount = True

    def get_word_count(self) -> int:
        """Calculates the number of words in the lyrics field

        :int returns: number of words in the lyrics attribute
        """
        return len(self.lyrics.split())
