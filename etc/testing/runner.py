import json
from pydoc import doc
from g4f import ChatCompletion, models, Provider
import time
from g4f.Provider.perplexity import Perplexity

ai = Perplexity()

question = "Who are you"

def perplex():
    doct = ""
    docs = []
    for res in ai.search(question):
        response = eval(f"{res}")
        text = ""
        if ('text' in response) and ('answer' not in response):
            response["answer"] = response['text']

        if 'answer' in response:
            text = response['answer']
        elif 'chunks' in response:
            text = "".join(response['chunks'])
        else:
            docs.append(response)

        print(text[len(doct):])
        doct = text
        
    print(docs)
    ai.close()

def runner():
    path_file = "./cookie.json"
    with open(path_file, "r",encoding='utf-8') as f:
        cookies = json.load(f)
    for response in ChatCompletion.create(
            model=['concise','gpt-4','gpt-3.5-turbo','perplexity'][0],
            provider= Provider.HuggingChat,
            messages=[{"role": "user", "content": question}],
            temperature=0.1,
            auth=True,
            stream=True,
            cookies = cookies,
        ):
        print(response, end="", flush=True)
        time.sleep(0.1)

# perplex()
runner()