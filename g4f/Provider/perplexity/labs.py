from os import listdir
from traceback import print_tb
from uuid import uuid4
from time import sleep, time
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp
from requests import Session, get, post

class Labs:
    def __init__(self) -> None:
        self._startSocket()
        while not (self.ws.sock and self.ws.sock.connected):
            sleep(0.01)

    def _startSocket(self):
        self.history: list = []
        self.session: Session = Session()
        # self.user_agent: dict = { "User-Agent": "Ask/2.2.1/334 (iOS; iPhone) isiOSOnMac/false", "X-Client-Name": "Perplexity-iOS" }
        self.user_agent: dict = { 
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0", 
            "X-Firefox-Spdy": "h2"
        }
        self.session.headers.update(self.user_agent)
        self._init_session_without_login()

        self.sid: str = self._get_sid()
    
        self.queue: list = []
        self.finished: bool = True
        self.ws: WebSocketApp = self._init_websocket()
        self.ws_thread: Thread = Thread(target=self.ws.run_forever).start()

    def _init_session_without_login(self) -> None:
        # self.session.get(url=f"https://www.perplexity.ai/search/{str(uuid4())}")
        self.session.get(url="https://labs.perplexity.ai")
        # print(self.user_agent)
        self.session.headers.update(self.user_agent)

    def _get_sid(self) -> str:
        return loads(self.session.get(
            url=f"https://labs-api.perplexity.ai/socket.io/?transport=polling&EIO=4"
        ).text[1:])["sid"]

    def _get_cookies_str(self) -> str:
        cookies = ""
        for key, value in self.session.cookies.get_dict().items():
            cookies += f"{key}={value}; "
        return cookies[:-2]

    def _init_websocket(self) -> WebSocketApp:
        def on_open(ws: WebSocketApp) -> None:
            ws.send("2probe")
            ws.send("5")
            
        format_chat = {
            "answer": "Hello, world",
            'status': 'completed',
            'mode': 'concise',
        }

        def on_message(ws: WebSocketApp, message: str) -> None:
            if message == "2":
                ws.send("3")
            elif message.startswith("42"):
                content = loads(message[2:])
                text = content[1]
                if text["final"] == True:
                    self.finished = True
                    self.history.append({"role": "assistant", "content": text['output'], "priority": 0})
                elif ("output" in text) and (text["final"] == False):
                    format_chat["answer"] = text['output']
                    format_chat["status"] = "failed"
                    self.queue.append(format_chat)

        headers: dict = self.user_agent
        headers["Cookie"] = self._get_cookies_str()

        # print('new websocket',self.sid)

        return WebSocketApp(
            url=f"wss://labs-api.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header=headers,
            on_open=on_open,
            on_message=on_message,
            on_error=lambda ws, err: print(f"websocket error: {err}")
        )
    
    def _c(self, prompt: str, model: str) -> dict:
        while not (self.ws.sock and self.ws.sock.connected):
            self._startSocket()
            
        assert self.finished, "already searching"
        assert model in ["codellama-34b-instruct", "llama-2-13b-chat", "llama-2-70b-chat", "mistral-7b-instruct", "pplx-7b-chat-alpha", "pplx-70b-chat-alpha"]
        self.finished = False
        self.history.append({"role": "user", "content": prompt, "priority": 0})
        # self.history
        # self.ws.send("42[\"perplexity_playground\",{\"version\":\"2.1\",\"source\":\"default\",\"model\":\"" + model + "\",\"messages\":" + dumps(self.history) + "}]")
        mess = f'42["perplexity_labs",{"version":"2.2","source":"default","model":"{model}","messages":{prompt},"timezone":"Asia/Phnom_Penh"}]'
        print(mess)
        self.ws.send(mess)
    
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
