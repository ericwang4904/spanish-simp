import regex as re

from openai import OpenAI
from nltk import sent_tokenize, word_tokenize
from string import punctuation as PUNCT
from typing import *


from prompts import *
from config import *

class LS:
    def __init__(self, user: str, text: str, language: str = 'Spanish') -> None:
        self.user = user
        self.text = text
        self.language = language

        self._tokenize()

        self.client = OpenAI(api_key=API_KEY)
    
    def _tokenize(self):
        self.sentences = sent_tokenize(self.text, language=self.language)
        self.tokens = []

        for t in self.sentences:
            ft = re.sub(f'[{PUNCT}]', '', t)  # removes ascii punctuation
            self.tokens.append(word_tokenize(ft))
    
    def cwi(self, lower_bound: int, upper_bound: int) -> Dict[str, any]:
        '''
        :param lower_bound: lower index for slice of sentences to cwi
        :param upper_bound: upper index (not included) for slice of sentences to cwi
        :return: Dictionary of lb, ub, and raw outputs where self.sentences[i] corresponds to output[i]
        '''

        completion = []
        for context in self.sentences[lower_bound: upper_bound]:
            query = self.cwi_query(context)
            response = self.client.chat.completions.create(**query)
            completion.append(
                response.choices[0].message.content
                )
        
        output = {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'completion': completion,
        }
        
        return output
            
    def cwi_query(self, context) -> Dict:

        cw = context_window()['cwi']

        # most of these below variables can be tuned, either globally or on a context specific basis
        temperature = 0
        max_tokens = 256
        frequency_penalty = 0
        presence_penalty = 0
        prompt = return_cwi(self.user, context, language=self.language)['zero_shot']  # this can be changed in later revisions

        query = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': cw},
                {'role': 'user', 'content': prompt}
            ],
            'stream': False,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'frequency_penalty': frequency_penalty,
            'presence_penalty' : presence_penalty,
        }

        return query
    
