from .istorage import IStorage
import csv


class StorageCsv(IStorage):
    """
    A class for handling CSV-based data storage, implementing the IStorage interface.

    Attributes:
        file_path (str): Path to the CSV file used for data storage.
    """


    def __init__(self, file_path):
        """
        Initialize the storage with the specified file path.

        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path


    def _save_data(self, data):
        """Save data to the CSV file with proper formatting and exception handling.

        Args:
            data (dict): A dictionary containing movie information, where the keys are titles and values are dictionaries with 'rating' and 'year'.
        """
        # Prepare the data list with header
        data_list = [['title', 'rating', 'year']]  # Header for CSV file

        # Populate data_list with the movie data from the provided dictionary
        for title, details in data.items():
            rating = details.get('rating', 'N/A')  # Default to 'N/A' if rating is missing
            year = details.get('year', 'N/A')  # Default to 'N/A' if year is missing
            data_list.append([title, rating, year])  # Add each movie's details as a row

        try:
            # Open the file for writing and save the data
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data_list)  # Write all rows (header + data)

            print("Changes saved successfully.")

        except IOError as e:
            # Catch file I/O errors (e.g., permission errors, file not found)
            print(f"An error occurred while saving the data: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")



    def _load_data(self):
        """Load data from the CSV file or create an empty dictionary if file not found.

        Returns:
            dict: A dictionary where keys are movie titles and values are dictionaries
            containing 'rating' and 'year'.
        """
        new_dic = {}  # Initialize the dictionary to hold the movie data

        try:
            # Open the CSV file for reading
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                titles = next(reader)  # Read the header row

                # Initialize indices for 'title', 'rating', and 'year'
                title_index = rating_index = year_index = None

                # Determine the indices for 'title', 'rating', and 'year'
                for index, value in enumerate(titles):
                    if 'title' in value.lower():
                        title_index = index
                    elif 'rating' in value.lower():
                        rating_index = index
                    elif 'year' in value.lower():
                        year_index = index

                # Ensure all required indices are found
                if None in [title_index, rating_index, year_index]:
                    missing_columns = []
                    if title_index is None: missing_columns.append('title')
                    if rating_index is None: missing_columns.append('rating')
                    if year_index is None: missing_columns.append('year')
                    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}.")

                # Read the rows and populate the dictionary
                for row in reader:
                    try:
                        # Safely access each row's values using the identified indices
                        title = row[title_index]
                        rating = float(row[rating_index]) if row[rating_index] else None  # Convert to float
                        year = int(row[year_index]) if row[year_index] else None  # Convert to int

                        # Add the movie data to the dictionary
                        new_dic[title] = {"rating": rating, "year": year}

                    except ValueError:
                        print(f"Skipping row with invalid data: {row}")

                return new_dic

        except FileNotFoundError:
            print(f"The file {self.file_path} was not found. Creating a new one.")
            return {}
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            return {}


