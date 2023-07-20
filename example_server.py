import openai
import sys

openai.api_key = ""
openai.api_base = "http://127.0.0.1:1337"

chat_completion = openai.ChatCompletion.create(stream=True,
                                    model="gpt-3.5-turbo", 
                                    messages=[{"role": "user", 
                                            "content": "Write a poem about a tree."}])

for token in chat_completion:   
    content = token["choices"][0]["delta"].get("content")
    if content is not None:
        print(content, end="")
        sys.stdout.flush()
        
