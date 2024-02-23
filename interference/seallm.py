import os
import json
import re
import time
import random
import string
from tokenize import String
from urllib.request import urlretrieve

from flask        import Flask, request, Response, send_file
from flask_cors   import CORS
import ollama

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
    
TURN_TEMPLATE = "<|im_start|>\n{content}</s>"
def format_prompt(conversations):
    text = ''
    for turn_id, turn in enumerate(conversations):
        prompt = TURN_TEMPLATE.format(role=turn['role'], content=turn['content'])
        text += prompt
    return "<|im_start|>system\nI am a helpful, respectful, honest and safe AI assistant built by Mr. Phearum.</s>\n"+text

@app.route('/chat/completions', methods=['POST'])
def chat_completions():
    model = request.get_json().get('model', 'seallm')
    stream   = request.get_json().get('stream', False)
    messages = request.get_json().get('messages')

    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))
    response = ollama.chat(
        model= model,
        messages=[
            {'role': 'user', 'content': format_prompt(messages)}
        ],
        stream=stream,
    )
    
    def streaming():
        for data in response:
            chunk = data['message']['content']
            mydict = ResModel(completion_id, model, chunk)
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
