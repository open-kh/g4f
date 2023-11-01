from __future__ import annotations
import json
from perplexity import Perplexity

import random, string

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, format_prompt

perplex = Perplexity()

class PerplexityAI(AsyncGeneratorProvider):
    working = True
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
        chars = string.ascii_lowercase + string.digits
        user_id = ''.join(random.choice(chars) for _ in range(24))

        count = 0
        response = perplex.search(format_prompt(messages), mode = model, search_focus=search_focus) # type: ignore
        line_len = 0
        # data = []
        for line in response:
            # data.append(line)
            line_len = len(line["chunks"]) if "chunks" in line else line_len
            content = "".join(line["chunks"][-(line_len-count):] if line_len > count else line["chunks"])
            yield content
            count = line_len

        perplex.close()
        # print(json.dumps(data))


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
