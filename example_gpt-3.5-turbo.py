import g4f
import sys

# Automatic selection of provider, streamed completion
response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', 
                                    messages=[{"role": "user", 
                                            "content": "Write a poem about a tree."}], 
                                    stream=True)
                                     
for message in response:
    print(message, end="")
    sys.stdout.flush()
