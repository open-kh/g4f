from __future__  import annotations
from dataclasses import dataclass

from g4f.Provider import PerplexityLabs, SeaLLM, perplexity


from .typing     import Union
from .Provider   import BaseProvider, RetryProvider
from .Provider   import (
    PerplexityAI,
    Llama2,
    Vercel,
    Phind,
    Bing,
)

@dataclass(unsafe_hash=True)
class Model:
    name: str
    base_provider: str
    best_provider: Union[type[BaseProvider], RetryProvider] = None
    
    @staticmethod
    def __all__() -> list[str]:
        return _all_models

default = Model(
    name          = "",
    base_provider = "",
    best_provider = RetryProvider([
        Bing,         # Not fully GPT 3 or 4
        Phind
    ])
)

# GPT-3.5 too, but all providers supports long responses and a custom timeouts
gpt_35_long = Model(
    name          = 'gpt-3.5-turbo',
    base_provider = 'openai',
    best_provider = Phind
)

# H2o
copilot = Model(
    name          = "copilot",
    base_provider = 'perplexity',
    best_provider = PerplexityAI
)

concise = Model(
    name          = "concise",
    base_provider = 'perplexity',
    best_provider = PerplexityAI
)

seallm = Model(
    name          = "seallm",
    base_provider = 'seallm',
    best_provider = SeaLLM
)

perplexity_llama_2_70b = Model(
    name          = "llama-2-70b-chat",
    base_provider = 'perplexity',
    best_provider = PerplexityLabs
)
perplexity_pplx_70b = Model(
    name          = "pplx-70b-chat",
    base_provider = 'perplexity',
    best_provider = PerplexityLabs
)

perplexity_pplx_70b_online = Model(
    name          = "pplx-70b-online",
    base_provider = 'perplexity',
    best_provider = PerplexityLabs
)

# GPT-3.5 / GPT-4
gpt_35_turbo = Model(
    name          = 'gpt-3.5-turbo',
    base_provider = 'openai',
    best_provider=  Phind
)

gpt_4 = Model(
    name          = 'gpt-4',
    base_provider = 'openai',
    best_provider = RetryProvider([
        Bing, Phind
    ])
)


class ModelUtils:
    convert: dict[str, Model] = {
        'concise'       : concise,
        'copilot'       : copilot,

        # gpt
        'gpt-3.5-turbo' : gpt_35_turbo,
        'gpt-4'         : gpt_4,

        # Ollama
        'seallm'        : seallm,

        # perplexity
        'perplexity_llama2_70b'     : perplexity_llama_2_70b,
        'perplexity_pplx_70b'       : perplexity_pplx_70b,
        'perplexity_pplx_70b_online': perplexity_pplx_70b_online,
    }

_all_models = list(ModelUtils.convert.keys())