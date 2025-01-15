import os
import csv
import bcrypt
import uuid

class Message_Command:
    def __init__(self, env, usr, auth, msg, rct):
        self.env = env
        self.usr = usr
        self.auth = auth
        self.msg = msg
        self.rct = rct

    def returnElement(self):
        pass

    def print(self):
        print("\n--------------------")
        print(f"{self.usr} reacted in a {self.env}")
        print(f"{self.auth} said: {self.msg}")
        print(f"React Bot: {self.rct}")


#Create list of Message commands
def createMC():
    filename = "../Storage/text_history.csv"
    # Read the CSV file
    ret = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        prev = next(reader)  # Assuming the CSV has a header
        for row in reader:
           if row[1] == "Server" or row[1] == "DM":
               MC = Message_Command(row[1], prev[1], prev[2], prev[3], row[3])
               ret.append(MC)
           prev = row
    return ret


def authenticate(token, xsrf=None):
    # Set default values for a guest
    usr = "Guest"
    users = {}
    token = token.encode()
    for user in users:
        # loop through authenticated users and check the hash of their passwd
        auth_token = user.get("authenticationTOKEN", "")
        auth = bcrypt.checkpw(token, auth_token)
        if auth:
            # Grab username from the authenticated user
            usr = user.get("username")
            print("\nauthorized: ", usr)
            return auth, usr

    print("---Guest not authorized---")
    return False, usr



#
# # Add a channel to the banned list
# async def ban_channel(interaction: discord.interactions, channel: discord.TextChannel = None, channel_id: str = None):
#     global banned_channels
#     channel_name, channel_id = await channelInfo(interaction, bot, channel, channel_id)
#     exists = channel_id in banned_channels
#     problem = edit_banned_list(ban_file, channel_name, channel_id)
#
#     if problem or exists:
#         await interaction.response.send_message(f"Sorry, I can't ban: {channel_name}", ephemeral = True)
#     else:
#         banned_channels = banned_list_file(ban_file)
#         await interaction.response.send_message(f"I have now been banished from: {channel_name}")
#
#
# # Add a channel to the banned list
# async def unban_channel(ctx, channel: discord.TextChannel = None, channel_id: str = None):
#     global banned_channels
#     channel_name, channel_id = await channelInfo(ctx, bot, channel, channel_id)
#     exists = channel_id in banned_channels
#     problem = edit_banned_list(ban_file, channel_name, channel_id, False)
#
#     if problem or not exists:
#         await ctx.response.send_message(f"Sorry, I can't unban: {channel_name}", ephemeral = True)
#     else:
#         banned_channels = banned_list_file(ban_file)
#         await ctx.response.send_message(f"I have now been returned to: {channel_name}")

