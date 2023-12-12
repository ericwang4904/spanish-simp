from model import TS
from prompts import *
from request_handler import rawtext_from_url


url = 'https://www.lifeder.com/identidad-personal/'
rawtext = rawtext_from_url(url)

#user = "Spanish beginner with good vocabulary, but poor understanding of sentence structure."
user = "Spanish beginner with good understanding of sentence structure, but poor vocabulary."

params = {
    'user': user,
    'group_len': 3,  # higher values require fewer tokens but may be less fine 
    'context_window_len': 1, # higher values give more context but require more tokens
    'model': 'gpt-4-1106-preview',
}

openai_params = {
    'temperature': 0,
    'max_tokens': 256,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}

a=TS(rawtext, params)
a.simplify(0, 3, openai_params)
# a.len_s_group_tokens_list

# the tool in action
file = open('output.txt', 'w')

file.write("----- Sample Output -----\n")
file.write(f"User: {params['user']}\n")
file.write(f"Model: {params['model']}\n")
file.write("----- Old -----\n")
file.write(a.old_s_text + "\n")
file.write("----- New -----\n")
file.write(a.s_text + "\n")

file.close()


