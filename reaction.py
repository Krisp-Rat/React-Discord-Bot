import os
import random

def grab_reaction():
    """Choose a random file from the given folder."""
    try:
        # List all files in the folder
        folder_path = "Reactions/GrabBag"
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        if not files:
            return "The folder is empty or contains no files."

        # Select a random file
        random_file = random.choice(files)
        return random_file
    except FileNotFoundError:
        return "The specified folder does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def react_text():
    file = grab_reaction()
    index = file.find(" ")
    file = file[index + 1: -4]
    return file.capitalize()
