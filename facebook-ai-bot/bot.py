from fbchat import Client
from fbchat.models import *
import requests, json, os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ai_reply(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-2-13b-chat",
        "messages": [
            {"role": "system", "content": "You are a chatbot made by Nabil, a game developer from Bangladesh."},
            {"role": "user", "content": user_message}
        ]
    }
    r = requests.post(url, headers=headers, json=data)
    return r.json()["choices"][0]["message"]["content"]

with open("fbstate.json", "r") as f:
    session = json.load(f)

class MessengerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id != self.uid:
            reply = ai_reply(message_object.text)
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

client = MessengerBot("", "", session_cookies=session)
client.listen()
