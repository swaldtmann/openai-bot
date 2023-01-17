# chatbot.py
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    before
)

logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

start_chat_log = list()
start_chat_log.append("Human: Hello, who are you?")
start_chat_log.append("AI: I am doing great. How can I help you today?")

chat_log = list()

engine_model = "text-davinci-003"
engine_max_tokens = 400

def shorten_chat_log():
    global chat_log
    # TODO 
    first_item = chat_log.pop(0)
    second_item = chat_log.pop(0)
    logger.info('shortened!')
    return True

@retry(stop=stop_after_attempt(6),
       before=shorten_chat_log(), 
       retry=retry_if_exception_type(openai.error.Timeout))
def ask_with_backoff(**kwargs):
    return ask(**kwargs)

def create_prompt(question, chat_log):
    return f'{chat_log_to_str(chat_log)}\nHuman: {question}\nAI:'

def ask(question, a_chat_log=None):
    global chat_log
    chat_log = a_chat_log
    #try:
    if chat_log is None:
        chat_log = start_chat_log
    prompt = create_prompt(question, chat_log)
    logger.info(f'\nchat_log:\n{chat_log}')
    logger.info(f'\nprompt:\n{prompt}')
    response = completion.create(
        prompt=prompt, engine=engine_model, stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=engine_max_tokens,
        request_timeout=0.01, # exception debugging only!!
        )
    answer = response.choices[0].text.strip()
    return answer

"""     except openai.error.Timeout as exception:
        print ("Timeout: {}".format(exception))

    except Exception as exception:
        print("Exception: {}".format(type(exception).__name__))
        print("Exception message: {}".format(exception))
 """    
def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    chat_log.append(f'Human: {question}')
    chat_log.append(f'AI: {answer}')
    return chat_log

def chat_log_to_str(chat_log):
    return "\n".join(chat_log)
