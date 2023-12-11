import regex as re

from openai import OpenAI
from nltk import sent_tokenize, word_tokenize
from string import punctuation as PUNCT
from typing import *

import logging as log
from prompts import *
from config import *

class TS:
    def __init__(self, text: str, params: dict) -> None:
        """
        Text Simplification Object. 
        :param text: text to be simplifed
        :param params: Other parameters for the object.
            user: description of user's linguistic capabilites
            group_len: number of sentences per token group. Defaults to 1.  
            context_window_size: the size of the window in the context for context_from_group (in # of tokens)
            model: name of openai model (e.g. gpt-3.5-turbo and gpt-4)
        """
        try: self.user = params['user']
        except KeyError: log.error("user not provided")
        self.group_len = params.get("group_len", 1)
        self.context_window_size = params.get("context_window_size", 1)
        self.openai_model = params.get("model", "gpt-3.5-turbo")


        self.text = text
        self.tokens, self.group_tokens = self.tokenize(self.text)

        # s_ : simplified language (used in simplification iteratively) 
        # old_s : allows for undo feature
        self.s_text = self.text
        self.old_s_text = self.s_text
        self.s_tokens = self.tokens
        self.old_s_tokens = self.s_tokens
        self.s_group_tokens = self.group_tokens
        self.old_s_group_tokens = self.s_group_tokens

        self.len_s_group_tokens_list = len(self.s_group_tokens)
        self.len_s_token_list = len(self.s_tokens)

        self.client = OpenAI(api_key=API_KEY)

    
    def tokenize(self, text: str):
        """
        :return: tokens, group_tokens according to text input and self.group_len. Used in to tokenize simplified text.
        """
        tokens = sent_tokenize(text)
        
        # concatenate sentences according to group length 
        group_tokens = []
        for i in range(0, len(tokens), self.group_len):
            group = " ".join(tokens[i:i + self.group_len])
            group_tokens.append(group)
        
        return tokens, group_tokens
    
    def undo(self):
        self.s_text = self.old_s_text
        self.s_tokens = self.old_s_tokens
        self.s_group_tokens = self.old_s_group_tokens

    def simplify(self, lower_bound: int, upper_bound: int, openai_params: Dict[str, any]) -> Dict[str, any]:
        '''
        Simplifies a range of text in group_tokens and saves them to self variables.
        :param lower_bound: lower index for slice of group_tokens to cwi
        :param upper_bound: upper index (not included) for slice of group_tokens to cwi
        :param openai_params: parameters for openai query
        :return: None
        '''

        # save old text
        self.old_s_text = self.s_text
        self.old_s_tokens = self.s_tokens
        self.old_s_group_tokens = self.s_group_tokens
        
        # prompt openai for simplification
        ts_output = self._ts(lower_bound, upper_bound, openai_params=openai_params)
        new_sgt = self.s_group_tokens
        new_sgt[lower_bound : upper_bound] = ts_output['completion']

        self.set_parameters(new_sgt)
        
    def set_parameters(self, new_text):
        """
        Sets all s_ based on new text
        """
        self.s_text = ' '.join(new_text)  # is this too shady? idk. its 9:25 at night I cant
        self.s_tokens, self.s_group_tokens = self.tokenize(self.s_text)

        self.len_s_token_list = len(self.s_tokens)
        self.len_s_group_tokens_list = len(self.s_group_tokens)
        

    def _ts(self, lower_bound: int, upper_bound: int, openai_params) -> Dict[str, any]:
        '''
        Returns simplifications of each sentence. Use simplify instead.
        :param lower_bound: lower index for slice of group_tokens to cwi
        :param upper_bound: upper index (not included) for slice of group_tokens to cwi
        :param openai_params: params for openai query
        :return: Dictionary of (lb, ub, response) where self.group_tokens[i] corresponds to response[i]
        '''

        completion = []
        for idx in range(lower_bound, upper_bound):

            context_dict = self.context_from_group(idx, self.context_window_size)  # todo
            query = self.ts_query(**context_dict, user=self.user, params=openai_params)

            response = self.client.chat.completions.create(**query)
            completion.append(
                response.choices[0].message.content
                )
            
            # query debugging
            # print("-" * 10)
            # print(response.choices[0].message.content)
        
        output = {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'completion': completion,
        }

        return output

    def ts_query(self, context, target, user, params) -> Dict:
        """
        :param context: context for prompt; see prompts.py
        :param target: target for prompt; see prompts.py
        :param user: user for prompt; see prompts.py
        :param params: parameters for query
        """

        cw = context_window()['ts']

        # most of these below variables can be tuned, either globally or on a context specific basis
        prompt = return_ts(context, target, user)['zero_shot']

        query = {
            'model': self.openai_model,
            'messages': [
                {'role': 'system', 'content': cw},
                {'role': 'user', 'content': prompt}
            ],
            'stream': False,
        }

        query.update(params)  # haha unfiltered parameter inputs (should be fine though)

        return query

    def context_from_group(self, idx: int, window: int) -> Dict[str, str]:
        """
        Returns a dictionary of context and target. For use in generating a ts_query input (excluding "user") field.
        :param idx: refers to the index found in self.group_tokens.
        :param window: size of context window in number of sentences (self.tokens), not groups (self.group_tokens).
        """
        tok_idx = idx * self.group_len

        lb = max(tok_idx-window, 0)  # prevents underflow
        ub = min(tok_idx+self.group_len + window, len(self.tokens))  # prevents overflow

        target = self.s_group_tokens[idx]
        context_lower = self.s_tokens[lb : tok_idx]
        context_higher = self.s_tokens[tok_idx+self.group_len : ub]

        context_list = context_lower + ["\n[Target]\n"] + context_higher
        context = " ".join(context_list)
        output = {
            "context": context,
            "target": target,
        }

        return output
