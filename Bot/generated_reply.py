from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path='../Storage/.env')
client = OpenAI()

def generate_reaction(phrase, text, img=None):
    if text == "" and img is None:
        return phrase

    try:
        if img:
            phrase = image_reaction(phrase, img)
        else:
            completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a low effort reaction YouTuber who's name is React Bot but you don't say very much in your reactions"
                                "Use the following phrase to help influence a unique reaction to whatever a user says"
                                f"{phrase}"
                                "Consider discord emotes and text formating in your reactions"
                            )
                        },
                        {
                            "role": "user",
                            "content": text,
                            "store" : True
                        }
                    ]
                )
            phrase = completion.choices[0].message.content
    except Exception as e:
        pass
    print("AI used in response")
    return phrase

def image_reaction(phrase, image):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text":
                            "You are a low effort reaction YouTuber who's name is React Bot but you don't say very much in your reactions"
                            "Use the following phrase to help influence a unique reaction to whatever a user says"
                            f"{phrase}"
                            "Consider discord emotes and text formating in your reactions"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                        }
                    },
                ],
            }
        ],
        max_tokens=400,
    )
    return response.choices[0].message.content

