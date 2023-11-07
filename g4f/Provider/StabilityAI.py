from weakref import proxy
import requests
import random
import os
import json
import string

sdxl_version=[
    # "2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
    # "d830ba5dabf8090ec0db6c10fc862c6eb1c929e1a194a5411852d25fd954ac82"
    # "c221b2b8ef527988fb59bf24a8b97c4561f1c671f73bd389f866bfb27c061316",
    # "2a865c9a94c9992b6689365b75db2d678d5022505ed3f63a5f53929a31a46947",
    "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
]

user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Thunder Client (https://www.thunderclient.com)'
]

class StabilityAI:
    def __init__(self):
        self.headers = {
                'User-Agent': random.choice(user_agent),
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
                'Host': 'replicate.com',
                'Referer': 'https://replicate.com/stability-ai/sdxl',
                'Content-Type': 'application/json',
                'Origin': 'https://replicate.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'TE': 'trailers',
                'X-CSRFToken': self.generate_random_string(32)
            }
        self.ver = random.choice(sdxl_version)
    
    def _random_ip(self):
        return f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        

    def image_generate(self, prompt, count=1,lora_scale=0.6, width=1024, height=1024, refine="expert_ensemble_refiner", scheduler="K_EULER", guidance_scale=7.5, high_noise_frac=0.8, prompt_strength=0.8, num_inference_steps=25):
        try:
            proxies = ['https://openkh.org', 'https://api.openkh.org']
            self.ver = random.choice(sdxl_version)
            self.headers['User-Agent'] = random.choice(user_agent)
            random_ip = self._random_ip()
            self.headers['x-forwarded-for'] = random_ip
            url = 'https://replicate.com/api/predictions'
            payload = json.dumps({
                "version": self.ver,
                "input": {
                    "width": width,
                    "height": height,
                    "prompt": prompt,
                    "refine": refine,
                    "scheduler": scheduler,
                    "lora_scale": lora_scale,
                    "num_outputs": count,
                    "guidance_scale": guidance_scale,
                    "apply_watermark": False,
                    "high_noise_frac": high_noise_frac,
                    "negative_prompt": "",
                    "prompt_strength": prompt_strength,
                    "num_inference_steps": num_inference_steps
                },
                "is_training": False
            })
            response = requests.request("POST", url, headers=self.headers, data=payload, timeout=1000)
            print(json.dumps(response))
            response.raise_for_status()

            json_response = response.json()
            uuid = json_response['id']
            image_url = self.get_image_url(uuid,prompt)

            return image_url

        except ValueError as e:
            print(f"Error: {e}")
            return None
        
    def generate_random_string(self, length=32):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def get_image_url(self, uuid,prompt):
        url = f"https://replicate.com/api/predictions/{uuid}"
        response = requests.request("GET", url, headers=self.headers, timeout=1000).json()
        if response['status'] == "succeeded":
            output = {"prompt":prompt,"images":response['output']}
            return output
        else:
            return self.get_image_url(uuid,prompt)