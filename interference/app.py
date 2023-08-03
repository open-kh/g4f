import os
import sys
import time
import json
import random
import base64
import requests

from g4f import Model, ChatCompletion, Provider, Utils
from flask import Flask, request, Response, send_file
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

    model_base = Utils.convert[model]
    # prompt = "You are Open Brain, a large language model trained by OpenAI using gpt-4-32k. Follow the user's instructions carefully. Respond using markdown."
    # for message in config['messages']:
    #     prompt += '%s: %s\n' % (message['role'], message['content'])

    # Provider selection

    if model == 'gpt-4':
        provider=Provider.Phind
    else:
        model_base = Utils.convert['falcon-40b']
        provider=Provider.H2o

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
        'llama-13b': 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b',
        # 'claude-instant-v1': 'anthropic:claude-instant-v1',
        # 'claude-v1': 'anthropic:claude-v1',
        # 'alpaca-7b': 'replicate:replicate/alpaca-7b',
    }

    # Getting the response
    response = ChatCompletion.create(model=model_base.name,
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
                'model': models[model_base.name],
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

API_KEY="sk-WTeLd6cpQJzWBwqrwDDWkZGwiyg4IQ0dUpReZc8v59Sd3N9l"
@app.route("/chat/image_generation", methods=['POST'])
def image_generation():
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-beta-v2-2-2/text-to-image"
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
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

    body = {
        "width": 512,
        "height": 512,
        "steps": 50,
        "seed": 0,
        "cfg_scale": 7,
        "samples": 1,
        "style_preset": "enhance",
        "text_prompts": [
            {
            "text": f"{text}",
            "weight": 1
            },
            {
            "text": "reduce noise",
            "weight": -1
            }
        ],
    }
    response = requests.post(url,headers=header,json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    token = ""
    for i, image in enumerate(data["artifacts"]):
        img64 = image["base64"]
        imgID = image["seed"]
        imgName = f"txt2img_{imgID}.png"
        with open(f"./out/{imgName}", "wb") as f:
            f.write(base64.b64decode(img64))
            urlImg = f"https://{request.host}/images/{imgName}"
            token+=f"[![Image Generator]({urlImg})]({urlImg})\n"

    completion_data = f"Sure, Here is the image:\n{token}Did you like it?"

    return Response(completion_data, content_type='application/json')

@app.route('/images/<path:path>',methods=['GET'])
def send_static_file(path):
    return send_file(f"../out/{path}")

if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 1337,
        'debug': True
    }

    app.run(**config)
