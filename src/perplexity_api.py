import requests
from json import loads
from typing import *

class Client:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    def generate_response(self, **query):
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(url, json=query, headers=headers)
        response_dict = loads(response.text)
        return response_dict['choices'][0]['message']['content']