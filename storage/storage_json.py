import json
from .istorage import IStorage

class StorageJson(IStorage):
    """
    A class for handling JSON-based data storage, implementing the IStorage interface.

    Attributes:
        file_path (str): Path to the JSON file used for data storage.
    """


    def __init__(self, file_path):
        """
        Initialize the storage with the specified file path.

        Args:
            file_path (str): Path to the JSON file.
        """
        self.file_path = file_path


    def _load_data(self):
        """
        Load data from the JSON file.

        Returns:
            dict: The loaded data, or an empty dictionary if the file does not exist
                  or is corrupted.

        Raises:
            Exception: If an unexpected error occurs while loading the file.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.file_path}. Creating a new empty database.")
            return {}
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON. The file might be empty or corrupted.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")
            return {}


    def _save_data(self, data):
        """
        Save data to the JSON file.

        Args:
            data (dict): The data to save.

        Raises:
            Exception: If an error occurs while writing to the file.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
                print(f"Data successfully saved to {self.file_path}.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while saving data: {e}")





