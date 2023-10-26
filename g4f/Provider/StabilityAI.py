import requests
import random
import os
import json

sdxl_version=[
    # "2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
    "c221b2b8ef527988fb59bf24a8b97c4561f1c671f73bd389f866bfb27c061316"
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
                # 'Accept': '*/*',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://replicate.com/stability-ai/sdxl',
                'Content-Type': 'application/json',
                'Origin': 'https://replicate.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'TE': 'trailers'
            }
        self.ver = random.choice(sdxl_version)
        

    def image_generate(self, prompt, count=1,lora_scale=0.6, width=1024, height=1024, refine="expert_ensemble_refiner", scheduler="K_EULER", guidance_scale=7.5, high_noise_frac=0.8, prompt_strength=0.8, num_inference_steps=25):
        try:
            self.ver = random.choice(sdxl_version)
            url = "https://replicate.com/api/predictions"
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
            response.raise_for_status()

            json_response = response.json()
            uuid = json_response['id']
            image_url = self.get_image_url(uuid,prompt)

            return image_url

        except ValueError as e:
            print(f"Error: {e}")
            return None

    def get_image_url(self, uuid,prompt):
        url = f"https://replicate.com/api/predictions/{uuid}"
        response = requests.request("GET", url, headers=self.headers, timeout=1000).json()
        if response['status'] == "succeeded":
            output = {"prompt":prompt,"images":response['output']}
            return output
        else:
            return self.get_image_url(uuid,prompt)