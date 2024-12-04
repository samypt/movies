import omdbapi

class MovieApp:
    """
    A class to manage a movie database with a menu-driven interface.

    Attributes:
        _storage: An object that provides methods to manage movie data storage.
    """

    # Menu options
    MENU = {
        0: "Exit",
        1: "List movies",
        2: "Add movie",
        3: "Delete movie",
        4: "Update movie",
        5: "Stats",
        6: "Random movie",
        7: "Search movie",
        8: "Movies sorted by rating",
        9: "Movies sorted by year",
        10: "Filter movies",
        11: "Generate Website"
    }

    # Constants
    MIN_YEAR = 1800
    MAX_YEAR = 2024
    MIN_RATING = 0
    MAX_RATING = 10


    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage object.

        Args:
            storage: The storage object for movie data.
        """
        self._storage = storage


    def _print_menu(self):
        """Display the menu options to the user."""
        print("\nMenu:")
        for key, value in self.MENU.items():
            print(f"{key}. {value}")
        print('\n')


    def _get_user_choice(self):
        """
        Prompt the user to select a menu option.

        Returns:
            int: The user's selected menu option.
        """
        while True:
            value = input(f"Enter choice (0-{len(self.MENU) - 1}): ")
            if value.isdigit() and 0 <= int(value) <= len(self.MENU) - 1:
                return int(value)
            print("Invalid input. Please enter a valid option.\n")


    def _command_list_movies(self):
        """List all movies in the database."""
        self._storage.list_movies()


    def _command_add_movie(self):
        """Add a new movie to the database."""
        try:
            movie_data = omdbapi.get_movie_info(self.get_user_input_title())
            if movie_data:
                self._storage.add_movie(
                    movie_data['title'],
                    movie_data['year'],
                    movie_data['rating'],
                    movie_data['poster']
                )
                print("Movie added successfully!")
            else:
                print("Movie not found.")
        except Exception as e:
            print(f"Error while adding movie: {e}")


    def _command_delete_movie(self):
        """Delete a movie from the database."""
        title = self.get_user_input_title()
        self._storage.delete_movie(title)


    def _command_update_movie(self):
        """Update a movie's rating in the database."""
        title = self.get_user_input_title()
        rating = self.get_user_input_rating()
        self._storage.update_movie(title, rating)


    def _command_movie_stats(self):
        """Show statistics about the movies in the database."""
        self._storage.show_stats()


    def _command_random_movie(self):
        """Display a random movie from the database."""
        self._storage.random_movie()


    def _command_search_movie(self):
        """Search for a movie by title in the database."""
        title = self.get_user_input_title()
        self._storage.search_movie(title)


    def _command_movies_sorted_by_rating(self):
        """Display movies sorted by rating."""
        self._storage.movies_sorted_by_rating()


    def _command_movies_sorted_by_year(self):
        """Display movies sorted by year."""
        latest_first = self.get_yes_or_no("Do you want the latest movies first? (Y/N): ")
        self._storage.movies_sorted_by_year(latest_first)


    def _command_filter_movies(self):
        """Filter movies by rating and year range."""
        min_rating = self.get_user_input_rating("Enter minimum rating: ")
        start_year = self.get_user_input_year("Enter start year: ")
        end_year = self.get_user_input_year("Enter end year: ")
        self._storage.filter_movies(min_rating, start_year, end_year)


    def _generate_website(self):
        """Generate a website to display the movies."""
        try:
            data = self._storage.get_data()
            template = ''
            for title in data.keys():
                movie_data = omdbapi.get_movie_info(title)
                if movie_data:
                    movie = f"""
                    <li>
                        <div class="movie">
                            <img class="movie-poster" src="{movie_data['poster']}"/>
                            <div class="movie-title">{movie_data['title']}</div>
                            <div class="movie-year">{movie_data['year']}</div>
                        </div>
                    </li>
                    """
                    template += movie
            omdbapi.create_html_template(template)
            print("Website generated successfully!")
        except Exception as e:
            print(f"Error while generating website: {e}")


    def _create_menu_actions(self):
        """
        Create a dictionary mapping menu options to functions.

        Returns:
            dict: A mapping of menu options to functions.
        """
        return {
            1: self._command_list_movies,
            2: self._command_add_movie,
            3: self._command_delete_movie,
            4: self._command_update_movie,
            5: self._command_movie_stats,
            6: self._command_random_movie,
            7: self._command_search_movie,
            8: self._command_movies_sorted_by_rating,
            9: self._command_movies_sorted_by_year,
            10: self._command_filter_movies,
            11: self._generate_website
        }


    @staticmethod
    def _menu_handler(choice, actions):
        """
        Execute the function corresponding to the user's menu choice.

        Args:
            choice (int): The menu option selected by the user.
            actions (dict): A dictionary mapping menu options to functions.
        """
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")


    def run(self):
        """Run the application."""
        menu_actions = self._create_menu_actions()
        print('********** My Movies Database **********\n')
        while True:
            self._print_menu()
            user_choice = self._get_user_choice()
            if user_choice == 0:
                print("Goodbye!")
                break
            self._menu_handler(user_choice, menu_actions)
            input("Press Enter to continue...")


    @staticmethod
    def get_user_input_title():
        """Prompt the user for a movie title."""
        while True:
            value = input("Enter movie title: ").strip()
            if value:
                return value
            print("Invalid input. Please try again.")


    @staticmethod
    def get_user_input_year(prompt="Enter year: "):
        """Prompt the user for a valid movie year."""
        while True:
            value = input(prompt).strip()
            if value.isdigit() and MovieApp.MIN_YEAR <= int(value) <= MovieApp.MAX_YEAR:
                return int(value)
            print(f"Please enter a year between {MovieApp.MIN_YEAR} and {MovieApp.MAX_YEAR}.")


    @staticmethod
    def get_user_input_rating(prompt="Enter rating: "):
        """Prompt the user for a valid movie rating."""
        while True:
            value = input(prompt).strip()
            if (value.replace('.', '', 1).isdigit()
                    and MovieApp.MIN_RATING <= float(value) <= MovieApp.MAX_RATING):
                return float(value)
            print(f"Please enter a rating between {MovieApp.MIN_RATING} and {MovieApp.MAX_RATING}.")


    @staticmethod
    def get_yes_or_no(prompt="Enter Y/N: "):
        """Prompt the user for a yes or no input."""
        while True:
            value = input(prompt).strip().lower()
            if value in ['y', 'n']:
                return value
            print("Invalid input. Please enter 'Y' or 'N'.")
