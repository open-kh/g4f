import json
import time
import random
import string
from tokenize import String

from flask        import Flask, request, Response
from flask_cors   import CORS
from g4f          import ChatCompletion, models, Provider
from g4f.Provider import (
    Bard,
    PerplexityAI,
    Phind,
    Bing,
    HuggingChat,
    Llama2,
)
from g4f.Provider.helper import get_cookies

app = Flask(__name__)
CORS(app)

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
        # model = "tiiuae/falcon-180B-chat"
        # model = "meta-llama/Llama-2-70b-chat-hf"
        model = models.default
        myauth = '&#39'
    else:
        provider = None
        model = models.default

    path_file = "./cookie.json"
    with open(path_file, "r",encoding='utf-8') as f:
        cookies = json.load(f)

    if not cookies:
        cookies = get_cookies(".huggingface.co")
        with open(path_file, "w",encoding='utf-8') as f:
            json.dump(cookies,f)
    
    response = ChatCompletion.create(
        model = model,
        provider=provider,
        stream = stream, 
        messages = messages,
        auth=myauth,
        cookies= cookies
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

def main():
    app.run(host='0.0.0.0', port=1337, debug=True)

if __name__ == '__main__':
    main()