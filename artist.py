from custom_exceptions import BreakLoopError


class Artist:
    def __init__(self, name: str):
        self.name = name
        self.song_list = []
        self.statistics = None

    def has_statistics(self) -> bool:
        """Does the artist already have a not None statistics field?

        :bool returns: True if artist.statistics != None
        """
        return True if self.statistics != None else False

    def calculate_mean_wordcount(self) -> int:
        """Calculates the mean number of words in the artists song list

        :int returns: mean number of words in song list
        """
        number_of_songs = 0
        total_words_in_songs = 0

        for song in self.song_list:
            if song.has_wordcount:
                number_of_songs += 1
                total_words_in_songs += song.wordcount
        average_wordcount = (
            total_words_in_songs / number_of_songs if number_of_songs > 0 else None
        )
        self.wordcount_mean = average_wordcount

        return average_wordcount

    def calculate_max_wordcount(self) -> int:
        """Calculates the highest number of words in the artists song list

        :int returns: highest number of words in song list
        """
        song_list_has_non_zero_wordcount = any(
            song.has_wordcount == True for song in self.song_list
        )
        return (
            max([song.wordcount for song in self.song_list if song.has_wordcount])
            if song_list_has_non_zero_wordcount
            else 0
        )

    def calculate_min_wordcount(self) -> int:
        """Calculates the lowest number of words in the artists song list

        :int returns: lowest number of words in song list
        """
        song_list_has_non_zero_wordcount = any(
            song.has_wordcount == True for song in self.song_list
        )
        return (
            min([song.wordcount for song in self.song_list if song.has_wordcount])
            if song_list_has_non_zero_wordcount
            else 0
        )

    def calculate_variance_wordcount(self) -> int:
        """Calculates the variance of number of words in the artists song list

        :int returns: variance of number of words in song list
        """
        if self.wordcount_mean == 0:
            return 0

        total_mean_differnce_squared = 0
        for song in self.song_list:
            if song.has_wordcount:
                total_mean_differnce_squared += (
                    song.wordcount - self.wordcount_mean
                ) ** 2

        variance = total_mean_differnce_squared / len(
            [song for song in self.song_list if song.has_wordcount]
        )
        self.wordcount_variance = variance
        return variance

    def calculate_standard_deviation_wordcount(self) -> int:
        """Calculates the standard deviation
        of number of words in the artists song list

        :int returns: standard deviation of number of words in song list
        """
        if self.wordcount_variance == 0:
            return 0
        standard_deviation = self.wordcount_variance ** 0.5
        self.wordcount_standard_deviation = standard_deviation
        return standard_deviation

    def get_artist_statistics(self) -> dict:
        """Returns a dictionary of the mean, max, min, variance,
        and standard deviation on the number of words in the artist's song list

        :dict returns: Dictionary of statistics
        """
        if self.song_list == []:
            raise BreakLoopError(
                "Artist has no songs in song list. Unable to calculate statistics"
            )
        wordcount_mean = self.calculate_mean_wordcount()
        wordcount_max = self.calculate_max_wordcount()
        wordcount_min = self.calculate_min_wordcount()
        wordcount_variance = self.calculate_variance_wordcount()
        wordcount_standard_deviation = self.calculate_standard_deviation_wordcount()

        statistics_dict = {
            "Mean": wordcount_mean,
            "Max": wordcount_max,
            "Min": wordcount_min,
            "Variance": wordcount_variance,
            "Std_dev": wordcount_standard_deviation,
        }
        self.statistics = statistics_dict
        return statistics_dict
