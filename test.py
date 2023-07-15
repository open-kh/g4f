from gpt4free import gptworldAi,you, usesless, theb,forefront, deepai, aiassist, aicolors, hpgptai, italygpt2, quora

from gpt4free.quora import Poe

# token = quora.Account.create(logging=True, enable_bot_creation=True)

# model = quora.Model.create(
#     token=token,
#     model='gpt-3.5-turbo',  # or claude-instant-v1.0
#     system_prompt='you are ChatGPT a large language model ...'
# )

while True:
    x = input("User: ")
    if x == "quit":
        break
    if x == "ai":
        print("AI: ", end="")
        for chunk in deepai.Completion.create(x):
            print(chunk, end="", flush=True)
        print()
        