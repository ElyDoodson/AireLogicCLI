from unittest import TestCase, mock
import artist_logic as al
from artist import BreakLoopError
import artist
import song


class TestGetArtistReponse(TestCase):
    @mock.patch("api_caller.get_artist_list_from_name")
    def test_shouldReturnDictionary(self, mock_api_call):
        mock_api_call.return_value = _response = {"artists": [1, 2, 3]}

        actual = al.get_artist_response("")
        expected = _response
        self.assertEqual(actual, expected)

    @mock.patch("api_caller.get_artist_list_from_name")
    def test_shouldRaiseBreakLoopError_whenDictionaryHasNoArtistsKey(
        self, mock_api_call
    ):
        mock_api_call.return_value = _response = {"artists": []}

        with self.assertRaises(BreakLoopError) as err:
            al.get_artist_response("")

        actual = err.exception.args[0]
        expected = "No artists found..."
        self.assertEqual(actual, expected)


class TestGetArtistList(TestCase):
    def setUp(self) -> None:
        self.test_artist_list = ["bob", "fred"]
        self.test_dict_good = {"artists": self.test_artist_list, "other": 123}
        self.test_dict_bad = {"other2": 123}

    def test_shouldReturnArtistList(self):
        actual = al.get_artist_list(self.test_dict_good)
        expected = self.test_artist_list
        self.assertEqual(actual, expected)

    def test_shouldRaiseBreakLoopError_whenDictionaryHasNoArtistKey(self):
        with self.assertRaises(BreakLoopError) as err:
            al.get_artist_list(self.test_dict_bad)

        actual = err.exception.args[0]
        expected = "No Artists found in response"
        self.assertEqual(actual, expected)


class TestGetArtistMbidByIndex(TestCase):
    def setUp(self) -> None:
        self.test_id_list = [{"id": "mbid1"}, {"id": "mbid2"}]
        self.test_response_good = {"artists": self.test_id_list, "other": 123}
        self.test_response_bad = {"other": 123}

    def test_shouldReturnArtistMbid(self):
        index = 0
        actual = al.get_artist_mbid_by_index(self.test_response_good, index)
        expected = self.test_id_list[index]["id"]
        self.assertEqual(actual, expected)

    def test_shouldRaiseBreakLoopError_whenDictionaryHasNoArtistKey(self):
        index_good = 0
        index_bad = 20
        with self.assertRaises(BreakLoopError) as err:
            al.get_artist_mbid_by_index(self.test_response_bad, index_good)

        actual = err.exception.args[0]
        expected = "Id of artist not found"
        self.assertEqual(actual, expected)

    def test_shouldRaiseBreakLoopError_whenIndexChosenNotAvailableInList(self):
        index_good = 0
        index_bad = 20

        with self.assertRaises(BreakLoopError) as err:
            al.get_artist_mbid_by_index(self.test_response_good, index_bad)

        actual = err.exception.args[0]
        expected = "Chosen index not in range of artists available"
        self.assertEqual(actual, expected)


class TestGetPartialArtistSongList(TestCase):
    def return_fake_api_response(self, numer_of_songs):
        return {"works": [{"title": f"{song}"} for song in range(numer_of_songs)]}

    def setUp(self) -> None:
        self._artist = artist.Artist("artist_name")
        self._artist.mbid = "mbid_string"

    @mock.patch(
        "api_caller.get_songs_from_artist_mbid",
    )
    def test_shouldReturnSongList(self, return_function):
        return_function.return_value = self.return_fake_api_response(5)
        actual = [
            song.title for song in al.get_partial_artist_song_list(self._artist, 1)
        ]
        expected = ["0", "1", "2", "3", "4"]
        self.assertEqual(actual, expected)

    @mock.patch("api_caller.get_songs_from_artist_mbid", return_value={"works": []})
    def test_shouldReturnEmptyList_whenWorksKeyEmpty(self, func):
        actual = al.get_partial_artist_song_list(self._artist, 0)
        expected = []

        self.assertEqual(actual, expected)

    @mock.patch("api_caller.get_songs_from_artist_mbid", return_value={})
    def test_shouldRaiseBreakLoopError_whenReponseDictionaryEmpty(self, func):
        with self.assertRaises(BreakLoopError) as err:
            al.get_partial_artist_song_list(self._artist, 0)

        actual = err.exception.args[0]
        expected = "Response has no works attribute"
        self.assertEqual(actual, expected)


class TestAssignLyricsToSongs(TestCase):
    def return_function_bad(self, _artist):
        raise LookupError

    def return_function_good(self, _artist):
        if _artist == "Song1":
            return {"lyrics": "Song 1 lyrics"}
        if _artist == "Song2":
            return {"lyrics": "Song 2 lyrics"}

    def setUp(self) -> None:
        self._artist = artist.Artist("artist_name")
        self._artist.mbid = "mbid_string"
        self._artist.song_list = [song.Song("Song1"), song.Song("Song2")]

    @mock.patch(
        "api_caller.get_lyrics_from_artist_name_and_title",
        side_effect=return_function_good,
    )
    def test_shouldReturnListOfLyrics(self, func):
        al.assign_lyrics_to_songs(self._artist)
        actual = [song.lyrics for song in self._artist.song_list]
        expected = ["Song 1 lyrics", "Song 2 lyrics"]
        self.assertEqual(actual, expected)

    @mock.patch(
        "api_caller.get_lyrics_from_artist_name_and_title",
        side_effect=return_function_bad,
    )
    def test_shouldReturnNumberOfFailedLyricsAssigned_whenLyricsDontGetAssignedToSong(
        self, func
    ):
        actual = al.assign_lyrics_to_songs(self._artist)
        expected = 2
        self.assertEqual(actual, expected)
