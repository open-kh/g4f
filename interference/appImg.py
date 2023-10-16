import io
import os
import sys
import time
import json
import random
import base64
import requests

from PIL import Image

from g4f import Model, ChatCompletion, Provider, Utils
from flask import Flask, request, Response, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"
API_KEY="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"

# MODEL_ID="stabilityai/stable-diffusion-xl-base-1.0"
# MODEL_ID="stabilityai/stable-diffusion-xl-base-0.9"
MODEL_ID="CompVis/stable-diffusion-v1-4"
header = {
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}",
}
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"


@app.route("/chat/image_generation", methods=['POST'])
def image_generation():
    text = request.json.get('text')
    barer = request.headers.get('Authorization')
    if barer is None:
        barer = 'unknown'
    else:
        barer = barer.strip().split(" ")[1] if len(barer.strip().split(" ")) > 1 else 'unknown'

    if barer != f"pk-{public_key}":
        return Response(response='Unauthorized', status=401)
    # return text

    payload = {
        "inputs": f"{text}",
    }
    response = requests.post(API_URL, headers=header, json=payload)
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
    imgName = f"txt2img_{imgID}.png"
    
    image.save(f"./out/{imgName}")
    # with open(f"./out/{imgName}", "wb") as f:
    #     f.write(image)
        
    urlImg = f"https://{request.host}/images/{imgName}"
    token = f"[![Image Generator]({urlImg})]({urlImg})\n"

    completion_data = f"Sure, Here is the image:\n{token}Did you like it?"

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
