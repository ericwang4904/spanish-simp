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
    'model': 'gpt-3.5-turbo',#'pplx-7b-chat',
    'context_window_size': 1,  # higher values give more context but require more tokens
}]

base_restart_params = [{
    'group_len': 3,  # higher values require fewer tokens but may be less fine
}]

base_api_params = [{
    'temperature': 0.2,
    'max_tokens': 1024,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}]

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

def load_api_key(ts: TS, api_key: str):
    load_api_key = st.button("Load Your API Key")
    if load_api_key:
        ts.client.api_key = api_key

def simplify_selections(ts: TS, selection: list, api_params: dict):
    simplify = st.button("Simplify!")
    if simplify:
        ts.simplify(selection, api_params)
    

st.title("Article Simplifier")
st.write("This app makes use of OpenAI's api to create simplifications.")

if 'ts' not in st.session_state:
    st.session_state.ts = TS("placeholder", params=dict(**base_params[0], **base_restart_params[0]))
api_key = st.text_input(label="API Key", type='password')
load_api_key(st.session_state.ts, api_key)

st.header("News Website URL")
url = st.text_input("Website URL", placeholder='https://google.com')
load_data(st.session_state.ts, url)

st.header("Model Parameters that Require a Reset")
reset_params = st.data_editor(base_restart_params)
load_restart_params(st.session_state.ts, reset_params[0])

st.header("Model Parameters")
params = st.data_editor(base_params)
load_params(st.session_state.ts, params[0])

st.header("Completion Parameters")
api_params = st.data_editor(base_api_params, column_config=st.column_config.NumberColumn())

st.header("Simplification Selection")
col1, col2 = st.columns([0.2, 0.8])
with col1:
    selection = st.data_editor(pd.Series(data=[False] * st.session_state.ts.len_s_group_tokens_list, name="Selection"))
    simplify_selections(st.session_state.ts, np.nonzero(selection)[0].tolist(), api_params[0])

with col2:
    ui_df = pd.DataFrame(
    {   
        "Original": st.session_state.ts.group_tokens,
        "Simplified": st.session_state.ts.s_group_tokens,
    }
    )
    st.table(ui_df)
