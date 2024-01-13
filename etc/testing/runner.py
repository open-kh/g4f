from abc import get_cache_token
import json
from pydoc import doc
import random
from arrow import get

from sqlalchemy import Null
from g4f import ChatCompletion, models, Provider
import time
from g4f.Provider import (ClaudeAI)
from g4f.Provider.helper import get_cookies

question = "Hello, who are you"

# path_file = "access_token_claude.txt"
cookies = open("access_token_claude.txt", "r").read()
# cookies = get_cookies('claude.ai')

# print(cookies)
# with open(path_file, "r") as f:

ai = ClaudeAI(cookies)

ids = []
def runner():
    conversations = ai.list_all_conversations()
    for conversation in conversations:
        ids.append(conversation['uuid'])

def chat():
    if len(ids) == 0:
        runner()
    chat_id = "a438087b-9039-4330-9fce-bb02fd039c11"
    # chat_id = random.choices(ids)[0]
    # print(chat_id)
    # response = ai.create_new_chat()
    response = ai.send_message(question,chat_id)
    print(response)
# perplex()
# runner()
chat()