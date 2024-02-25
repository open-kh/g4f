from __future__       import annotations
from .Bing            import Bing
from .Phind           import Phind
from .Vercel          import Vercel
from .StabilityAI     import StabilityAI
from .ClaudeAI        import ClaudeAI
from .Llama2        import Llama2
from .PerplexityLabs    import PerplexityLabs
from .SeaLLM         import SeaLLM
from .Ollama         import Ollama

from .base_provider  import BaseProvider, AsyncProvider, AsyncGeneratorProvider
from .retry_provider import RetryProvider


class ProviderUtils:
    convert: dict[str, BaseProvider] = {
        'SeaLLM': SeaLLM,
        'Ollama': Ollama,
        'StabilityAI': StabilityAI,
        'PerplexityLabs': PerplexityLabs,
        'Llama2': Llama2,
        'Bing': Bing,
        'Phind': Phind,
        'Vercel': Vercel,
        
        'BaseProvider': BaseProvider,
        'AsyncProvider': AsyncProvider,
        'AsyncGeneratorProvider': AsyncGeneratorProvider,
        'RetryProvider': RetryProvider,
    } # type: ignore

__all__ = [
    'Ollama',
    'SeaLLM',
    'PerplexityLabs',
    'StabilityAI',
    'BaseProvider',
    'AsyncProvider',
    'AsyncGeneratorProvider',
    'RetryProvider',
    'Bing',
    'Llama2',
    'Phind',
    'Vercel',
]
