# chatbot.py
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
import openai

logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''
engine_model = "text-davinci-003"
engine_max_tokens = 400


def ask(question, chat_log=None):
    try:
        if chat_log is None:
            chat_log = start_chat_log
        prompt = f'{chat_log}Human: {question}\nAI:'
        response = completion.create(
            prompt=prompt, engine=engine_model, stop=['\nHuman'], temperature=0.9,
            top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
            max_tokens=engine_max_tokens)
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f'Error: {e}')    

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'
