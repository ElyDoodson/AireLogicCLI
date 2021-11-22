from unittest import TestCase, mock
import api_caller

# All tthe tests here are kind of unecessary because theyre all effectively the same function
# but with different API URLs. However, tests are needed nontheless.
class TestGetArtistListFromName(TestCase):
    @mock.patch("api_caller.requests.get")
    def test_output_successful(self, mock_api_call):
        json_response = {"key": "value"}
        mock_api_call.return_value.ok = True
        mock_api_call.return_value.json.return_value = json_response

        actual = api_caller.get_artist_list_from_name("")
        expected = json_response

        self.assertEqual(actual, expected)

    @mock.patch("api_caller.requests.get")
    def test_output_failure(self, mock_api_call):
        status_code = 200
        mock_api_call.return_value.ok = False
        mock_api_call.return_value.status_code = status_code

        with self.assertRaises(LookupError) as err:
            api_caller.get_artist_list_from_name("")

        actual = err.exception.args[0]
        expected = f"Server error with status code {status_code}"
        self.assertEqual(actual, expected)


class TestGetSongsFrromArrtistMbid(TestCase):
    @mock.patch("api_caller.requests.get")
    def test_output_successful(self, mock_api_call):
        json_response = {"key": "value"}
        mock_api_call.return_value.ok = True
        mock_api_call.return_value.json.return_value = json_response

        actual = api_caller.get_songs_from_artist_mbid("", 0)
        expected = json_response

        self.assertEqual(actual, expected)

    @mock.patch("api_caller.requests.get")
    def test_output_failure(self, mock_api_call):
        status_code = 200
        mock_api_call.return_value.ok = False
        mock_api_call.return_value.status_code = status_code

        with self.assertRaises(LookupError) as err:
            api_caller.get_songs_from_artist_mbid("", 0)

        actual = err.exception.args[0]
        expected = f"Server error with status code {status_code}"
        self.assertEqual(actual, expected)


class TestGetLyricsFromArtistNameAndTitle(TestCase):
    @mock.patch("api_caller.requests.get")
    def test_output_successful(self, mock_api_call):
        json_response = {"key": "value"}
        mock_api_call.return_value.ok = True
        mock_api_call.return_value.json.return_value = json_response

        actual = api_caller.get_artist_list_from_name("")
        expected = json_response

        self.assertEqual(actual, expected)

    @mock.patch("api_caller.requests.get")
    def test_output_failure(self, mock_api_call):
        status_code = 200
        mock_api_call.return_value.ok = False
        mock_api_call.return_value.status_code = status_code

        with self.assertRaises(LookupError) as err:
            api_caller.get_lyrics_from_artist_name_and_title("", "")

        actual = err.exception.args[0]
        expected = f"Server error with status code {status_code}"
        self.assertEqual(actual, expected)
