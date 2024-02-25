from __future__ import annotations

from g4f.Provider.helper import seallm_format_prompt

from .base_provider import AsyncGeneratorProvider

from ..typing import AsyncResult, Messages

class Ollama(AsyncGeneratorProvider):
    working = True
    default_model = 'seallm'

    @classmethod
    def _chat(cls, chunk: dict) -> str:
        if not chunk.get('done'):
            return chunk['response']
        return ''

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        **kwargs
    )-> AsyncResult:
        streaming = ollama.generate(model= model or cls.default_model,
                                    prompt=seallm_format_prompt(messages),
                                    stream=True)
        try:
            for chunk in streaming:
                if chunk['done'] is True:
                    break
                yield chunk['response']
        except Exception as e:
            print("Error: {0}".format(e))
