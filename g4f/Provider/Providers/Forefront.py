import os
import json
import requests
from ...typing import sha256, Dict, get_type_hints

url = 'https://chat.forefront.ai'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    json_data = {
        'text': messages[-1]['content'],
        "action": "continue",
        "id": "b6ff0fe1-fce5-42ce-9351-8f464ff0faa7",
        "parentId": "98865671-2ef3-43ad-b532-0f93e81536ef",
        "workspaceId": "98865671-2ef3-43ad-b532-0f93e81536ef",
        "messagePersona": "default",
        "model": "gpt-4",
        # "model": "gpt-3.5-turbo",
        'messages': messages[:-1] if len(messages) > 1 else [],
        'internetMode': 'never',
        "hidden": True
    }
    SIGN="28c3b1cc9f29f581b377206e9a9c7e6b261cf325909e8e4c6552089a986043f8a679d49f2d0beb88b80f670a6aa55ef0510a3a23cd6f31ef41f3e7b5dee497ac"
    AKEY="eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yTzZ3UTFYd3dxVFdXUWUyQ1VYZHZ2bnNaY2UiLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL2NoYXQuZm9yZWZyb250LmFpIiwiZXhwIjoxNjg4NjEyNzMyLCJpYXQiOjE2ODg2MTI2NzIsImlzcyI6Imh0dHBzOi8vY2xlcmsuZm9yZWZyb250LmFpIiwibmJmIjoxNjg4NjEyNjYyLCJzaWQiOiJzZXNzXzJTQkZhSk5iTEZOWnlMc1ZhMWZ2V3lBNG43NiIsInN1YiI6InVzZXJfMlNCRmFHRmpISVRYOWNJMFRkY1h2ZFI4Q0pzIn0.fOiOZt74hyHakSQcp3k6Lu2dMpocRVz6kROgMPrHZMf4rpU1sOdgXx7RKOx_BjWP_JUsi7tX4t8MyP0S09t8QDvni87ojKHO9mSzb8-n0deJ5Ig4alG98JWjs78fCpP190RjR1CtVIlJDAEX0fLb4q4wHqNLN0O0jxNn6_zeE5Bnov5-scqK3aD4JcdJcDBzW1lF86C88saGwrqSAJuZDaCww8rr563So3wK4qFzigA03CJZEqhQR1FbtYYTAGz25KbK78Dgw7yW0ATJjhMKNEDw9WVUaoQbsXKOga0900yVOq7HQ9-pJrj7FVEELPetaa4_FD8eH1cfYqrYXyNBTw"
    response = requests.post('https://streaming-worker.forefront.workers.dev/chat',
        json=json_data, stream=True, headers={
            "Contenct-Type": "application/json",
            "Access-Control-Request-Headers": "Origin, X-Requested-With, Content-Type, Accept",
            "Origin": "https://chat.forefront.ai",
            "Referer": "https://chat.forefront.ai",
            "Cf-Ray": "7e249ef658ce3e65-SIN",
            "Authorization": f"Bearer {AKEY}",
            "X-Signature": f"{SIGN}"
        })
    for token in response.iter_lines(): 
        if b'delta' in token:
            token = json.loads(token.decode().split('data: ')[1])['delta']
            yield (token)
            
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])