import os
import time
import json
import random

from g4f import Model, ModelUtils, ChatCompletion, Provider
from flask import Flask, request, Response
from flask_cors import CORS
from keypair.encryption import encrypt, decrypt, public_key, plaintext

# print('public_key', public_key)

public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"
plaintext = "Hello, World!"

# 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
# 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

# encoded_ciphertext = encrypt(public_key, plaintext)
# print("Encoded Ciphertext:", encoded_ciphertext)

app = Flask(__name__)
CORS(app)

@app.route("/chat/completions", methods=['POST'])
def chat_completions():
    streaming = request.json.get('stream', False)
    model = request.json.get('model', 'falcon-40b')
    messages = request.json.get('messages')
    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    SetModel = ModelUtils.convert[model]

    models = {
        'gpt-4': 'gpt-4',
        'gpt-4-0613': 'gpt-4-0613',
        'gpt-3.5-turbo-16k': 'GPT-3.5-16k',
        'gpt-3.5-turbo': 'gpt-3.5-turbo-0301',
        'gpt-3.5-turbo-0613': 'gpt-3.5-turbo-0613',
        'falcon-7b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
        'falcon-40b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'llama-13b': 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b'
    }

    # print("original string: ", message)
    # print("encrypted string: ", encMessage)
    # decMessage = fernet.decrypt(encMessage).decode()
 
    # print("decrypted string: ", decMessage)

    # https://liaobots.work/en?ic=TR0NX9 // get code
    # https://liaobots.work/_next/data/4nxMC017cSo0fRuOmTTYj/en.json?ic=TR0NX9
    
    # https://liaobots.work?ic=MGJ7P8
    # https://liaobots.work?ic=1YN4MT
    # https://liaobots.work?ic=Z8WQYS
    authkey = ['Co23kV7sPU45t', '7pZ9moAGkqR2i', 'RXsIxyJc6hGsA','4fDGzgKsEEW1q','tIUtcIhFwXZQv', 'DD3H9jy9gtf0L','iW6fkRHUGV8tm']

    # setTimeout(() => {
    #     $.post("/recaptcha/api/login", {token: 'abcdefghijklmnopqrst'}, res => {
    #         if (res.code != 200) {
    #             layer.msg(res.msg);
    #             return;
    #         }
    #         window.location.reload();
    #     });
    # }, 1300);
    response = ChatCompletion.create(model=SetModel.name, provider=Provider.Forefront, stream=streaming,
                                     messages=messages, auth=authkey[random.randint(0,len(authkey)-1)])
    # response = ChatCompletion.create(model="gpt-4", provider=Provider.Bing, stream=streaming,
    #                                  messages=messages)

    if not streaming:
        while 'curl_cffi.requests.errors.RequestsError' in response:
            response = ChatCompletion.create(model=SetModel.name, provider=Provider.Forefront, stream=streaming,
                                             messages=messages)

        completion_timestamp = int(time.time())
        completion_id = ''.join(random.choices(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

        return {
            'id': 'chatcmpl-%s' % completion_id,
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': models[model],
            'usage': {
                'prompt_tokens': None,
                'completion_tokens': None,
                'total_tokens': None
            },
            'choices': [{
                'message': {
                    'role': 'assistant',
                    'content': response
                },
                'finish_reason': 'stop',
                'index': 0
            }]
        }

    def stream():
        for token in response:
            completion_timestamp = int(time.time())
            completion_id = ''.join(random.choices(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

            completion_data = {
                'id': f'chatcmpl-{completion_id}',
                'object': 'chat.completion.chunk',
                'created': completion_timestamp,
                'model': 'gpt-3.5-turbo-0301',
                'choices': [
                    {
                        'delta': {
                            'content': token
                        },
                        'index': 0,
                        'finish_reason': None
                    }
                ]
            }

            yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
            time.sleep(0.1)

    return app.response_class(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 1337,
        'debug': True
    }

    app.run(**config)
