import os
import sys
import time
import json
import random
import requests

from g4f import Model, ChatCompletion, Provider, Utils
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"

@app.route("/chat/completions", methods=['POST'])
def chat_completions():
    streaming = request.json.get('stream', False)
    model = request.json.get('model', 'gpt-3.5-turbo')
    messages = request.json.get('messages')
    barer = request.headers.get('Authorization')
    
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    model = Utils.convert[model]
    # prompt = "You are Open Brain, a large language model trained by OpenAI using gpt-4-32k. Follow the user's instructions carefully. Respond using markdown."
    # for message in config['messages']:
    #     prompt += '%s: %s\n' % (message['role'], message['content'])

    # Provider selection
    provider=Provider.Phind

    # Streaming is not supported by these providers
    if provider in {Provider.Aws, Provider.Ora, Provider.Bard, Provider.Aichat}:
        streaming=False
    else:
        streaming=True

    models = {
        'gpt-4': 'gpt-4',
        'gpt-4-0613': 'gpt-4-0613',
        'claude_instant_v1_100k': 'claude_instant_v1_100k',
        'gpt-3.5-turbo': 'gpt-3.5-turbo-0301',
        'gpt-3.5-turbo-0613': 'gpt-3.5-turbo-0613',
        'falcon-7b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
        'falcon-40b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'llama-13b': 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b'
    }

    # Getting the response
    response = ChatCompletion.create(model='gpt-4'or model.name, 
                                        messages=messages, 
                                        stream=streaming, 
                                        provider=provider)
    # Printing the response
    def stream():
        for token in response:
            completion_timestamp = int(time.time())
            completion_id = ''.join(random.choices(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

            completion_data = {
                'id': f'chatcmpl-{completion_id}',
                'object': 'chat.completion.chunk',
                'created': completion_timestamp,
                'model': models[model.name],
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
            # sys.stdout.flush()

    return app.response_class(stream(), mimetype='text/event-stream')

bearer = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjFhZjI0ZTQ5LTFiMDUtNDBlMy1iMDU2LTFmM2FlYmViNzEyMCIsImlhdCI6MTY4OTQ5NjY3NCwiZXhwIjoxNjg5NzU1ODc0LCJhY3Rpb24iOiJhdXRoIiwiaXNzIjoidGhlYi5haSJ9.z5t72OxVK9xMxe8kC3huAqo6qPqkv92TG3SxqcGs0sg'

@app.route("/chat/image_generation", methods=['POST'])
def image_generation():
    url = "https://beta.theb.ai/api/image?org_id=496d24bf-2c9f-45a1-9d78-03213dca713b"
    header = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
        'Authorization': f"Bearer {bearer}",
    }
    text = request.json.get('text')
    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)
    # return text
    response = requests.post(url=url, headers=header, json={
        "text": text
    })
    token = response.json()
    completion_data = f"Sure, Here is the image:\n[![Image Generator]({token['data']['link']})]({token['data']['link']})\nDid you like it?"

    return Response(completion_data, content_type='application/json')


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 1337,
        'debug': True
    }

    app.run(**config)
