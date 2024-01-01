from openai import OpenAI
from typing import *

class Client:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def generate_response(self, **query):
        client =  OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(**query)
        return response.choices[0].message.content