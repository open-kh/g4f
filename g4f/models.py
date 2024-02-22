from __future__  import annotations
from dataclasses import dataclass

from g4f.Provider import PerplexityLabs, SeaLLM, perplexity


from .typing     import Union
from .Provider   import BaseProvider, RetryProvider
from .Provider   import (
    GptForLove,
    PerplexityAI,
    ChatgptAi,
    GptChatly,
    DeepInfra,
    ChatgptX,
    ChatBase,
    GeekGpt,
    FakeGpt,
    FreeGpt,
    NoowAi,
    Llama2,
    Vercel, 
    Aichat,
    GPTalk,
    AiAsk,
    GptGo,
    Phind,
    Bard, 
    Bing,
    You,
    H2o,
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
        AiAsk, Aichat, ChatgptAi, FreeGpt, GptGo, GeekGpt,
        Phind, You
    ])
)

# GPT-3.5 too, but all providers supports long responses and a custom timeouts
gpt_35_long = Model(
    name          = 'gpt-3.5-turbo',
    base_provider = 'openai',
    best_provider = RetryProvider([
        AiAsk, Aichat, FreeGpt, You,
        GptChatly, GptForLove,
        NoowAi, GeekGpt, Phind,
        FakeGpt
    ])
)

# H2o
copilot = Model(
    name          = "copilot",
    base_provider = 'perplexity',
    best_provider = PerplexityAI)
concise = Model(
    name          = "concise",
    base_provider = 'perplexity',
    best_provider = PerplexityAI)

seallm = Model(
    name          = "seallm",
    base_provider = 'seallm',
    best_provider = SeaLLM
)
perplexity_llama2_70b = Model(
    name          = "llama-2-70b-chat",
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
    best_provider=RetryProvider([
        ChatgptX, GptGo, You, 
        NoowAi, GPTalk, GptForLove, Phind, ChatBase
    ])
)

gpt_4 = Model(
    name          = 'gpt-4',
    base_provider = 'openai',
    best_provider = RetryProvider([
        Bing, GeekGpt, Phind
    ])
)

llama2_7b = Model(
    name          = "meta-llama/Llama-2-7b-chat-hf",
    base_provider = 'huggingface',
    best_provider = RetryProvider([Llama2, DeepInfra]))

llama2_13b = Model(
    name          ="meta-llama/Llama-2-13b-chat-hf",
    base_provider = 'huggingface',
    best_provider = RetryProvider([Llama2, DeepInfra]))

llama2_70b = Model(
    name          = "meta-llama/Llama-2-70b-chat-hf",
    base_provider = "huggingface",
    best_provider = RetryProvider([Llama2, DeepInfra]))

# Bard
palm = Model(
    name          = 'palm',
    base_provider = 'google',
    best_provider = Bard)

# H2o
falcon_7b = Model(
    name          = 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
    base_provider = 'huggingface',
    best_provider = H2o)

falcon_40b = Model(
    name          = 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
    base_provider = 'huggingface',
    best_provider = H2o)

llama_13b = Model(
    name          = 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b',
    base_provider = 'huggingface',
    best_provider = H2o)

# Vercel
claude_instant_v1 = Model(
    name          = 'claude-instant-v1',
    base_provider = 'anthropic',
    best_provider = Vercel)

claude_v1 = Model(
    name          = 'claude-v1',
    base_provider = 'anthropic',
    best_provider = Vercel)

claude_v2 = Model(
    name          = 'claude-v2',
    base_provider = 'anthropic',
    best_provider = Vercel)

command_light_nightly = Model(
    name          = 'command-light-nightly',
    base_provider = 'cohere',
    best_provider = Vercel)

command_nightly = Model(
    name          = 'command-nightly',
    base_provider = 'cohere',
    best_provider = Vercel)

gpt_neox_20b = Model(
    name          = 'EleutherAI/gpt-neox-20b',
    base_provider = 'huggingface',
    best_provider = Vercel)

oasst_sft_1_pythia_12b = Model(
    name          = 'OpenAssistant/oasst-sft-1-pythia-12b',
    base_provider = 'huggingface',
    best_provider = Vercel)

oasst_sft_4_pythia_12b_epoch_35 = Model(
    name          = 'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5',
    base_provider = 'huggingface',
    best_provider = Vercel)

santacoder = Model(
    name          = 'bigcode/santacoder',
    base_provider = 'huggingface',
    best_provider = Vercel)

bloom = Model(
    name          = 'bigscience/bloom',
    base_provider = 'huggingface',
    best_provider = Vercel)

flan_t5_xxl = Model(
    name          = 'google/flan-t5-xxl',
    base_provider = 'huggingface',
    best_provider = Vercel)

code_davinci_002 = Model(
    name          = 'code-davinci-002',
    base_provider = 'openai',
    best_provider = Vercel)

