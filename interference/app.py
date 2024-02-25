import os
import sys
import json
import time
import random
import string
import ollama
from tokenize import String
from urllib.request import urlretrieve

from flask        import Flask, request, Response, send_file
from flask_cors   import CORS
from g4f          import ChatCompletion, models
from g4f.Provider import (
    Ollama,
    PerplexityLabs,
    Phind,
    Bing,
    SeaLLM,
)
from g4f.Provider.helper import response_callback, seallm_format_prompt

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN="r8_clGIfdHF8p7zDWF3LBz1Ri8WQT7xNBU2BqAb2"
os.environ["REPLICATE_API_TOKEN"]=REPLICATE_API_TOKEN
public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"

    
@app.route('/chat/completions', methods=['POST']) # type: ignore
def chat_completions():
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
        provider = Bing
    
    elif model.startswith('ollama'):
        model = model.split('/')[1]
        provider = Ollama

    elif model == 'openai':
        model = 'gpt-3.5-turbo-16k'
        provider = Bing or Phind

    elif model == 'seallm':
        model = models.seallm
        provider = SeaLLM

    elif model == 'perplexity':
        model = models.perplexity_pplx_70b_online
        provider = PerplexityLabs

    elif model == 'meta':
        model = models.perplexity_pplx_70b
        provider = PerplexityLabs

    else:
        provider = None
        model = models.default

    completion_id = ''.join(random.choices(string.ascii_letters + string.digits, k=28))

    response = ChatCompletion.create(
        model = model,
        provider = provider,
        stream = stream, 
        messages = messages,
        auth = myauth,
        cookies = cookies
    )
    
    def _chat(chuck):
        if chuck['done'] is False:
            return chuck['response']
        else:
            return ''
    
    def streaming():
        for chunk in response:
            mydict = response_callback(completion_id, model, chunk)
            content = json.dumps(mydict.to_dict(), separators=(',', ':'))
            yield f'data: {content}\n\n'
            time.sleep(0.1)

        mydict = response_callback(completion_id, model,True)
        content = json.dumps(mydict.to_dict(), separators=(',', ':'))
        yield f'data: {content}\n\n'
    return app.response_class(streaming(), mimetype='text/event-stream')

@app.route("/chat/image_generation", methods=['POST'])
def image_generate_temp():
    ai = g4f.Provider.StabilityAI()
    barer = request.headers.get('Authorization')

    count = request.get_json().get('count', 1)
    if request.json is not None:
        text = request.get_json().get('text')
    else:
        return Response(response='Unknow request', status=404)

    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    out = ai.image_generate(prompt=f"{text}, cinematic, dramatic", count=(count if count <= 4 else 4))

    completion_data = "Sorry, I am running out off memory!"

    if out is not None and 'images' in out:
        images = out['images']
        image_tags = []
        for img in images:
            imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
            imgName = f"txt2img_{imgID}.png"
            urlImg = f"https://api.openkh.org/images/{imgName}"
            # urlImg = f"https://{request.host}/images/{imgName}"
            urlretrieve(img, f"./out/{imgName}")
            image_tags.append(f"[![Image generate]({urlImg})]({urlImg})")

        if len(image_tags) == 1:
            completion_data = f"Sure, Here is the image:\n{image_tags[0]}\nDid you like it? 😊"
        else:
            image_tags_str = "\n".join(image_tags)
            completion_data = f"Sure, Here are the images:\n{image_tags_str}\nDid you like them?"

    return Response(completion_data, content_type='application/json')


@app.route('/images/<path:path>',methods=['GET'])
def send_static_file(path):
    return send_file(f"/out/{path}")

def main(port:int=1337):
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    arguments = sys.argv[1:]
    for port in arguments:
        main(int(port))
