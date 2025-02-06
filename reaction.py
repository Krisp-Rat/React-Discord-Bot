import os
import random
import csv
import json
import discord
from datetime import datetime
# from openai import OpenAI
# import dotenv
# dotenv.load_dotenv()
# client = OpenAI()


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
    with open("Reactions/react_phrases.txt", "r") as file:
        lines = file.readlines()
        if not lines:
            return "The file is empty"
        react_phrase = random.choice(lines).strip()

        # If this phrase is chosen then return the current time
        if react_phrase == "Tell the current time":
            if random.randint(0, 1) < .5:
                time = datetime.now().strftime("%H:%M %p")
                react_phrase = f"The current time is {time}"
    return react_phrase


def store_message(server, channel, name, content, attachments):
    """Appends a new line to the specified CSV file."""
    filename = "Storage/text_history.csv"
    # Open the CSV file in append mode
    url_list = [img.url for img in attachments]
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Append the new row
        writer.writerow([server, channel, name, content] + url_list)


def banned_list_file(filename):
    try:
        # Load data from the JSON file
        with open(filename, 'r') as file:
            data = json.load(file)

        # Return all the values from the JSON data as a list
        return list(data.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: File not found or invalid JSON in {filename}")
        return []






