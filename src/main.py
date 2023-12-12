from model import TS
from prompts import *
from request_handler import rawtext_from_url

LANGUAGE = "Spanish"

url = 'https://www.lifeder.com/identidad-personal/'
# url = 'https://www.cnn.com/2023/12/11/world/spacex-falcon-heavy-x37b-space-plane-scn/index.html'
rawtext = rawtext_from_url(url)

#user = f"{LANGUAGE}  beginner with good vocabulary, but poor understanding of sentence structure."
user = f"{LANGUAGE} beginner with good understanding of sentence structure, but poor vocabulary."

params = {
    'user': user,
    'group_len': 3,  # higher values require fewer tokens but may be less fine 
    'context_window_len': 1, # higher values give more context but require more tokens
    'model': 'gpt-3.5-turbo',  # use gpt-3.5 for testing; gpt-4 is expensive!
}

openai_params = {
    'temperature': 0,
    'max_tokens': 256,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}

lb,ub = (0, 3)

a=TS(rawtext, params)
a.simplify(lb, ub, openai_params)
# a.len_s_group_tokens_list

# the tool in action
file = open('output.txt', 'w')

file.write("----- Sample Output -----\n")
file.write(f"User: {params['user']}\n")
file.write(f"Model: {params['model']}\n")
file.write("----- Old -----\n")
file.write(a.text + "\n")
file.write("----- New -----\n")
file.write(a.s_text + "\n")

file.close()


