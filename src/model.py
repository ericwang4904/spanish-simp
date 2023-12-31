from openai_api import Client  # specific api provider

import regex as re

from nltk import sent_tokenize, word_tokenize
from string import punctuation as PUNCT
from typing import *

import logging as log
from prompts import *

try:  # developers don't have to enter api key 
    from config import API_KEY
except:
    API_KEY = ''

import pandas as pd
import numpy as np

from copy import deepcopy

class TS:
    def __init__(self, text: str, params: dict) -> None:
        """
        Text Simplification Object. 
        :param text: text to be simplifed
        :param params: Other parameters for the object.
            user: description of user's linguistic capabilites
            group_len: number of sentences per token group. Defaults to 1.  
            context_window_size: the size of the window in the context for context_from_group (in # of tokens)
            model: name of model (e.g. gpt-3.5-turbo and mixtral-8x7b-instruct)
        """
        self.text = text
        self.load_params(params)
        self.load_restart_params(params)
        self.load_text(self.text)
        self.load_token_length()

        self.client = Client(api_key=API_KEY)  # api
    
    def load_user(self, user):
        self.user = user

    def load_params(self, params):
        """
        load parameters that don't require a full restart
            - model
            - user
            - context_window_size
        """
        try: self.user = params['user']
        except KeyError: log.error("user not provided")

        self.context_window_size = int(params.get("context_window_size", 1))
        self.model_name = str(params.get("model", "null"))

    def load_restart_params(self, params):
        """
        load parameters that require full restart of simplification process
            - group_len
        """
        
        self.group_len = int(params.get("group_len", 3))
        
        self.load_text(self.text)
        self.load_token_length()

    def load_text(self, text):
        """
        load text, tokens, and group tokens into model from rawtext input
        """

        self.text = text
        self.tokens = self.make_tokens(self.text) 
        self.group_tokens = self.make_groups(self.tokens)

        # s_ : simplified language (used in simplification iteratively) 
        # old_s : allows for undo feature
        self.s_text = deepcopy(self.text)
        self.s_group_tokens = deepcopy(self.group_tokens)

        # Possibly useful for recursive simplification (i.e. context windows with simplified text), but unused
        self.s_tokens = deepcopy(self.tokens)

    def set_s_text(self, s_group_tokens):
        """
        Sets new text and sentences based on self.s_group_tokens. Groups are not remade, to preserve the structure of the text.
        """

        self.s_group_tokens = deepcopy(s_group_tokens)
        self.s_text = ' '.join(self.s_group_tokens)
        self.s_tokens = sent_tokenize(self.s_text)

        self.len_s_token_list = len(self.s_tokens)

    def load_token_length(self):
        self.len_s_group_tokens_list = len(self.s_group_tokens)
        self.len_s_token_list = len(self.s_tokens)


    def make_tokens(self, text: str) -> List[str]:
        return sent_tokenize(text)
     
    def make_groups(self, tokens: List[str]) -> List[str]:
        """
        :return: group_tokens according to self.group_len. 
        """        
        # concatenate sentences according to group length 
        group_tokens = []
        for i in range(0, len(tokens), self.group_len):
            group = " ".join(tokens[i:i + self.group_len])
            group_tokens.append(group)
        
        return group_tokens

    def simplify(self, ids: List[int], api_params: Dict[str, any]):
        '''
        Simplifies a range of text in group_tokens and saves them to self variables.
        :param ids: List of ids in group_tokens for simplification
        :param api_params: parameters for querying api provider
        :return: None
        '''
        # prompt api provider for simplification

        ts_output = self._ts(ids, api_params=api_params)
        
        ngt = self.s_group_tokens
        for output_idx, group_index in enumerate(ids):
            ngt[group_index] = ts_output['completion'][output_idx]

        self.set_s_text(ngt)
        

    def _ts(self, ids: List[int], api_params) -> Dict[str, any]:
        '''
        Returns simplifications of each sentence. Use simplify instead.
        :param ids: List of ids in group_tokens for simplification
        :param api_params: params for querying api provider
        :return: Dictionary of (ids, completion) where self.group_tokens[ids[i]] corresponds to completion[i]
        '''

        completion = []
        for id in ids:
            context_dict = self.context_from_group(id, self.context_window_size)  # todo
            query = self.ts_query(**context_dict, user=self.user, params=api_params)
            
            completion.append(
                self.client.generate_response(**query)
                )
            
            # query debugging:
            #print("-" * 10)
            #print(response.choices[0].message.content)
        
        output = {
            'ids': ids, 
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

        cw = context_window()['ts']  # todo: add selector option?

        # most of these below variables can be tuned, either globally or on a context specific basis
        prompt = return_ts(context, target, user)['zero_shot']

        query = {
            'model': self.model_name,
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

        THIS IS THE FUNCTION TO CHANGE FOR IMPROVEMENTS AND QOL TO PROMPTING; THIS FUNCTION GENERATES THE CONTEXT
        """
        tok_idx = idx * self.group_len

        lb = max(tok_idx-window, 0)  # prevents underflow
        ub = min(tok_idx+self.group_len + window, len(self.tokens))  # prevents overflow

        target = self.group_tokens[idx] 
        context_lower = self.tokens[lb : tok_idx]
        context_higher = self.tokens[tok_idx+self.group_len : ub]

        context_list = context_lower + ["\n[Target]\n"] + context_higher
        context = " ".join(context_list)
        output = {
            "context": context,
            "target": target,
        }

        return output
