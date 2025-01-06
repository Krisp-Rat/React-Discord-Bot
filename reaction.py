import os
import random
import csv
import json
import discord

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
            return "11 The file is empty.mp4"
        filename = random.choice(lines).strip()
    return filename

def store_message(server, channel, name, content, attachments):
    """Appends a new line to the specified CSV file."""
    filename = "storage/text_history.csv"
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
        return list(data.values())
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: File not found or invalid JSON in {filename}")
        return []


def edit_banned_list(filename, channel_name, channel_id, add=True):
    # Retrieve the data from the banned list
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    problem = False
    if add:
        data[channel_name] = channel_id
        print(f"Added: {channel_name} to the banned list")
    else:
        if channel_name in data:
            del data[channel_name]
            print(f"Removed: {channel_name} from the banned list")
        else:
            print(f"{channel_name}: not found in the banned list.")
            problem = True

    # Save the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    return problem

async def channelInfo(interaction, bot, channel: discord.TextChannel = None, channel_ids: str = None):
    if channel:
        # If a channel is provided, grab the ID and add to the list
        channel_name = channel.name
        channel_id = channel.id
    elif channel_ids:
        channel_name = await bot.fetch_channel(int(channel_ids))
        channel_name = channel_name.name
        channel_id = int(channel_ids)
    else:
        # If no channel is provided, inform the user
        channel_name = interaction.channel.name
        channel_id = interaction.channel.id
    return channel_name, channel_id

