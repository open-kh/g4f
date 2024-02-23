from __future__ import annotations
import json

from aiohttp import BaseConnector

from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
import ollama

from ..typing import Messages

class SeaLLM(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://labs.perplexity.ai"    
    working = True
    default_model = 'seallm'
    models = [
        'seallm', 'seallm2', 'llama2'
    ]

    @classmethod
    def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        **kwargs
    ):
        return ollama.chat(
            model= model if model in cls.models else cls.default_model,
            messages=[
                {'role': 'user', 'content': format_prompt(messages)}
            ],
            stream=True,
        )
        # for chunk in stream:
            # yield (chunk['message']['content']).lstrip()
            # print(chunk['message']['content'], end='', flush=True)
            # yield chunk['message']['content']
        # for chunk in yield_content_from_stream(stream):
        #     print(chunk['message']['content'], end='', flush=True)


def yield_content_from_stream(stream):
    for chunk in stream:
        yield chunk['message']['content']

TURN_TEMPLATE = "<|im_start|>\n{content}</s>"
def format_prompt(conversations):
    text = ''
    for turn_id, turn in enumerate(conversations):
        prompt = TURN_TEMPLATE.format(role=turn['role'], content=turn['content'])
        text += prompt
    return "<|im_start|>system\nI am a helpful, respectful, honest and safe AI assistant built by Mr. Phearum.</s>\n"+text