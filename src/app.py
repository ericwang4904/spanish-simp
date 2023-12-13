import streamlit as st
import numpy as np
import pandas as pd

from typing import *

from model import TS
from prompts import *
from request_handler import rawtext_from_url

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


# App
@st.cache_resource
def load_model():
    return TS("placeholder", params={})

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
    
    
def load_params(ts: TS, params: dict):
    load_params = st.button("Load params into model (this will NOT reset progress)")
    if load_params:
        ts.load_params(params)

def load_restart_params(ts: TS, params: dict):
    load_restart_params = st.button("Load params into model (this will reset progress)")
    if load_restart_params:
        ts.load_restart_params(params)


def simplify_selections(ts: TS, selection: list, openai_params: dict):
    simplify = st.button("Simplify!")
    if simplify:
        ts.simplify(selection, openai_params)

st.title("Yolanda's Spanish Simplifier")
ts = load_model()
#api_key = st.text_input(label="OpenAI API Key", type='password')
#ts.client.api_key = api_key


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
