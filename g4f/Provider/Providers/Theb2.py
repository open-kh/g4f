import os
import json
from queue import Queue, Empty
from re import findall
from threading import Thread

from curl_cffi import requests
from fake_useragent import UserAgent

from ...typing import get_type_hints, Optional

url = 'https://theb.ai'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, proxy: Optional[str] = None, **kwargs):
    conversation = "You are Open Brain, a large language model trained by OpenAI using gpt-4-32k. Follow the user's instructions carefully. Respond using markdown."
    for message in messages:
        conversation += '%s: %s\n' % (message['role'], message['content'])
    
    conversation += 'assistant: '
    for token in Completion.create(conversation):
        print(token, end='', flush=True)

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

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])