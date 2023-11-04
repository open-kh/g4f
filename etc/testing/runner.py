import json
from pydoc import doc
from g4f import ChatCompletion, models, Provider
import time
from g4f.Provider.perplexity import Perplexity

ai = Perplexity()

question = "Hello, Who are you"

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
    for response in ChatCompletion.create(
            model=['concise','gpt-4','gpt-3.5-turbo','perplexity'][2],
            provider= Provider.Phind,
            messages=[{"role": "user", "content": question}],
            temperature=0.1,
            auth=True,
            stream=True
        ):
        print(response, end="", flush=True)
        time.sleep(0.1)

runner()