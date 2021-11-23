import sys
import artist
import artist_logic as al
from time import sleep
from custom_exceptions import BreakLoopError


def display_initial_message() -> None:
    """Displays initial message to user

    :None returns:
    """
    print(
        """
        #################################################################################
        Welcome to my CLI Python app for Airelogic Assessment.

        This CLI should be able to get the average number of words in an artists songs.
        It will also allow you to see other statistics of their songs and compare these 
        statistics with another artist.

        To start, please enter the name of an artist or band you wish to investigate.   
        #################################################################################
        """
    )


def display_artist_search_results(
    list_of_artists: list, number_of_results: int
) -> None:
    """Displays a formatted truncated list of artists

    :list list_of_artists: List of Artist names
    :int number_of_results: Number of results to be shown
    :None returns:
    """
    trunc_list_of_artists = list_of_artists[:number_of_results]
    number_of_artists = len(trunc_list_of_artists)

    if number_of_artists > 0:
        print(f"Showing {number_of_artists} Artists matching your search result.\n")

        for index, artist in enumerate(trunc_list_of_artists):
            print(
                "Id: {:>2} | Name: {:^20} | Type: {:>9} | Country: {}".format(
                    index + 1,
                    artist["name"],
                    artist["type"] if "type" in artist else "N/A",
                    artist["area"]["name"] if "area" in artist else "N/A",
                )
            )


def get_input_from_user(user_message: str, number_of_results: int) -> int:
    """Gets input from user between 1 -> number_of_results

    :str user_message: Message to display to the user
    :int number_of_results: Number of results the user has to choose from
    :int returns: index of list chosen
    :raises ValueError: When input != int
    """
    while True:
        try:
            chosen_artist_index = int(input(user_message))
        except ValueError:
            print("Please choose an integer.")
            continue

        if chosen_artist_index < 1 or chosen_artist_index > number_of_results:
            print(f"Please choose a number between 1 and {number_of_results}.")
        else:
            break
    return chosen_artist_index


