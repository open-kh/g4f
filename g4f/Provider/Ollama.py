from __future__ import annotations
import json

from openai import OpenAI

from aiohttp import BaseConnector

from .base_provider import AsyncGeneratorProvider
import ollama

from ..typing import Messages

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

class Ollama(AsyncGeneratorProvider):
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
        chat_completion = client.chat.completions.create(
            messages= messages,
            model = model or 'seallm',
            stream=True,
        )
        return chat_completion
