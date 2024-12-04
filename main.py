from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp

# File paths for storing movie data
JOHN_PATH = 'data/data.json'
MARK_PATH = 'data/data.csv'


def main():
    """
    The main entry point of the application.

    Creates instances of `MovieApp` using different storage backends
    (`StorageJson` and `StorageCsv`) and runs the application for each storage.

    Storage backends used:
    - JSON file storage (`StorageJson`) for John.
    - CSV file storage (`StorageCsv`) for Mark.
    """
    # Run the application with JSON storage
    print("Launching Movie App for John (JSON Storage)")
    john_movies = StorageJson(JOHN_PATH)
    john_app = MovieApp(john_movies)
    john_app.run()

    # Run the application with CSV storage
    print("\nLaunching Movie App for Mark (CSV Storage)")
    mark_movies = StorageCsv(MARK_PATH)
    mark_app = MovieApp(mark_movies)
    mark_app.run()


if __name__ == '__main__':
    main()



