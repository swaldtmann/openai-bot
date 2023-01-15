# app_http.py
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

import os
from slack_bolt.async_app import AsyncApp
from dotenv import load_dotenv

from chatbot import ask, append_interaction_to_chat_log

load_dotenv()
chat_log = None

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"],
               signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# Middleware
@app.middleware  # or app.use(log_request)
async def log_request(logger, body, next):
    logger.info(body)
    return await next()

@app.event("message")
async def handle_message_events(event, say, logger):
    global chat_log
    incoming_msg = event['text']
    answer = ask(incoming_msg, chat_log)
    chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    logger.info(chat_log)
    await say(f"{answer}")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
