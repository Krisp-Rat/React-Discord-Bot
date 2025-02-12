import csv

class Message_Command:
    def __init__(self, env, usr, auth, msg, rct):
        self.env = env
        self.usr = usr
        self.auth = auth
        self.msg = msg
        self.rct = rct

    def returnElement(self):
        info = {"env": self.env, "usr": self.usr, "auth": self.auth, "msg": self.msg, "rct": self.rct}
        return info

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

# stats = createMC()
# for stat in stats: stat.print()

