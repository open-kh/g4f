
import random
from urllib.request import urlretrieve

# from sdxl import ImageGenerator
from g4f.Provider import (StabilityAI)

ai = StabilityAI()

question = "Kirigami illustration on delicate paper with slight wear: Intricate 3D pop-up of a traditional Japanese garden with koi pond and stone lanterns - Scenes of nature brought to life through precise cuts and folds - The art of cutting and folding paper to create sculptural designs."

out = ai.image_generate(prompt=f"{question}, cinematic, dramatic", count=2)
completion_data = "Sorry, I am running out off memory!"

imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
imgName = f"txt2img_{imgID}.png"
urlImg = f"https://localhost/images/{imgName}"

if out is not None and 'images' in out:
    images = out['images']
    image_tags = []
    for img in images:
        imgID = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
        imgName = f"txt2img_{imgID}.png"
        urlImg = f"https://localhost/images/{imgName}"
        urlretrieve(img, f"./out/{imgName}")
        image_tags.append(f'<a href="{urlImg}"><img src="{urlImg}" alt="Image Generate" style="width:100%"></a>')

    if len(image_tags) == 1:
        completion_data = f"Sure, Here is the image:\n{image_tags[0]}\nDid you like it?"
    else:
        image_tags_str = ''.join(f'<div>{tag}</div>' for tag in image_tags)
        grid_html = f'<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 5px;">{image_tags_str}</div>'
        completion_data = f"Sure, Here are the images:\n{grid_html}\nDid you like them?"

print(completion_data)