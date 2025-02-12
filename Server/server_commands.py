import os
import bcrypt
import dotenv
import requests
import json

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')


#-----------------------------------------------------------------------------
# Authenticate functions

def authenticate(token):
    # Set default values for a guest
    usr = "Guest"
    token = token.encode()
    auth_token = os.environ.get("ADMIN_PASS", "").encode()
    auth = bcrypt.checkpw(token, auth_token)
    return auth, usr

def convert(token):
    try:
        return int(token).to_bytes(6, byteorder="big").decode("utf-8")
    except ValueError:
        return "None"


#-----------------------------------------------------------------------------
# Ban/Unban functions

def grabChannelName(channel_id):
    # Construct the URL for the API endpoint
    url = f'https://discord.com/api/v10/channels/{channel_id}'

    # Set the headers to include the bot token for authorization
    headers = {'Authorization': f'Bot {BOT_TOKEN}'}

    # Send a GET request to fetch channel details
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        channel_data = response.json()

        # Print the channel name
        return True, channel_data['name']
    else:
        return False, "Error"

def sendResponse(channel_id, message_content):
    # URL to send the message
    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    # Headers to authenticate the request
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    # Payload for the message
    payload = {'content': message_content}
    requests.post(url, headers=headers, json=payload)


def edit_banned_list(channel_name, channel_id, ban=True):
    # Retrieve the data from the banned list
    filename = f"../Storage/banned_channels.json"
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if ban:
        data[channel_id] = channel_name
        message = f"Added: {channel_name} to the banned list"
        sendResponse(channel_id, "I have been banned from this channel :(")
    else:
        if channel_id in data:
            del data[channel_id]
            message = f"Removed: {channel_name} from the banned list"
            sendResponse(channel_id, "We are **SO** back!!!")
        else:
            message = f"{channel_name}: not found in the banned list."

    # Save the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    return message

#-----------------------------------------------------------------------------
# Add phrase to Reactions/react_phrases.txt

def add_phrase(phrase):
    with open("../Reactions/react_phrases.txt", mode='a', encoding='utf-8') as file:
        # Append the new row
        file.write(f"\n{phrase}")

#-----------------------------------------------------------------------------
