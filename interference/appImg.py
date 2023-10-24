import os
import random

from flask import Flask, request, Response, send_file
from flask_cors import CORS
from urllib.request import urlretrieve

from g4f.Provider import (
    StabilityAI
)

ai = StabilityAI()


app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN="r8_clGIfdHF8p7zDWF3LBz1Ri8WQT7xNBU2BqAb2"
os.environ["REPLICATE_API_TOKEN"]=REPLICATE_API_TOKEN
public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"


@app.route("/chat/image_generation", methods=['POST'])
def image_generate_temp():
    text = request.json.get('text')
    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)

    out = ai.image_generate(prompt=f"{text}")
    images = []
    for img in out['images']:
        imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
        imgName = f"txt2img_{imgID}.png"
        urlImg = f"http://{request.host}/images/{imgName}"
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

if __name__ == '__main__':
    config = {
        'host': '0.0.0.0',
        'port': 1333,
        'debug': True
    }

    app.run(**config)
