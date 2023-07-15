import json
import sys
from re import findall
from curl_cffi import requests

config = json.loads(sys.argv[1])
prompt = config['messages'][-1]['content']

json_data = {
    'prompt': prompt,
    'options': {}
}

def format(chunk):
    try:
        completion_chunk = findall(r'content":"(.*)"},"fin', chunk.decode())[0]
        print(completion_chunk, flush=True, end='')

    except Exception as e:
        print(f'[ERROR] an error occured, retrying... | [[{chunk.decode()}]]', flush=True)
        return

while True:
    try: 
        response = requests.post('https://chatbot.theb.ai/api/chat-process', 
                            headers=headers, json=json_data, content_callback=format, impersonate='chrome110')
        
        exit(0)
    
    except Exception as e:
        print('[ERROR] an error occured, retrying... |', e, flush=True)
        continue

