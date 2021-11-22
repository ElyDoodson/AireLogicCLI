from unittest import TestCase, mock
import artist as a
import song as s
from custom_exceptions import BreakLoopError


class TestHasStatistics(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")

    def test_shouldReturnFalse_whenStatisticsIsNone(self):
        actual = self.artist.has_statistics()
        expected = False

        self.assertEqual(actual, expected)

    def test_shouldReturnTrue_whenStatisticsIsNotNone(self):
        self.artist.statistics = 123

        actual = self.artist.has_statistics()
        expected = True

        self.assertEqual(actual, expected)


class TestCalculateMeanWordcount(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")
        song_dict = {
            "has_wordcount": [True, True, True, False],
            "wordcount": [3, 4, 5, 0],
        }
        self.song_list = []
        for i in range(4):
            song = mock.MagicMock()
            song.has_wordcount = list(song_dict.values())[0][i]
            song.wordcount = list(song_dict.values())[1][i]
            self.song_list.append(song)

        self.artist.song_list = self.song_list

    def test_shouldReturnCorrectMean(self):
        actual = self.artist.calculate_mean_wordcount()
        expected = sum(
            [song.wordcount for song in self.artist.song_list if song.has_wordcount]
        ) / sum([1 for song in self.artist.song_list if song.has_wordcount])

        self.assertEqual(actual, expected)

    def test_shouldReturnCorrectMean_whenLessSongsWithWordCount(self):
        self.artist.song_list[2].has_wordcount = False

        actual = self.artist.calculate_mean_wordcount()
        expected = sum(
            [song.wordcount for song in self.artist.song_list if song.has_wordcount]
        ) / sum([1 for song in self.artist.song_list if song.has_wordcount])

        self.assertEqual(actual, expected)

    def test_shouldRetturnNone_whenNoSongsHaveWordCount(self):
        self.artist.song_list[0].has_wordcount = False
        self.artist.song_list[1].has_wordcount = False
        self.artist.song_list[2].has_wordcount = False

        actual = self.artist.calculate_mean_wordcount()
        expected = None

        self.assertEqual(actual, expected)


class TestCalculateMaxWordcount(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")
        self.false_max = 30
        self.true_max = 10
        song_dict = {
            "has_wordcount": [True, True, True, False],
            "wordcount": [3, 4, self.true_max, self.false_max],
        }
        self.song_list = []
        for i in range(4):
            song = mock.MagicMock()
            song.has_wordcount = list(song_dict.values())[0][i]
            song.wordcount = list(song_dict.values())[1][i]
            self.song_list.append(song)

        self.artist.song_list = self.song_list

    def test_shouldReturnMax(self):
        actual = self.artist.calculate_max_wordcount()
        expected = self.true_max

        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, self.false_max)

    def test_shouldReturnZero_whenSongListEmpty(self):
        for song in self.artist.song_list:
            song.has_wordcount = False
        actual = self.artist.calculate_max_wordcount()
        expected = 0

        self.assertEqual(actual, expected)


class TestCalculateMinWordcount(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")
        self.false_min = 5
        self.true_min = 10
        song_dict = {
            "has_wordcount": [True, True, True, False],
            "wordcount": [30, 40, self.true_min, self.false_min],
        }
        self.song_list = []
        for i in range(4):
            song = mock.MagicMock()
            song.has_wordcount = list(song_dict.values())[0][i]
            song.wordcount = list(song_dict.values())[1][i]
            self.song_list.append(song)

        self.artist.song_list = self.song_list

    def test_shouldReturnMin(self):
        actual = self.artist.calculate_min_wordcount()
        expected = self.true_min

        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, self.false_min)

    def test_shouldReturnZero_whenSongListEmpty(self):
        for song in self.artist.song_list:
            song.has_wordcount = False
        actual = self.artist.calculate_min_wordcount()
        expected = 0

        self.assertEqual(actual, expected)


class TestCalculateVarianceWordcount(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")
        song_dict = {
            "has_wordcount": [True, True, True, False],
            "wordcount": [10, 20, 30, 40],
        }
        self.song_list = []
        for i in range(4):
            song = mock.MagicMock()
            song.has_wordcount = list(song_dict.values())[0][i]
            song.wordcount = list(song_dict.values())[1][i]
            self.song_list.append(song)

        self.artist.song_list = self.song_list
        self.artist.wordcount_mean = 20

    def test_shouldReturnVariance(self):
        actual = self.artist.calculate_variance_wordcount()
        expected = 66.6666667

        self.assertAlmostEqual(actual, expected)

    def test_shouldReturnZero_whenMeanIsZero(self):
        for song in self.artist.song_list:
            song.has_wordcount = False
        self.artist.wordcount_mean = 0

        actual = self.artist.calculate_variance_wordcount()
        expected = 0

        self.assertEqual(actual, expected)


class TestCalculateStandardDeviationWordcount(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")
        self.artist.wordcount_variance = 25

    def test_shouldReturnStandardDeviation(self):
        actual = self.artist.calculate_standard_deviation_wordcount()
        expected = self.artist.wordcount_variance ** 0.5

        self.assertEqual(actual, expected)

    def test_shouldReturnZero_whenVarianceIsZero(self):
        self.artist.wordcount_variance = 0

        actual = self.artist.calculate_standard_deviation_wordcount()
        expected = 0

        self.assertEqual(actual, expected)


class TestGetArtistStatistics(TestCase):
    def setUp(self) -> None:
        self.artist = a.Artist("")

    def set_up_mocks(self) -> None:
        self.mean = 25
        self.max = 50
        self.min = 10
        self.variance = 9
        self.standard_dev = 3

        self.artist.calculate_mean_wordcount = mock.MagicMock(return_value=self.mean)
        self.artist.calculate_max_wordcount = mock.Mock(return_value=self.max)
        self.artist.calculate_min_wordcount = mock.Mock(return_value=self.min)
        self.artist.calculate_variance_wordcount = mock.Mock(return_value=self.variance)
        self.artist.calculate_standard_deviation_wordcount = mock.Mock(
            return_value=self.standard_dev
        )

    def test_shouldRaiseBreakLoopError_whenSongListIsEmptyList(self):
        with self.assertRaises(BreakLoopError) as err:
            self.artist.get_artist_statistics()

        actual = err.exception.args[0]
        expected = "Artist has no songs in song list. Unable to calculate statistics"
        self.assertEqual(actual, expected)

    def test_shouldReturnDictionaryWithStatistics(self):
        self.set_up_mocks()
        self.artist.song_list = None
        actual = self.artist.get_artist_statistics()
        expected = {
            "Mean": self.mean,
            "Max": self.max,
            "Min": self.min,
            "Variance": self.variance,
            "Std_dev": self.standard_dev,
        }

        self.assertDictEqual(actual, expected)
