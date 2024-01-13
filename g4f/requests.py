from __future__ import annotations

import warnings
import string
import json
import socket
import ipaddress
import struct
import random
import asyncio
from functools import partialmethod
from asyncio import Future, Queue
from typing import AsyncGenerator, Union, Optional



from curl_cffi.requests import AsyncSession, Response, Cookies
import curl_cffi
import requests

is_newer_0_5_8: bool = hasattr(AsyncSession, "_set_cookies") or hasattr(Cookies, "get_cookies_for_curl")
is_newer_0_5_9: bool = hasattr(curl_cffi.AsyncCurl, "remove_handle")
is_newer_0_5_10: bool = hasattr(AsyncSession, "release_curl")

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES  # 2 ** 32 - 1
MAX_IPV6 = ipaddress.IPv6Address._ALL_ONES  # 2 ** 128 - 1

proxies_list = open("rotating_proxies.txt", "r").read().strip().split("\n")

def get(url, proxy): 
	try: 
		# Send proxy requests to the final URL 
		response = requests.get(url, proxies={'http': f"http://{proxy}"}, timeout=30) 
		print(proxy,response.status_code, response.text) 
	except Exception as e: 
		print(e) 
 
def check_proxies(): 
	proxy = proxies_list[random.randint(0, len(proxies_list) - 1)]
	get("https://replicate.com", proxy)

def random_ipv4():
    return  ipaddress.IPv4Address._string_from_ip_int(
        random.randint(0, MAX_IPV4)
    )

def random_ipv6():
    return ipaddress.IPv6Address._string_from_ip_int(
        random.randint(0, MAX_IPV6)
    )

def generate_public_ip():
    socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def random_IP():
    return f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def random_port():
    return random.randint(1024, 65535)

def random_url():
    return f"http://{random_IP()}:{random_port()}"

def random_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }


def generate_random_string(length=32):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

class StreamResponse:
    def __init__(self, inner: Response, queue: Queue[bytes]) -> None:
        self.inner: Response = inner
        self.queue: Queue[bytes] = queue
        self.request = inner.request
        self.status_code: int = inner.status_code
        self.reason: str = inner.reason
        self.ok: bool = inner.ok
        self.headers = inner.headers
        self.cookies = inner.cookies

    async def text(self) -> str:
        content: bytes = await self.read()
        return content.decode()

    def raise_for_status(self) -> None:
        if not self.ok:
            raise RuntimeError(f"HTTP Error {self.status_code}: {self.reason}")

    async def json(self, **kwargs) -> dict:
        return json.loads(await self.read(), **kwargs)

    async def iter_lines(
        self, chunk_size: Optional[int] = None, decode_unicode: bool = False, delimiter: Optional[str] = None
    ) -> AsyncGenerator[bytes, None]:
        """
        Copied from: https://requests.readthedocs.io/en/latest/_modules/requests/models/
        which is under the License: Apache 2.0
        """

        pending: bytes = None # type: ignore

        async for chunk in self.iter_content(
            chunk_size=chunk_size, decode_unicode=decode_unicode
        ):
            if pending is not None:
                chunk = pending + chunk
            lines = chunk.split(delimiter) if delimiter else chunk.splitlines() # type: ignore
            if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
                pending = lines.pop()
            else:
                pending = None

            for line in lines:
                yield line

        if pending is not None:
            yield pending

    async def iter_content(
        self, chunk_size: Optional[int] = None, decode_unicode: bool = False
    ) -> AsyncGenerator[bytes, None]:
        if chunk_size:
            warnings.warn("chunk_size is ignored, there is no way to tell curl that.")
        if decode_unicode:
            raise NotImplementedError()
        while True:
            chunk = await self.queue.get()
            if chunk is None:
                return
            yield chunk

    async def read(self) -> bytes:
        return b"".join([chunk async for chunk in self.iter_content()])


class StreamRequest:
    def __init__(self, session: AsyncSession, method: str, url: str, **kwargs: Union[bool, int, str]) -> None:
        self.session: AsyncSession = session
        self.loop: asyncio.AbstractEventLoop = session.loop if session.loop else asyncio.get_running_loop()
        self.queue: Queue[bytes] = Queue()
        self.method: str = method
        self.url: str = url
        self.options: dict = kwargs
        self.handle: Optional[curl_cffi.AsyncCurl] = None

    def _on_content(self, data: bytes) -> None:
        if not self.enter.done():
            self.enter.set_result(None)
        self.queue.put_nowait(data)

    def _on_done(self, task: Future) -> None:
        if not self.enter.done():
            self.enter.set_result(None)
        self.queue.put_nowait(None)

        self.loop.call_soon(self.release_curl)

    async def fetch(self) -> StreamResponse:
        if self.handle:
            raise RuntimeError("Request already started")
        self.curl: curl_cffi.AsyncCurl = await self.session.pop_curl()
        self.enter: asyncio.Future = self.loop.create_future()
        if is_newer_0_5_10:
            request, _, header_buffer, _, _ = self.session._set_curl_options(
                self.curl,
                self.method,
                self.url,
                content_callback=self._on_content,
                **self.options
            )
        else:
            request, _, header_buffer = self.session._set_curl_options(
                self.curl,
                self.method,
                self.url,
                content_callback=self._on_content,
                **self.options
            )
        if is_newer_0_5_9:
            self.handle = self.session.acurl.add_handle(self.curl)
        else:
            await self.session.acurl.add_handle(self.curl, False)
            self.handle = self.session.acurl._curl2future[self.curl]
        self.handle.add_done_callback(self._on_done)
        # Wait for headers
        await self.enter
        # Raise exceptions
        if self.handle.done():
            self.handle.result()
        if is_newer_0_5_8:
            response = self.session._parse_response(self.curl, _, header_buffer)
            response.request = request
        else:
            response = self.session._parse_response(self.curl, request, _, header_buffer)
        return StreamResponse(response, self.queue)

    async def __aenter__(self) -> StreamResponse:
        return await self.fetch()

    async def __aexit__(self, *args) -> None:
        self.release_curl()

    def release_curl(self) -> None:
        if is_newer_0_5_10:
            self.session.release_curl(self.curl)
            return
        if not self.curl:
            return
        self.curl.clean_after_perform()
        if is_newer_0_5_9:
            self.session.acurl.remove_handle(self.curl)
        elif not self.handle.done() and not self.handle.cancelled():
            self.session.acurl.set_result(self.curl)
        self.curl.reset()
        self.session.push_curl(self.curl)
        self.curl = None


class StreamSession(AsyncSession):
    def request(
        self, method: str, url: str, **kwargs
    ) -> StreamRequest:
        return StreamRequest(self, method, url, **kwargs)

    head = partialmethod(request, "HEAD")
    get = partialmethod(request, "GET")
    post = partialmethod(request, "POST")
    put = partialmethod(request, "PUT")
    patch = partialmethod(request, "PATCH")
    delete = partialmethod(request, "DELETE")