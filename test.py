from gpt4free import gptworldAi,you, usesless, theb,forefront, deepai, aiassist, aicolors, hpgptai, italygpt2, quora

from gpt4free.quora import Poe

# token = quora.Account.create(logging=True, enable_bot_creation=True)

# model = quora.Model.create(
#     token=token,
#     model='gpt-3.5-turbo',  # or claude-instant-v1.0
#     system_prompt='you are ChatGPT a large language model ...'
# )

message = []
while True:
    prompt = input("请输入问题：")
    message.append({"role": "user","content": prompt})
    text = ""
    for chunk in gptworldAi.ChatCompletion.create(message,'127.0.0.1:7890'):
        text = text+chunk
        print(chunk, end="", flush=True)
        print()
        message.append({"role": "assistant", "content": text})