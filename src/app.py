import streamlit as st
import numpy as np
import pandas as pd

from model import TS
from prompts import *
from request_handler import rawtext_from_url

base_user = f"English beginner with good understanding of sentence structure, but poor vocabulary."

base_params = {
    'user': base_user, 
    'context_window_size': 1, # higher values give more context but require more tokens
    'model': 'gpt-3.5-turbo',  # use gpt-3.5 for testing; gpt-4 is expensive!
}

base_restart_params = {
    'group_len': 3,  # higher values require fewer tokens but may be less fine
}

base_openai_params = {
    'temperature': 0,
    'max_tokens': 256,
    'frequency_penalty': 0,
    'presence_penalty': 0,
}


# App

@st.cache_resource
def load_model():
    return TS("placeholder", base_params)

def load_data(url):
    load_button = st.button("Load Data Into Model (this will reset progress)")
    if load_button:
        try:
            rawtext = rawtext_from_url(url)
        except:
            st.write("Invalid URL!")
            return

        # setting new data
        model.load_text(rawtext)
    
    
def load_params(params):
    load_params = st.button("Load params into model")
    if load_params:
        model.load_params(params)

def load_restart_params(params):
    load_restart_params = st.button("Load params into model (this will reset progress)")
    if load_restart_params:
        model.load_restart_params(params)

    # reformat text for group_len (causes a reset)
    model.group_tokens = model.make_groups(model.tokens)
    model.s_group_tokens = model.group_tokens
    model.load_token_length()

def simplify_selections(selection):
    simplify = st.button("Simplify!")
    if simplify:
        print("wtf")
        model.simplify(
            selection,
            openai_params
            )
        print("done")

st.title("Yolanda's Spanish Simplifier")
model = load_model()

st.header("News Website URL")
url = st.text_input("Website URL", placeholder='https://google.com')
load_data(url)
st.header("Model Parameter that Require a Reset")
reset_params = st.data_editor(base_restart_params)
load_restart_params(reset_params)
st.header("Model Parameters")
params = st.data_editor(base_params)
load_params(params)
st.header("OpenAI Parameters")
openai_params = st.data_editor(base_openai_params)

st.header("Simplification Selection")

ui_df = pd.DataFrame(
    {   
        "Selected": False,
        "Original": model.group_tokens,
        "Simplified": model.s_group_tokens,
    }
)

col1, col2 = st.columns([0.2, 0.8])
with col1:
    selection = st.data_editor(ui_df["Selected"])
    simplify_selections(np.nonzero(selection)[0].tolist())

with col2:
    st.table(ui_df.loc[:, ["Original", "Simplified"]])
