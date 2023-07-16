import json
import sys
from queue import Queue, Empty
from threading import Thread
from re import findall
from curl_cffi import requests
from fake_useragent import UserAgent
from typing import Generator, Optional


class Completion:
    # experimental
    part1 = '{"role":"assistant","id":"chatcmpl'
    part2 = '"},"index":0,"finish_reason":null}]}}'
    regex = rf'{part1}(.*){part2}'

    timer = None
    message_queue = Queue()
    stream_completed = False
    last_msg_id = None

    @staticmethod
    def request(prompt: str, proxy: Optional[str] = None):
        headers = {
            'authority': 'chatbot.theb.ai',
            'content-type': 'application/json',
            'origin': 'https://chatbot.theb.ai',
            'user-agent': UserAgent().random,
        }

        proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy} if proxy else None
        
        options = {}
        if Completion.last_msg_id:
            options['parentMessageId'] = Completion.last_msg_id
        
        requests.post(
            'https://chatbot.theb.ai/api/chat-process',
            headers=headers,
            proxies=proxies,
            content_callback=Completion.handle_stream_response,
            json={'prompt': prompt, 'options': options},
            timeout=100000
        )

        Completion.stream_completed = True

    @staticmethod
    def create(prompt: str, proxy: Optional[str] = None) -> Generator[str, None, None]:
        Completion.stream_completed = False
        
        Thread(target=Completion.request, args=[prompt, proxy]).start()

        while not Completion.stream_completed or not Completion.message_queue.empty():
            try:
                message = Completion.message_queue.get(timeout=0.01)
                # print(message)
                for message in findall(Completion.regex, message):
                    message_json = json.loads(Completion.part1 + message + Completion.part2)
                    Completion.last_msg_id = message_json['id']
                    yield message_json['delta']

            except Empty:
                pass

    @staticmethod
    def handle_stream_response(response):
        Completion.message_queue.put(response.decode())

    @staticmethod
    def get_response(prompt: str, proxy: Optional[str] = None) -> str:
        response_list = []
        for message in Completion.create(prompt, proxy):
            response_list.append(message)
        return ''.join(response_list)
        
        Completion.message_queue.put(response.decode(errors='replace'))


config = json.loads(sys.argv[1])
# proxy = config['proxy'] or None
prompt = config['messages'][-1]['content']

conversation = "You are Open Brain, a large language model trained by OpenAI using gpt-4-32k. Follow the user's instructions carefully. Respond using markdown."
for message in config['messages']:
    conversation += '%s: %s\n' % (message['role'], message['content'])

conversation += 'assistant: '

def format(chunk):
    try:
        completion_chunk = findall(r'content":"(.*)"},"fin', chunk.decode())[0]
        print(completion_chunk, flush=True, end='')

    except Exception as e:
        print(f'[ERROR] an error occured, retrying... | [[{chunk.decode()}]]', flush=True)
        return

while True:
    try:
        for token in Completion.create(conversation):
            print(token, end='', flush=True)
        # response = requests.post('https://chatbot.theb.ai/api/chat-process', 
        #                     headers=headers, json=json_data, content_callback=format, impersonate='chrome110')
        exit(0)
    
    except Exception as e:
        print('[ERROR] an error occured, retrying... |', e, flush=True)
        continue