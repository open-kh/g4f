from __future__ import annotations
import json
from urllib import response

from ..websocket import WebSocket
from .perplexity import Perplexity

import random, string

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, format_prompt

class SeaLLM(AsyncGeneratorProvider):
    working = True
    count_check = 0

    def __init__(self):
        self.ws = WebSocket()._init_websocket()

    @classmethod
    async def create_async_generator(
        cls,
        model: str, # type: ignore
        messages: Messages,
        search_focus: str = "internet",
        proxy: str = None, # type: ignore
        timeout: int = 120,
        **kwargs
    ) -> AsyncResult:
        socket = WebSocket()
        self.ws = socket._init_websocket()
        # chars = string.ascii_lowercase + string.digits
        # user_id = ''.join(random.choice(chars) for _ in range(24))
        doct = "" 
        text = ""
        for line in perplex.search(format_prompt(messages), mode = model, search_focus=search_focus): # type: ignore
            text = cls.check_answer(line)
            yield text[len(doct):] # type: ignore
            doct = text

        perplex.close()


    @classmethod
    def check_answer(cls, response):
        try:
            text = ""
            if 'answer' in response:
                text = response['answer']
            elif 'chunks' in response:
                text = "".join(response['chunks'])
            elif 'text' in response:
                response["answer"] = json.dumps(response['text'],separators=(',', ':'))
                cls.check_answer(response)

            return text
        except json.decoder.JSONDecodeError:
            pass


    @classmethod
    @property
    def params(cls):
        params = [
            ("model", "str"),
            ("messages", "list[dict[str, str]]"),
            ("stream", "bool"),
            ("proxy", "str"),
            ("timeout", "int"),
        ]
        param = ", ".join([": ".join(p) for p in params])
        return f"g4f.provider.{cls.__name__} supports: ({param})"
    

    def _init_websocket(self) -> WebSocketApp:
        def on_open(ws: WebSocketApp) -> None:
            ws.send("2probe")
            ws.send("5")

        def on_message(ws: WebSocketApp, message: str) -> None:
            if message == "2":
                ws.send("3")
            elif message.startswith("42"):
                message = loads(message[2:])[1]
                if "status" not in message:
                    self.queue.append(message)
                elif message["status"] == "completed":
                    self.finished = True
                    self.history.append({"role": "assistant", "content": message["output"], "priority": 0})
                elif message["status"] == "failed":
                    self.finished = True

        headers: dict = self.user_agent
        headers["Cookie"] = self._get_cookies_str()

        return WebSocketApp(
            url=f"wss://{self.app_url}/queue/join",
            header=headers,
            on_open=on_open,
            on_message=on_message,
            on_error=lambda ws, err: print(f"websocket error: {err}")
        )
