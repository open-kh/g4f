import json
import sys
from re import findall
import queue
from curl_cffi import requests
# import requests

config = json.loads(sys.argv[1])
prompt = "You are Open Brain, a large language model trained by OpenAI using gpt-4-32k. Follow the user's instructions carefully. Respond using markdown."
for message in config['messages']:
    prompt += '%s: %s\n' % (message['role'], message['content'])

prompt += 'assistant: '
# print(prompt,config)
# print("Phearum")

headers = {
    'authority': 'chatbot.theb.ai',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
    'content-type': 'application/json',
    'origin': 'https://chatbot.theb.ai',
    'referer': 'https://chatbot.theb.ai/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

json_data = {
    'prompt': prompt,
    'options': {}
}


chunks_queue = queue.Queue()
error = None
response = None
# text = ''
def callback(chunk):
    # global text
    try:
        # text += chunk
        # print(chunk)
        completion_chunk = findall(r'content":"(.*)"},"fin', chunk.decode())[0]
        # print(completion_chunk)
        print(completion_chunk,flush=True, end='')

    except Exception as e:
        print(f'[ERROR] an error occured, retrying... | [[{chunk.decode()}]]', flush=True)
        return

while True:
    # text = ''
    try: 
        requests.post('https://chatbot.theb.ai/api/chat-process', headers=headers, json=json_data, content_callback=callback, impersonate='chrome110')
        # response = requests.post('https://chatbot.theb.ai/api/chat-process', headers=headers, data=json.dumps(json_data))
        # for token in response:
        #     if b'delta' in token:
        #         token = json.loads(token.decode().split('data: ')[1])['delta']
        #         print(token)
        # print(text)

        exit(0)
    
    except Exception as e:
        print('[ERROR] an error occured, retrying... |', e, flush=True)
        continue