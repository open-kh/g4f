from gpt4free import Completion, Provider, forefront
# import forefront

response = Completion.create(Provider.You, prompt='Write a poem on Lionel Messi')
print(response)