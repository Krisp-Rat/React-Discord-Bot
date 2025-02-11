from openai import OpenAI
import dotenv

dotenv.load_dotenv()
client = OpenAI()

def generate_reaction(phrase, text):
    if text == "":
        return phrase
    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a low effort reaction YouTuber who doesn't say very much in your reactions"
                        "Use the following phrase to help influence a unique reaction to whatever a user says"
                        f"{phrase}"
                        "Consider discord emotes and text formating in your reactions"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

    print("AI used in response")
    return completion.choices[0].message.content