from flask import Flask
import asyncio

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    loop = asyncio.get_event_loop()
    result = loop.run_in_executor(None, looping())
    return result


def looping():
    for i in range(2000):
        print(i)

if __name__ == '__main__':
    app.run()