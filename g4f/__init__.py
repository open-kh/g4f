import sys
from .typing import MetaModels, Union
from . import Provider

class Model(metaclass=MetaModels):
    
    class model:
        name: str
        base_provider: str
        best_site: str
    
    class gpt_35_turbo:
        name: str = 'gpt-3.5-turbo'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Forefront

    class gpt_4:
        name: str = 'gpt-4'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Bing,
    
    class claude_instant_v1_100k:
        name: str = 'claude-instant-v1-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Vercel

    class claude_instant_v1:
        name: str = 'claude-instant-v1'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Vercel

    class claude_v1_100k:
        name: str = 'claude-v1-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Vercel

    class claude_v1:
        name: str = 'claude-v1'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Vercel

    class alpaca_7b:
        name: str = 'alpaca-7b'
        base_provider: str = 'replicate'
        best_provider: Provider.Provider = Provider.Vercel

    class stablelm_tuned_alpha_7b:
        name: str = 'stablelm-tuned-alpha-7b'
        base_provider: str = 'replicate'
        best_provider: Provider.Provider = Provider.Vercel

    class bloom:
        name: str = 'bloom'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class bloomz:
        name: str = 'bloomz'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class flan_t5_xxl:
        name: str = 'flan-t5-xxl'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class flan_ul2:
        name: str = 'flan-ul2'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class gpt_neox_20b:
        name: str = 'gpt-neox-20b'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class oasst_sft_4_pythia_12b_epoch_35:
        name: str = 'oasst-sft-4-pythia-12b-epoch-3.5'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class santacoder:
        name: str = 'santacoder'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.Vercel

    class command_medium_nightly:
        name: str = 'command-medium-nightly'
        base_provider: str = 'cohere'
        best_provider: Provider.Provider = Provider.Vercel

    class command_xlarge_nightly:
        name: str = 'command-xlarge-nightly'
        base_provider: str = 'cohere'
        best_provider: Provider.Provider = Provider.Vercel

    class code_cushman_001:
        name: str = 'code-cushman-001'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class code_davinci_002:
        name: str = 'code-davinci-002'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class text_ada_001:
        name: str = 'text-ada-001'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class text_babbage_001:
        name: str = 'text-babbage-001'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class text_curie_001:
        name: str = 'text-curie-001'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class text_davinci_002:
        name: str = 'text-davinci-002'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel

    class text_davinci_003:
        name: str = 'text-davinci-003'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Vercel
        
    class palm:
        name: str = 'palm'
        base_provider: str = 'google'
        best_provider: Provider.Provider = Provider.Bard
        
    class davinvi_003:
        name: str = 'davinvi-003'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Vercel
    class falcon_40b:
        name: str = 'falcon-40b'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.H2o
    
    class falcon_7b:
        name: str = 'falcon-7b'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.H2o
        
    class llama_13b:
        name: str = 'llama-13b'
        base_provider: str = 'huggingface'
        best_provider: Provider.Provider = Provider.H2o
        
class Utils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,
        'gpt-4': Model.gpt_4,
        'falcon-40b': Model.falcon_40b,
        'falcon-7b': Model.falcon_7b,
        'llama-13b': Model.llama_13b,
        'claude-instant-v1': Model.claude_instant_v1,
        'claude-v1': Model.claude_v1,
        'alpaca-7b': Model.alpaca_7b,
    }

class ChatCompletion:
    @staticmethod
    def create(model: Model.model or str, messages: list, provider: Provider.Provider = None, stream: bool = False, **kwargs):
        try:
            if isinstance(model, str):
                model = Utils.convert[model]
            
            engine = model.best_site if not provider else provider
            if not engine.supports_stream and stream == True:
                print(
                    f"ValueError: {engine.__name__} does not support 'stream' argument", file=sys.stderr)
                sys.exit(1)
            
            return (engine._create_completion(model.name, messages, stream, **kwargs)
                    if stream else ''.join(engine._create_completion(model.name, messages, stream, **kwargs)))

        except TypeError as e:
            print(e)
            arg: str = str(e).split("'")[1]
            print(
                f"ValueError: {engine.__name__} does not support '{arg}' argument", file=sys.stderr)
            sys.exit(1)
