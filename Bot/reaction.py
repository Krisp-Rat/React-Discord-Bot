import os
import random
import csv
import json
from dotenv import load_dotenv
from datetime import datetime
from generated_reply import generate_reaction

# Percentage of reactions that use AI
load_dotenv(dotenv_path='../Storage/.env')
AI_RATE = float(os.environ.get("AI_RATE"))


def grab_reaction():
    """Choose a random file from the given folder."""
    try:
        # List all files in the folder
        folder_path = "../Storage/Reactions/GrabBag"
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

def react_text(text="", img=None):
    with open("../Storage/Reactions/react_phrases.txt", "r") as file:
        lines = file.readlines()
        if not lines:
            return "The file is empty"
        react_phrase = random.choice(lines).strip()

        # If this phrase is chosen then return the current time
        if react_phrase == "Tell the current time":
            time = datetime.now().strftime("%I:%M %p").lstrip('0')
            react_phrase = f"The current time is {time}"

        # Feed response to GPT model
        if random.random() < AI_RATE:
            react_phrase = generate_reaction(react_phrase, text, img)

    return react_phrase


def store_message(server, channel, name, content, attachments):
    """Appends a new line to the specified CSV file."""
    filename = "../Storage/text_history.csv"
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

