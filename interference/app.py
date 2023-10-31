import json
import time
import random
import string
from tokenize import String
import requests

from typing       import Any
from flask        import Flask, request, Response
from flask_cors   import CORS
from transformers import AutoTokenizer
from g4f          import ChatCompletion, models, Provider
from g4f.Provider import (
    Bard,
    Perplexity,
    Phind,
    Bing,
    Liaobots,
    HuggingChat,
    OpenAssistant,
    OpenaiChat,
    Vercel,
    Llama2,
    ChatgptAi,
    You,
    Yqcloud,
    MyShell,
    Hashnode
)
from g4f.Provider.helper import get_cookies
from g4f.Provider.Bing import (create_context)
# from g4f import (Provider)

app = Flask(__name__)
CORS(app)

public_key = "pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"

class ResModel:
    def __init__(self,completion_id,model,chunk) -> None:
        self.model = model if model is String else "default"
        self.completion_id = completion_id
        self.chunk = chunk

    def to_dict(self):
        return {
            'id': f'chatcmpl-{self.completion_id}',
            'object': 'chat.completion.chunk',
            'created': int(time.time()),
            'model': self.model,
            'choices': [
                {
                    'index': 0,
                    'delta': {
                        'content': self.chunk,
                    },
                    'finish_reason': None,
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

    check = True
    perplexity = False
    myauth = False
    if model == 'bing':
        model = 'gpt-4'
        provider = Bing
    elif model == 'bard':
        provider = Bard
        stream = False
        check = False
    elif model == 'openai':
        model = 'gpt-3.5-turbo-16k'
        provider = Bing

    elif model == 'perplixity':
        perplexity = True

    elif model == 'meta':
        provider = HuggingChat
        # model = "tiiuae/falcon-180B-chat"
        # model = "meta-llama/Llama-2-70b-chat-hf"
        model = models.default
        myauth = True
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
    
    # print(model)

    if perplexity:
        perplixAI = Perplexity()
        response = perplixAI.search(create_context(messages))
    else:
        response = ChatCompletion.create(
            model = model,
            provider=provider,
            stream = stream, 
            messages = messages,
            auth=myauth,
            cookies= cookies
        )
    # if check:
    # else:
    #     response = ChatCompletion.create(
    #         model = model,
    #         provider=provider,
    #         stream = stream, 
    #         messages = messages, 
    #         auth=True,
    #     )

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

        end_completion_data: dict[str, Any] = {
            'id': f'chatcmpl-{completion_id}',
            'object': 'chat.completion.chunk',
            'created': completion_timestamp,
            'model': model,
            'choices': [
                {
                    'index': 0,
                    'delta': {},
                    'finish_reason': 'stop',
                }
            ],
        }
        content = json.dumps(end_completion_data, separators=(',', ':'))
        yield f'data: {content}\n\n'

    return app.response_class(streaming(), mimetype='text/event-stream')


# Get the embedding from huggingface
def get_embedding(input_text, token):
    huggingface_token = token
    embedding_model = 'sentence-transformers/all-mpnet-base-v2'
    max_token_length = 500

    # Load the tokenizer for the 'all-mpnet-base-v2' model
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)
    # Tokenize the text and split the tokens into chunks of 500 tokens each
    tokens = tokenizer.tokenize(input_text)
    token_chunks = [tokens[i:i + max_token_length]
                    for i in range(0, len(tokens), max_token_length)]

    # Initialize an empty list
    embeddings = []

    # Create embeddings for each chunk
    for chunk in token_chunks:
        # Convert the chunk tokens back to text
        chunk_text = tokenizer.convert_tokens_to_string(chunk)

        # Use the Hugging Face API to get embeddings for the chunk
        api_url = f'https://api-inference.huggingface.co/pipeline/feature-extraction/{embedding_model}'
        headers = {'Authorization': f'Bearer {huggingface_token}'}
        chunk_text = chunk_text.replace('\n', ' ')

        # Make a POST request to get the chunk's embedding
        response = requests.post(api_url, headers=headers, json={
                                 'inputs': chunk_text, 'options': {'wait_for_model': True}})

        # Parse the response and extract the embedding
        chunk_embedding = response.json()
        # Append the embedding to the list
        embeddings.append(chunk_embedding)

    # averaging all the embeddings
    # this isn't very effective
    # someone a better idea?
    num_embeddings = len(embeddings)
    average_embedding = [sum(x) / num_embeddings for x in zip(*embeddings)]
    embedding = average_embedding
    return embedding


@app.route('/embeddings', methods=['POST'])
def embeddings():
    input_text_list = request.get_json().get('input')
    input_text      = ' '.join(map(str, input_text_list))
    token           = request.headers.get('Authorization').replace('Bearer ', '')
    embedding       = get_embedding(input_text, token)
    
    return {
        'data': [
            {
                'embedding': embedding,
                'index': 0,
                'object': 'embedding'
            }
        ],
        'model': 'text-embedding-ada-002',
        'object': 'list',
        'usage': {
            'prompt_tokens': None,
            'total_tokens': None
        }
    }

def main():
    app.run(host='0.0.0.0', port=1337, debug=True)

if __name__ == '__main__':
    main()