from abc import ABC, abstractmethod
import random


class IStorage(ABC):
    """
    Abstract base class for storage operations related to managing a collection of movies.

    This interface defines the essential methods that any concrete storage implementation
    must provide, ensuring a consistent contract for data management.

    Methods:
        _load_data(): Abstract method to load data from the storage medium.
        _save_data(data): Abstract method to save data to the storage medium.
    """


    @abstractmethod
    def _load_data(self):
        """
        Load data from the storage medium.

        Returns:
            dict: A dictionary representing the data retrieved from storage.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        pass


    @abstractmethod
    def _save_data(self, data):
        """
        Save data to the storage medium.

        Args:
            data (dict): The data to be saved.

        Raises:
            NotImplementedError: If not implemented by the subclass.
        """
        pass


    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        """
        data = self._load_data()
        if not data:
            print("No movies found.")
            return {}

        print(f'{len(data)} movies in total:\n')
        for movie, info in data.items():
            print(f'{movie} ({info["year"]}) : {info["rating"]}')


    def add_movie(self, title, year, rating, poster=''):
        """
        Adds a movie to the 'movies database.
        Loads the information from the JSON file, adds the movie,
        and saves it. The function doesn't need to validate the input.
        """
        new_movie = {
            "year": year,
            "rating": rating,
            "poster": poster,
        }

        data = self._load_data()
        if title in data:
            print(f"The movie '{title}' already exists. Updating its details.")
        data[title] = new_movie
        self._save_data(data)
        print("New movie added or updated successfully.")


    def get_data(self):
        """
        Retrieve all data from the storage.

        This method serves as a public interface to load and return the stored data.

        Returns:
            dict: The data retrieved from the storage medium.
        """
        return self._load_data()


    def delete_movie(self, title):
        """
        Deletes a movie from the 'movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data = self._load_data()
        if title in data:
            data.pop(title)
            self._save_data(data)
            print(f"The movie '{title}' was deleted successfully.")
        else:
            print(f"The movie '{title}' was not found in the database.")


    def update_movie(self, title, rating):
        """
        Updates a movie from the 'movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        data = self._load_data()
        if title in data:
            data[title]['rating'] = rating
            self._save_data(data)
            print(f"The movie '{title}' was updated successfully.")
        else:
            print(f"The movie '{title}' was not found in the database.")


    @staticmethod
    def print_best_worst_movie(text, movie_list, movie):
        """
        Print the best or worst movie(s) from a given list based on their ratings.
        """
        print(f"{text} movie: ", end="")
        for mult_best_movie in movie_list:
            if movie[1]['rating'] == mult_best_movie[1]['rating']:
                print(mult_best_movie[0], end=", ")
        print(f"Rating: {movie[1]['rating']}")


    def show_stats(self):
        """
        Display movie statistics, including average and median ratings,
        as well as the highest and lowest-rated movies.
        """
        data = self._load_data()

        # Check if data is empty
        if len(data) == 0:
            print("No data available.")
            return

        # Calculate total rating for average
        total_rating = sum(info["rating"] for info in data.values())
        average = total_rating / len(data)

        # Calculate median rating
        sorted_ratings = sorted(info["rating"] for info in data.values())
        if len(sorted_ratings) % 2 == 0:
            mid1, mid2 = len(sorted_ratings) // 2, len(sorted_ratings) // 2 - 1
            median_rating = (sorted_ratings[mid1] + sorted_ratings[mid2]) / 2
        else:
            median_rating = sorted_ratings[len(sorted_ratings) // 2]

        # Find best and worst movies
        sorted_movies = sorted(data.items(), key=lambda x: x[1]["rating"])
        best_movie = sorted_movies[-1]
        worst_movie = sorted_movies[0]

        # Print results
        print(f"Average rating: {average:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        # Print multiple best/worst films, if they have the same rating
        self.print_best_worst_movie("Best", sorted_movies, best_movie)
        self.print_best_worst_movie("Worst", sorted_movies, worst_movie)


    def random_movie(self):
        """Select and display a random movie from the database."""
        data = self._load_data()
        if not data:
            print("No movies found.")
            return
        random_item = random.choice(list(data.items()))
        print(f"Your movie for tonight: {random_item[0]}, it's rated: {random_item[1]['rating']}")


    def search_movie(self, title):
        """Search for movies by a title keyword, displaying matching results."""
        data = self._load_data()
        if not data:
            print("No movies found.")
            return
        search_part = title.lower()
        for movie, info in data.items():
            if movie.lower().find(search_part) != -1:
                print(f"{movie} ({info['year']}) : {info['rating']}")


    def movies_sorted_by_year(self, user_input):
        """Display movies sorted by their release year in ascending or descending order."""
        data = self._load_data()
        print(user_input)
        # Check if data is empty
        if len(data) == 0:
            print("No data available.")
            return
        if user_input == 'n':
            sorted_movies = sorted(data.items(), key=lambda x: x[1]["year"])
        elif user_input == 'y':
            sorted_movies = sorted(data.items(), key=lambda x: x[1]["year"], reverse=True)
        else:
            return {}
        for movie in sorted_movies:
            print(f"{movie[0]} : {movie[1]['year']}")


    def movies_sorted_by_rating(self):
        """Display movies sorted by rating in descending order."""
        data = self._load_data()
        # Check if data is empty
        if len(data) == 0:
            print("No data available.")
            return
        sorted_movies = sorted(data.items(), key=lambda x: x[1]["rating"], reverse=True)
        for movie in sorted_movies:
            print(f"{movie[0]} : {movie[1]['rating']}")


    def filter_movies(self, min_rating, start_year, end_year):
        """Filter and display movies based on minimum rating and year range."""
        data = self._load_data()
        # Check if data is empty
        if len(data) == 0:
            print("No data available.")
            return
        # Filtered dictionary comprehension
        filtered_movies = {
            title: info for title, info in data.items()
            if info["rating"] >= min_rating and start_year <= info["year"] <= end_year
        }
        if filtered_movies:
            for movie, info in filtered_movies.items():
                print(f"{movie} ({info['year']}) : {info['rating']}")
        else:
            print("No movies found after filtering.")