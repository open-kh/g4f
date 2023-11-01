from __future__ import annotations

from perplexity import Perplexity

import random, string
from datetime import datetime

from ..typing import AsyncResult, Messages
from ..requests import StreamSession
from .base_provider import AsyncGeneratorProvider, format_prompt

perplex = Perplexity()

class PerplexityAI:

    @classmethod
    async def create_async_generator(
        cls,
        messages: Messages,
        proxy: str = None, # type: ignore
        timeout: int = 120,
        **kwargs
    ) -> AsyncResult:
        chars = string.ascii_lowercase + string.digits
        user_id = ''.join(random.choice(chars) for _ in range(24))

        async with StreamSession(
            timeout=(5, timeout),
            proxies={"https": proxy},
            impersonate="chrome107"
        ) as session:
            count = 0
            async with perplex.search(format_prompt(messages)) as response:
                response.raise_for_status()
                line_len = 0
                async for line in response.iter_lines():
                    line_len = len(line["chunks"]) if "chunks" in line else line_len
                    content = "".join(line["chunks"][-(line_len-count):] if line_len > count else line["chunks"])
                    yield content
                    count = line_len


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