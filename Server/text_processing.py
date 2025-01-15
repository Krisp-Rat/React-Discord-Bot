import os
import csv
from datetime import datetime

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



def clear_server(Server_name):
    file_path = "../Storage/text_history.csv"

    # Create a temporary list to store filtered rows
    filtered_rows = []

    # Read the CSV file
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Assuming the CSV has a header
        filtered_rows.append(header)  # Add the header to the filtered list

        for row in reader:
            if row[0] != Server_name:  # Check if the value in the first column matches
                filtered_rows.append(row)

    # Write the filtered rows back to the CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(filtered_rows)
