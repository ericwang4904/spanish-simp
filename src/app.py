import streamlit as st
import numpy as np
import pandas as pd

from typing import *

from model import TS
from prompts import *
from request_handler import rawtext_from_url

from functools import cached_property

base_user = f"Spanish beginner with good understanding of sentence structure, but poor vocabulary."

base_params = [{
    'user': base_user, 
    'context_window_size': 1, # higher values give more context but require more tokens
    'model': 'gpt-3.5-turbo',  # use gpt-3.5 for testing; gpt-4 is expensive!
}] # list of dict insures that data typing stays when in data_editor

base_restart_params = [{
    'group_len': 3,  # higher values require fewer tokens but may be less fine
}] # list of dict insures that data typing stays when in data_editor

base_openai_params = [{
    'temperature': 0.2,
    'max_tokens': 256,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}] # list of dict insures that data typing stays when in data_editor


def cache_func(_obj: TS):
    attr = _obj.__dict__
    attr.pop("client")  # unhashable
    st.session_state.attr = attr

#print(hash_func(TS("", params={})))

def load_model(attr):
    obj = TS("placeholder", params={})
    obj.set_attributes(attr)
    return obj

def load_data(ts: TS, url):
    load_button = st.button("Load Data Into Model (this will reset progress)")
    if load_button:
        try:
            rawtext = rawtext_from_url(url)
        except:
            st.write("Invalid URL!")
            return

        # setting new data
        ts.load_text(rawtext)
        
        cache_func(ts)

    
def load_params(ts: TS, params: dict):
    load_params = st.button("Load params into model (this will NOT reset progress)")
    if load_params:
        ts.load_params(params)

        cache_func(ts)

def load_restart_params(ts: TS, params: dict):
    load_restart_params = st.button("Load params into model (this will reset progress)")
    if load_restart_params:
        ts.load_restart_params(params)

        cache_func(ts)

def load_api_key(ts: TS, api_key: str):
    load_api_key = st.button("Load Your OpenAI API Key")
    if load_api_key:
        ts.client.api_key = api_key

        cache_func(ts)

def simplify_selections(ts: TS, selection: list, openai_params: dict):
    simplify = st.button("Simplify!")
    if simplify:
        ts.simplify(selection, openai_params)

        cache_func(ts)

st.title("Text Simplifier")
try:
    ts = load_model(st.session_state.attr)
except:  # initialize if no attributes to load
    ts = load_model(dict())
    cache_func(ts)

api_key = st.text_input(label="OpenAI API Key", type='password')
load_api_key(ts, api_key)

st.header("News Website URL")
url = st.text_input("Website URL", placeholder='https://google.com')
load_data(ts, url)

st.header("Model Parameter that Require a Reset")
reset_params = st.data_editor(base_restart_params)
load_restart_params(ts, reset_params[0])

st.header("Model Parameters")
params = st.data_editor(base_params)
load_params(ts, params[0])

st.header("OpenAI Parameters")
openai_params = st.data_editor(base_openai_params)

st.header("Simplification Selection")
col1, col2 = st.columns([0.2, 0.8])
with col1:
    selection = st.data_editor(pd.Series(data=[False] * ts.len_s_group_tokens_list, name="Selection"))
    simplify_selections(ts, np.nonzero(selection)[0].tolist(), openai_params[0])

with col2:
    ui_df = pd.DataFrame(
    {   
        "Original": ts.group_tokens,
        "Simplified": ts.s_group_tokens,
    }
    )
    st.table(ui_df)