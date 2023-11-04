from __future__ import annotations
import json
from urllib import response
from .perplexity import Perplexity

import random, string

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, format_prompt

class PerplexityAI(AsyncGeneratorProvider):
    working = True
    count_check = 0
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
        perplex = Perplexity()
        # chars = string.ascii_lowercase + string.digits
        # user_id = ''.join(random.choice(chars) for _ in range(24))
        doct, text = ""
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
