from gpt4free import Completion, Provider, forefront
# import forefront

token = forefront.Account.create(logging=False)
response = Completion.create(
    Provider.ForeFront, prompt='Write a poem on Lionel Messi', model='gpt-4', token=token
)
print(response)
print(f'END')