gpt_35_turbo_16k = Model(
    name          = 'gpt-3.5-turbo-16k',
    base_provider = 'openai',
    best_provider = gpt_35_long.best_provider)

gpt_35_turbo_16k_0613 = Model(
    name          = 'gpt-3.5-turbo-16k-0613',
    base_provider = 'openai',
    best_provider = gpt_35_long.best_provider
)

gpt_35_turbo_0613 = Model(
    name          = 'gpt-3.5-turbo-0613',
    base_provider = 'openai',
    best_provider = gpt_35_turbo.best_provider
)

gpt_4_0613 = Model(
    name          = 'gpt-4-0613',
    base_provider = 'openai',
    best_provider = gpt_4.best_provider
)

gpt_4_32k = Model(
    name          = 'gpt-4-32k',
    base_provider = 'openai',
    best_provider = gpt_4.best_provider
)

gpt_4_32k_0613 = Model(
    name          = 'gpt-4-32k-0613',
    base_provider = 'openai',
    best_provider = gpt_4.best_provider
)

text_ada_001 = Model(
    name          = 'text-ada-001',
    base_provider = 'openai',
    best_provider = Vercel)

text_babbage_001 = Model(
    name          = 'text-babbage-001',
    base_provider = 'openai',
    best_provider = Vercel)

text_curie_001 = Model(
    name          = 'text-curie-001',
    base_provider = 'openai',
    best_provider = Vercel)

text_davinci_002 = Model(
    name          = 'text-davinci-002',
    base_provider = 'openai',
    best_provider = Vercel)

text_davinci_003 = Model(
    name          = 'text-davinci-003',
    base_provider = 'openai',
    best_provider = Vercel)

llama13b_v2_chat = Model(
    name          = 'replicate:a16z-infra/llama13b-v2-chat',
    base_provider = 'replicate',
    best_provider = Vercel)

llama7b_v2_chat = Model(
    name          = 'replicate:a16z-infra/llama7b-v2-chat',
    base_provider = 'replicate',
    best_provider = Vercel)

llama70b_v2_chat = Model(
    # name          = 'replicate:replicate/llama-2-70b-chat',
    name          = 'replicate/llama70b-v2-chat',
    base_provider = 'replicate',
    best_provider = Vercel)


class ModelUtils:
    convert: dict[str, Model] = {
        'concise'    : concise,
        'copilot'    : copilot,
        # gpt-3.5
        'gpt-3.5-turbo'          : gpt_35_turbo,
        'gpt-3.5-turbo-0613'     : gpt_35_turbo_0613,
        'gpt-3.5-turbo-16k'      : gpt_35_turbo_16k,
        'gpt-3.5-turbo-16k-0613' : gpt_35_turbo_16k_0613,
        
        # gpt-4
        'gpt-4'          : gpt_4,
        'gpt-4-0613'     : gpt_4_0613,
        'gpt-4-32k'      : gpt_4_32k,
        'gpt-4-32k-0613' : gpt_4_32k_0613,

        # Llama 2
        'llama2-7b' : llama2_7b,
        'llama2-13b': llama2_13b,
        'llama2-70b': llama2_70b,
        
        # Bard
        'palm2'       : palm,
        'palm'        : palm,
        'google'      : palm,
        'google-bard' : palm,
        'google-palm' : palm,
        'bard'        : palm,
        
        # H2o
        'falcon-40b' : falcon_40b,
        'falcon-7b'  : falcon_7b,
        'llama-13b'  : llama_13b,
        
        # Vercel
        #'claude-instant-v1' : claude_instant_v1,
        #'claude-v1'         : claude_v1,
        #'claude-v2'         : claude_v2,
        'command-nightly'   : command_nightly,
        'gpt-neox-20b'      : gpt_neox_20b,
        'santacoder'        : santacoder,
        'bloom'             : bloom,
        'flan-t5-xxl'       : flan_t5_xxl,
        'code-davinci-002'  : code_davinci_002,
        'text-ada-001'      : text_ada_001,
        'text-babbage-001'  : text_babbage_001,
        'text-curie-001'    : text_curie_001,
        'text-davinci-002'  : text_davinci_002,
        'text-davinci-003'  : text_davinci_003,
        'llama70b-v2-chat'  : llama70b_v2_chat,
        'llama13b-v2-chat'  : llama13b_v2_chat,
        'llama7b-v2-chat'   : llama7b_v2_chat,
        
        'oasst-sft-1-pythia-12b'           : oasst_sft_1_pythia_12b,
        'oasst-sft-4-pythia-12b-epoch-3.5' : oasst_sft_4_pythia_12b_epoch_35,
        'command-light-nightly'            : command_light_nightly,
    }

_all_models = list(ModelUtils.convert.keys())