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

gpt_access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJwaGVhcnVtLm5vcC5raEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci01THExYnRhRHp2N2w4Y0xJYnJDUXV5T04ifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDY1MDcyYWFmNjEwNmZkN2E3MmU5MDk0MCIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVu…VueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.tINb6O2Ny9B4_6QrC0f0orfXhSQnlejrapyROHjwQ4AvWt3V0m3XQRVNJIeMfcsT61mQj8jkwdiIuBqqvBG6LJ7lgBVzf6ZSsyvzSxPDiGGUOHeH2LhkouT9bjfEsURBZyf7BOLadn12eVPechzp3e4-wj07Gt3s8ZH6bnzUHi5yGIvEmv9fOr6ZnpJ3GJfrxMf-4EaSgSmc8xOzRChb6fRgfXHq551niLlAtUrlgK0rMOr-kyOZLO2aSCToFGSpD8Eq__bsMgFkaiAfmCHtSHZpcJHSDZynS0CUw_I9cduOMKkU-Sx8u8w7p8ORShGrtdu23kBD5nIV_SuoxrRuJw"

# print("Bing: ", end="")
for response in log_time_yield(
    g4f.ChatCompletion.create,
    model=g4f.models.default,
    messages=[{
            "role": "system",
            "content": "You are Open Brain"
        },{"role": "user", "content": _instruct}],
    # provider=g4f.Provider.Bard,
    provider=g4f.Provider.OpenaiChat,
    access_token=gpt_access_token,
    # provider=g4f.Provider.HuggingChat,
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