class Main:
    # Private Fields
    _list_of_artists = []
    _number_of_results = 10
    _max_artists = 5

    # Dunder Methods
    def __init__(self) -> None:
        self.choices = {
            "1": self.display_artists,
            "2": self.create_artist,
            "3": self.delete_artist,
            "4": self.display_artist_statistics,
            "5": self.compare_artists,
            "6": self.quit,
        }

    # Regular Methods
    def is_artist_available(self) -> None:
        """Returns whether there are available artists

        :None returns:
        """
        return True if len(self._list_of_artists) > 0 else False

    def create_artist(self) -> None:
        """Creates an artist using functions from artist_logic module
        and input from user

        :None returns:
        """
        if len(self._list_of_artists) < self._max_artists:
            # Object instantiation
            artist_name = input("Artist name: ")
            artist_ = artist.Artist(artist_name)

            # Display of queried artists
            response = al.get_artist_response(artist_name)
            artist_list = al.get_artist_list(response)
            display_artist_search_results(artist_list, self._number_of_results)

            # Selection and assignment of artist MBID
            user_message = "Please Choose the Id of the Artist you wish to select: "
            chosen_index = get_input_from_user(user_message, self._number_of_results)
            artist_mbid = al.get_artist_mbid_by_index(response, chosen_index - 1)
            artist_display_name = al.get_artist_display_name_by_index(
                response, chosen_index - 1
            )
            artist_.name = artist_display_name
            artist_.mbid = artist_mbid
            self._list_of_artists.append(artist_)
            print("Artist Added Successfully")

        else:
            print("Maximum Artists Reached, please delete one before proceeding\n")

    def display_artists(self) -> None:
        """Displays the list of current artists if available

        :None returns:
        """
        if self.is_artist_available():
            print(
                """
             Artist Table
            --------------"""
            )
            for index, artist in enumerate(self._list_of_artists):
                print(
                    f"Id: {index+1} | Name: {artist.name} | Has Statistics?: {artist.has_statistics()}"
                )
        else:
            print("Artist list empty, please add an Artist to view")

    def delete_artist(self):
        """Deletes an artist chosen by user

        :None returns:
        """
        if self.is_artist_available():
            # User input
            self.display_artists()
            user_message = "Please Choose an Artist to delete: "
            user_input = get_input_from_user(user_message, len(self._list_of_artists))

            # Deleting selected Artist
            artist_name = self._list_of_artists[user_input - 1].name
            del self._list_of_artists[user_input - 1]
            print(f"{artist_name} was successfully deleted.")
        else:
            print("There are no artists, please add an artist in order to use delete")

    def get_artist_statistics_dict(self, artist_: artist.Artist) -> dict:
        """Gets a dictionary containing artist statistics mean, max, min,
        variance, standard deviation of the number of words in the songs
        of the given artist

        :artist.Artist artist_:
        :dict return: Dictionary containing statistics
        """
        if artist_.has_statistics():
            return artist_.statistics
        else:
            # I wasnt sure what was better, getting the values then assigning,
            # or passing artist into a class and assigning it inline"
            # I went with this because it looks cleaner and easier to read
            # Also since i dont use song_list or lyrics, there is not reason to
            # store then as variables here
            al.assign_artist_song_list(artist_)
            failed_lyric_requests = al.assign_lyrics_to_songs(artist_)
            total_songs_with_lyrics = sum(
                [1 if song.has_wordcount else 0 for song in artist_.song_list]
            )
            print(
                f"{failed_lyric_requests} lyric request(s) failed out of {total_songs_with_lyrics} songs"
            )
            statistics = artist_.get_artist_statistics()

            return statistics

    def display_artist_statistics(self, artist_: artist.Artist = None) -> None:
        """Displays the statistics of the artist given

        :param artist_: If not None, displays the given artists statistics,
                        else it asks user which artist they would like
                        the statistsics for
        :type artist_: None or artist.Artist
        :None returns:
        """
        if self.is_artist_available():
            if artist_ == None:
                self.display_artists()
                user_message = "Please Choose an Artist to show statistics for: "
                user_input = get_input_from_user(
                    user_message, len(self._list_of_artists)
                )
                artist_ = self._list_of_artists[user_input - 1]

            statistics_dict = self.get_artist_statistics_dict(artist_)
            print(f"Statistics for {artist_.name}")

            statsistics_string = "|".join(
                f" {key}: {value} " for key, value in statistics_dict.items()
            )
            print(statsistics_string)
        else:
            print("No Artist available to calculate statistics, please add an Artist")

    def compare_artists(self) -> None:
        """Compares the stats of two artists

        :None returns:
        """
        if len(self._list_of_artists) > 1:
            artists_to_compare = []
            self.display_artists()
            for choice_as_string in ["First", "Second"]:
                user_message = (
                    f"Please Choose the {choice_as_string} Artist to compare: "
                )
                user_input = get_input_from_user(
                    user_message, len(self._list_of_artists)
                )

                artists_to_compare.append(self._list_of_artists[user_input - 1])
            for artist_ in artists_to_compare:
                self.display_artist_statistics(artist_)
        else:
            print("At least 2 Artists are required to compare, please add more artists")

    def display_menu(self) -> None:
        """Displays the available choices to the user

        :None returns:
        """

        print(
            """
        -----------------------------------------
            Menu
        -----------------------------------------
        1. Show Current Artist List
        2. Create New Artist
        3. Delete Artist
        4. Display Artist Statistics
        5. Compare Artists
        6. Quit
        """
        )

    def run(self) -> None:
        """This is the Application Loop and will run until quitted by the user

        :None returns:
        """
        display_initial_message()

        while True:
            try:
                sleep(0.5)
                self.display_menu()
                choice = input("Enter an option: ")
                action = self.choices.get(choice)
                if action:
                    action()
                else:
                    print(f"{choice} is not a valid choice")

            except BreakLoopError as err:
                print(
                    "\nMoving back to Main Menu. An error occured with the following message:"
                )
                print(err)

    def quit(self) -> None:
        """Quits the program

        :None returns:
        """

        print("Thank you for using my cli app")
        sys.exit(0)


if __name__ == "__main__":
    Main().run()
