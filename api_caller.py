import requests


def _check_response(response: requests.Response) -> dict:
    """Checks the response from the API.

    :requests.Response response: response object from the api call
    :dict returns: dictionary if api status_code < 400
    :raises LookupError: if api status_code >= 400
    """

    if response.ok:
        return response.json()
    else:
        raise LookupError(
            "Server error with status code {}".format(response.status_code)
        )


def get_artist_list_from_name(name: str) -> dict:
    """Queries MusicBrainz.org api using a given name to get a list of artists

    :str name: name of artist
    :dict returns: response from api as dictionary
    :raises LookupError: if api status_code >= 400
    """
    url = 'https://musicbrainz.org/ws/2/artist/?query="{}"&fmt=json'.format(name)
    response = requests.get(url)
    return _check_response(response)


def get_songs_from_artist_mbid(artist_mbid: str, api_song_offset: int) -> dict:
    """Queries MusicBrainz.org api using a given artist mbid to get a list of 'works'

    :str artist_mbid: mbid (uniqiue MusicBrainz ID) of artist
    :int api_song_offset: 100 maximum results returnable. Offset used to access more api results.
    :dict returns: response from api as dictionary
    :raises LookupError: if api status_code >= 400
    """
    url = "https://musicbrainz.org/ws/2/work?artist={}&limit=100&fmt=json&offset={}".format(
        artist_mbid, api_song_offset
    )
    response = requests.get(url)
    return _check_response(response)


def get_lyrics_from_artist_name_and_title(artist_name: str, song_title: str) -> dict:
    """Queries lyricsovh api using a given artist name and song title
        to get a lysics of chosen song

    :str artist_name: Name of artist
    :str song_title: Name of song
    :dict returns: dictionary containing lyrics of requested song
    :raises LookupError: if api status_code >= 400
    """
    url = "https://api.lyrics.ovh/v1/{}/{}".format(
        artist_name, song_title.replace(" ", "%20")
    )
    response = requests.get(url)
    return _check_response(response)
