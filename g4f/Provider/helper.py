from __future__ import annotations

from __future__ import annotations

import sys
import time
import random
import string
from tokenize import String
import asyncio
from typing import Optional
import webbrowser
from aiohttp import BaseConnector, ClientConnectionError, ClientSession

from os              import path
from asyncio         import AbstractEventLoop
from platformdirs    import user_config_dir

from ..typing        import Dict, Messages
from browser_cookie3 import chrome, chromium, opera, opera_gx, brave, edge, vivaldi, firefox, BrowserCookieError
from .. import debug

# Change event loop policy on windows
if sys.platform == 'win32':
    if isinstance(
        asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Local Cookie Storage
_cookies: Dict[str, Dict[str, str]] = {}

# If event loop is already running, handle nested event loops
# If "nest_asyncio" is installed, patch the event loop.
def get_event_loop() -> AbstractEventLoop:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())
            return asyncio.get_event_loop()
    try:
        event_loop = asyncio.get_event_loop()
        if not hasattr(event_loop.__class__, "_nest_patched"):
            import nest_asyncio
            nest_asyncio.apply(event_loop)
        return event_loop
    except ImportError:
        raise RuntimeError(
            'Use "create_async" instead of "create" function in a running event loop. Or install the "nest_asyncio" package.'
        )

def init_cookies():
    urls = [
        'https://chat-gpt.org',
        'https://www.aitianhu.com',
        'https://chatgptfree.ai',
        'https://gptchatly.com',
        'https://bard.google.com',
        'https://huggingface.co/chat',
        'https://open-assistant.io/chat'
    ]

    browsers = ['google-chrome', 'chrome', 'firefox', 'safari']

    def open_urls_in_browser(browser):
        b = webbrowser.get(browser)
        for url in urls:
            b.open(url, new=0, autoraise=True)

    for browser in browsers:
        try:
            open_urls_in_browser(browser)
            break 
        except webbrowser.Error:
            continue

# Load cookies for a domain from all supported browsers.
# Cache the results in the "_cookies" variable.
def get_cookies(domain_name=''):
    if domain_name in _cookies:
        return _cookies[domain_name]
    def g4f(domain_name):
        user_data_dir = user_config_dir("g4f")
        cookie_file = path.join(user_data_dir, "Default", "Cookies")
        return [] if not path.exists(cookie_file) else chrome(cookie_file, domain_name)

    cookies = {}
    for cookie_fn in [g4f, chrome, chromium, opera, opera_gx, brave, edge, vivaldi, firefox]:
        try:
            cookie_jar = cookie_fn(domain_name=domain_name)
            if len(cookie_jar) and debug.logging:
                print(f"Read cookies from {cookie_fn.__name__} for {domain_name}")
            for cookie in cookie_jar:
                if cookie.name not in cookies:
                    cookies[cookie.name] = cookie.value
        except BrowserCookieError as e:
            pass
    _cookies[domain_name] = cookies
    return _cookies[domain_name]


def format_prompt(messages: Messages, add_special_tokens=False) -> str:
    if not add_special_tokens and len(messages) <= 1:
        return messages[0]["content"]
    formatted = "\n".join(
        [
            f'{message["role"].capitalize()}: {message["content"]}' for message in (messages[-2:] if len(messages)>2 else messages)
        ]
    )
    return f"{formatted}\nAssistant:"


def get_browser(user_data_dir: str = None):
    from undetected_chromedriver import Chrome

    if not user_data_dir:
        user_data_dir = user_config_dir("g4f")

    return Chrome(user_data_dir=user_data_dir)

def get_connector(connector: BaseConnector = None, proxy: str = None) -> Optional[BaseConnector]:
    if proxy and not connector:
        try:
            from aiohttp_socks import ProxyConnector
            connector = ProxyConnector.from_url(proxy)
        except ImportError:
            raise MissingRequirementsError('Install "aiohttp_socks" package for proxy support')
    return connector


completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))
completion_timestamp = int(time.time())

class response_callback:
    def __init__(self,completion_id,model,chunk) -> None:
        self.model = model if model is String else "default"
        self.completion_id = completion_id
        self.chunk = chunk

    def to_dict(self):
        finish = None
        if self.chunk is True:
            finish = 'stop'
            self.chunk = {}
        else:
            self.chunk = {'content': self.chunk}
        return {
            'id': f'chatcmpl-{self.completion_id}',
            'object': 'chat.completion.chunk',
            'created': int(time.time()),
            'model': self.model,
            'choices': [
                {
                    'index': 0,
                    'delta': self.chunk,
                    'finish_reason': finish,
                }
            ],
        }
    

TURN_TEMPLATE = "###{role}:\n{content}"
FORMAT_TEMPLATE = "###Instruction:\nI am a helpful, respectful, honest and safe AI assistant built by Mr. Phearum.\n{message}\n###Response:\n"
TURN_PREFIX = "<|im_start|>{role}\n"

def seallm_format_prompt(conversations, add_assistant_prefix = False, system_prompt=None):
    # conversations: list of dict with key `role` and `content` (openai format)
    if conversations[0]['role'] != 'system' and system_prompt is not None:
        conversations = [{"role": "system", "content": system_prompt}] + conversations
    text = ''
    for turn_id, turn in enumerate(conversations):
        prompt = TURN_TEMPLATE.format(role= "Question" if turn['role'] == 'user' else "Response", content=turn['content'])
        text += prompt
    if add_assistant_prefix:
        prompt = TURN_PREFIX.format(role='assistant')
        text += prompt   
    # print(text) 
    return FORMAT_TEMPLATE.format(message=text)


class WebSocketClient:

    def __init__(self, url):
        self.url = url
        self.session = ClientSession()
        self.ws = None
        self.queue: list = []
        self.finished = False

    async def connect(self):
        while True:
            try:
                self.ws = await self.session.ws_connect(self.url)
                print("Connected to", self.url)
                await self.receive()
            except ClientConnectionError as e:
                print("Connection error:", e)
            print("Reconnecting to", self.url)
            await asyncio.sleep(1) # wait before reconnecting

    async def receive(self):
        async for msg in self.ws:
            # handle websocket messages here
            if msg == "2":
                self.ws.send("3")
            elif msg.startswith("42"):
                msg = loads(msg[2:])[1]
                if "status" not in msg:
                    self.queue.append(msg)
                elif msg["status"] == "completed":
                    self.finished = True
                    self.history.append({"role": "assistant", "content": msg["output"], "priority": 0})
                elif msg["status"] == "failed":
                    self.finished = True
            print(msg)

    async def close(self):
        await self.session.close()