import api_caller
import artist
import song
from custom_exceptions import BreakLoopError


def get_artist_response(artist_name: str) -> dict:
    """Gets a dict of artists using an api call a

    :str artist_name: Name of artist used to query api
    :dict returns: Dict of artist names or empty dict from LookupError
    """
    try:
        response_dict = api_caller.get_artist_list_from_name(artist_name)
        if response_dict["artists"] != []:
            return response_dict
        else:
            raise BreakLoopError("No artists found...")

    except LookupError:
        raise BreakLoopError("Api GET request failed...")


def get_artist_list(response_dict: dict) -> list:
    """Gets a list of artists from api response dictionary

    :dict response_dict: dict containing artist name
    :list returns: List of artist names or empty list from LookupError
    """
    try:
        list_of_artists = response_dict["artists"]
        return list_of_artists

    except KeyError:
        raise BreakLoopError("No Artists found in response")


def get_artist_mbid_by_index(response_dict: dict, index_of_artist: int) -> str:
    """Gets artists MBID (MusicBrainz unique ID) from reponse dictionary

    :int index_of_artist: The index of the artist chosen by user
    :str returns: MBID string of selected artist
    """
    try:
        return response_dict["artists"][index_of_artist]["id"]

    except KeyError:
        raise BreakLoopError("Id of artist not found")
    except IndexError:
        raise BreakLoopError("Chosen index not in range of artists available")


def assign_artist_song_list(artist_: artist.Artist) -> None:
    """Assigns a list of song names to artist using Artist MBID

    :str artist_mbid: The MBID of artist
    :None returns:
    """
    partial_song_list = None
    offset = 0
    while partial_song_list != []:
        partial_song_list = get_partial_artist_song_list(artist_, offset)
        artist_.song_list.extend(partial_song_list)
        offset = len(artist_.song_list)


def get_partial_artist_song_list(artist_: artist.Artist, offset: int) -> list:
    """Gets the partial list of artist songs (api returns a maximum of 100)
        so offset must by incremented to access all artists songs

    :artist.Artist artist_: Artist object
    :int offset: number of songs to offset the api call by
    :list returns: List of songs
    :raises BreakLoopError: if response has no "works" attribute
    """
    response = api_caller.get_songs_from_artist_mbid(artist_.mbid, offset)

    try:
        if response["works"] != []:
            song_list_from_works = [
                song.Song(work["title"]) for work in response["works"]
            ]
            return song_list_from_works
        else:
            return []
    except KeyError:
        raise BreakLoopError("Response has no works attribute")


def assign_lyrics_to_songs(artist_: artist.Artist) -> None:
    """ "Assigns Lyrics to each song in artist_.song_list

    :artist.Artist artist_: Artist object to assigns lyrics to songs
    :None returns:
    """

    number_of_failed_requests = 0
    total_number_of_songs = len(artist_.song_list)
    max_number_of_loading_sections = 10
    loading_sections = total_number_of_songs // max_number_of_loading_sections

    # I dont like having print functions in here, however I thought
    # it a good idea to have a visual representation of progress for the user
    # max_number_of_loading_sections #'s will always be printed
    print("Loading Lyrics data...")
    print("[", end="")
    for index, song in enumerate(artist_.song_list):
        # Prints every max_number_of_loading_sections songs
        if loading_sections != 0 and index % loading_sections == 0:
            print("#", end="")

        try:
            response = api_caller.get_lyrics_from_artist_name_and_title(
                artist_.name, song.title
            )
        except LookupError:
            number_of_failed_requests += 1
            continue

        song.assign_lyrics(response["lyrics"])
        number_of_failed_requests += 0 if song.has_wordcount else 1
    if loading_sections == 0:
        print("#" * max_number_of_loading_sections, end="")
    print("] = Completed")
    return number_of_failed_requests
