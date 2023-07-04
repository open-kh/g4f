from gpt4free import forefront, deepai


for chunk in deepai.Completion.create("Who are you?"):
    print(chunk, end="", flush=True)
    # yield chunk.decode()
print()