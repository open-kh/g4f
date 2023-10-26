import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent))

import g4f
from  testing.log_time import log_time, log_time_async, log_time_yield


_providers = [
    g4f.Provider.H2o,
    g4f.Provider.You,
    g4f.Provider.HuggingChat,
    g4f.Provider.OpenAssistant,
    g4f.Provider.Bing,
    g4f.Provider.Ails,
    g4f.Provider.Bard
]

_instruct = "Hello, are you GPT 4?."

_example = """
OpenaiChat: Hello! How can I assist you today? 2.0 secs
Bard: Hello! How can I help you today? 3.44 secs
Bing: Hello, this is Bing. How can I help? 😊 4.14 secs
Async Total: 4.25 secs

OpenaiChat: Hello! How can I assist you today? 1.85 secs
Bard: Hello! How can I help you today? 3.38 secs
Bing: Hello, this is Bing. How can I help? 😊 6.14 secs
Stream Total: 11.37 secs

OpenaiChat: Hello! How can I help you today? 3.28 secs
Bard: Hello there! How can I help you today? 3.58 secs
Bing: Hello! How can I help you today? 3.28 secs
No Stream Total: 10.14 secs
"""

gpt_access_token = '16117916cb06b62b8.7931458704|r=ap-southeast-1|meta=3|metabgclr=transparent|metaiconclr=%23757575|guitextcolor=%23000000|pk=3D86FBBA-9D22-402A-B512-3420086BA6CC|at=40|sup=1|rid=58|ag=101|cdn_url=https%3A%2F%2Ftcr9i.chat.openai.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-ap-southeast-1.arkoselabs.com|surl=https%3A%2F%2Ftcr9i.chat.openai.com|smurl=https%3A%2F%2Ftcr9i.chat.openai.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager'
# print("Bing: ", end="")
for response in log_time_yield(
    g4f.ChatCompletion.create,
    # model= g4f.models.default,
    model= g4f.models.llama70b_v2_chat,
    messages=[{
            "role": "system",
            "content": "You are Open Brain"
        },{"role": "user", "content": _instruct}],
    provider=g4f.Provider.Vercel,
    # access_token = gpt_access_token,
    # provider=g4f.Provider.Theb,
    # cookies=g4f.get_cookies(".huggingface.co"),
    stream=True,
    auth=True
):
    print(response, end="", flush=True)
print()
print()


# async def run_async():
#     responses = [
#         log_time_async(
#             provider.create_async, 
#             model=None,
#             messages=[{"role": "user", "content": _instruct}],
#         )
#         for provider in _providers
#     ]
#     responses = await asyncio.gather(*responses)
#     for idx, provider in enumerate(_providers):
#         print(f"{provider.__name__}:", responses[idx])
# print("Async Total:", asyncio.run(log_time_async(run_async)))
# print()


# def run_stream():
#     for provider in _providers:
#         print(f"{provider.__name__}: ", end="")
#         for response in log_time_yield(
#             provider.create_completion,
#             model=None,
#             messages=[{"role": "user", "content": _instruct}],
#         ):
#             print(response, end="", flush=True)
#         print()
# print("Stream Total:", log_time(run_stream))
# print()


# def create_no_stream():
#     for provider in _providers:
#         print(f"{provider.__name__}:", end=" ")
#         for response in log_time_yield(
#             provider.create_completion,
#             model=None,
#             messages=[{"role": "user", "content": _instruct}],
#             stream=False
#         ):
#             print(response, end="")
#         print()
# print("No Stream Total:", log_time(create_no_stream))
# print()