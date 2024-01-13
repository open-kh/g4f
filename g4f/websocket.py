from os import listdir
from uuid import uuid4
from time import sleep, time
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp
from requests import Session, get, post

app_url = "seallms-seallm-chat-13b.hf.space"

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept': 'application/json',
    'Referer': f'https://{app_url}',
    'Origin': f'http://{app_url}',
    'Host': f'{app_url}',
    'TE': 'trailers',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept': '*/*'
}

class WebSocket:

    def __init__(self) -> None:
        self.app_url = app_url
        self.history: list = []
        self.session: Session = Session()
        self.user_agent: dict = header
        self.session.headers.update(self.user_agent)
    
        self.queue: list = []
        self.finished: bool = True

        self.ws: WebSocketApp = self._init_websocket()
        self.ws_thread: Thread = Thread(target=self.ws.run_forever).start()

        while not (self.ws.sock and self.ws.sock.connected):
            sleep(0.01)

    def _get_cookies_str(self) -> str:
        cookies = ""
        for key, value in self.session.cookies.get_dict().items():
            cookies += f"{key}={value}; "
        return cookies[:-2]

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
    
    def _c(self, prompt: str, model: str) -> dict:
        assert self.finished, "already searching"
        assert model in ["codellama-34b-instruct", "llama-2-13b-chat", "llama-2-70b-chat", "mistral-7b-instruct", "pplx-7b-chat-alpha", "pplx-70b-chat-alpha"]
        self.finished = False
        self.history.append({"role": "user", "content": prompt, "priority": 0})
        self.ws.send("42[\"perplexity_playground\",{\"version\":\"2.1\",\"source\":\"default\",\"model\":\"" + model + "\",\"messages\":" + dumps(self.history) + "}]")
    
    def chat(self, prompt: str, model: str = "mistral-7b-instruct") -> dict:
        self._c(prompt, model)

        while (not self.finished) or (len(self.queue) != 0):
            if len(self.queue) > 0:
                yield self.queue.pop(0)

    def chat_sync(self, prompt: str, model: str = "llama-2-7b-chat") -> dict:
        self._c(prompt, model)

        while not self.finished:
            pass

        return self.queue.pop(-1)

    def close(self) -> None:
        self.ws.close()
