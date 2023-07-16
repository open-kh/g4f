import time
import json
import random

from g4f import ModelUtils, ChatCompletion, Provider
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat/completions", methods=['POST'])
def chat_completions():
    streaming = request.json.get('stream', False)
    model = request.json.get('model', 'gpt-3.5-turbo')
    messages = request.json.get('messages')
    SetModel = ModelUtils.convert[model]

    models = {
        'gpt-4': 'gpt-4',
        'gpt-4-0613': 'gpt-4-0613',
        'gpt-3.5-turbo-16k': 'gpt-3.5-turbo-16k',
        'gpt-3.5-turbo': 'gpt-3.5-turbo-0301',
        'gpt-3.5-turbo-0613': 'gpt-3.5-turbo-0613',
        'falcon-7b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-7b-v3',
        'falcon-40b': 'h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1',
        'llama-13b': 'h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-13b'
    }

    response = ChatCompletion.create(model=SetModel.name, provider=Provider.Theb, stream=streaming,
                                     messages=messages, auth="RXsIxyJc6hGsA")
    if not streaming:
        while 'curl_cffi.requests.errors.RequestsError' in response:
            response = ChatCompletion.create(model=SetModel.name, provider=Provider.Theb, stream=streaming,
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
            # if token is not "None":
            yield 'data: %s\n\n' % token
            # try:
            #     json_data = json.loads(token)
            #     yield 'data: %s\n\n' % json_data
            # except json.JSONDecodeError as e:
            #     print("Error: Invalid JSON format.")
            #     print("Details:", e)
                # data = json.loads(token)
            # completion_data = {
            #     'id': f'chatcmpl-{completion_id}',
            #     'object': 'chat.completion.chunk',
            #     'created': completion_timestamp,
            #     'model': 'gpt-3.5-turbo-0301',
            #     'choices': [
            #         {
            #             'delta': {
            #                 'content': token
            #             },
            #             'index': 0,
            #             'finish_reason': None
            #         }
            #     ]
            # }

            # yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
            time.sleep(0.1)

    return app.response_class(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 1337,
        'debug': True
    }

    app.run(**config)
