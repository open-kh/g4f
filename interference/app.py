import os
import json
import time
import random
import string
from tokenize import String
from urllib.request import urlretrieve

from flask        import Flask, request, Response, send_file
from flask_cors   import CORS
from g4f          import ChatCompletion, models
from g4f.Provider import (
    Bard,
    PerplexityAI,
    Phind,
    Bing,
    HuggingChat,
    Llama2,
    StabilityAI,
)

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN="r8_clGIfdHF8p7zDWF3LBz1Ri8WQT7xNBU2BqAb2"
os.environ["REPLICATE_API_TOKEN"]=REPLICATE_API_TOKEN
public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"

class ResModel:
    def __init__(self,completion_id,model,chunk) -> None:
        self.model = model if model is String else "default"
        self.completion_id = completion_id
        self.chunk = chunk

    def to_dict(self):
        finish = None
        if self.chunk is True:
            finish = 'stop'
            self.chunk = {}
        else:
            self.chunk = {'content': self.chunk}
        return {
            'id': f'chatcmpl-{self.completion_id}',
            'object': 'chat.completion.chunk',
            'created': int(time.time()),
            'model': self.model,
            'choices': [
                {
                    'index': 0,
                    'delta': self.chunk,
                    'finish_reason': finish,
                }
            ],
        }

@app.route('/chat/completions', methods=['POST'])
def chat_completions():
    # model    = request.get_json().get('model', 'gpt-3.5-turbo')
    model    = request.get_json().get('model', 'gpt-4')
    stream   = request.get_json().get('stream', False)
    messages = request.get_json().get('messages')

    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    myauth = None
    cookies = None

    if model == 'bing':
        model = 'gpt-4'
        provider = Phind
    elif model == 'bard':
        provider = Bard
        stream = False
    elif model == 'openai':
        model = 'gpt-3.5-turbo-16k'
        provider = Phind

    elif model == 'perplexity':
        model = "concise"
        provider = PerplexityAI

    elif model == 'meta':
        provider = HuggingChat
        path_file = "./cookie.json"
        with open(path_file, "r",encoding='utf-8') as f:
            cookies = json.load(f)
        model = models.default

        myauth = '&#39'
    else:
        provider = None
        model = models.default

    
    response = ChatCompletion.create(
        model = model,
        provider = provider,
        stream = stream, 
        messages = messages,
        auth = myauth,
        cookies = cookies
    )

    completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))
    completion_timestamp = int(time.time())

    if not stream:
        if model == 'bard':
            return response
        return {
            'id': f'chatcmpl-{completion_id}',
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': model,
            'choices': [
                {
                    'index': 0,
                    'message': {
                        'role': 'assistant',
                        'content': response,
                    },
                    'finish_reason': 'stop',
                }
            ],
            'usage': {
                'prompt_tokens': None,
                'completion_tokens': None,
                'total_tokens': None,
            },
        }

    def streaming():
        for chunk in response:
            mydict = ResModel(completion_id, model,chunk)
            content = json.dumps(mydict.to_dict(), separators=(',', ':'))
            yield f'data: {content}\n\n'
            time.sleep(0.1)

        mydict = ResModel(completion_id, model,True)
        content = json.dumps(mydict.to_dict(), separators=(',', ':'))
        yield f'data: {content}\n\n'

    return app.response_class(streaming(), mimetype='text/event-stream')

@app.route("/chat/image_generation", methods=['POST'])
def image_generate_temp():
    ai = StabilityAI()
    text = request.json.get('text')
    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    out = ai.image_generate(prompt=f"{text}, cinematic, dramatic")
    images = []
    for img in out['images']:
        imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
        imgName = f"txt2img_{imgID}.png"
        urlImg = f"https://{request.host}/images/{imgName}"
        urlretrieve(img, f"./out/{imgName}")
        # size = "{height=270px width=270px}" 
        # if len(out['images'])>=2 else ""
        images.append(f"[![{out['prompt']}]({urlImg})]({urlImg})")

    token = "\n".join(images)

    completion_data = f"Sure, Here is the image:\n{token}\nDid you like it?"

    return Response(completion_data, content_type='application/json')


@app.route('/images/<path:path>',methods=['GET'])
def send_static_file(path):
    return send_file(f"/out/{path}")

def main():
    app.run(host='0.0.0.0', port=1337, debug=True)

if __name__ == '__main__':
    main()