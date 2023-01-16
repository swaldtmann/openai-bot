# app_http_async.py
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

import os
from slack_bolt.async_app import AsyncApp
from dotenv import load_dotenv

from flask_app.chatbot import ask, append_interaction_to_chat_log

load_dotenv()
chat_log = None

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"],
               signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# Middleware
@app.middleware  # or app.use(log_request)
async def log_request(logger, body, next):
    logger.info(body)
    return await next()

""" @app.message("reset")
async def message_reset(message, say, logger):
    global chat_log
    chat_log = None
    logger.info(chat_log)
    await say(f"Chat log reset done. New conversation from now on ...")
 """
@app.event("message")
async def handle_message_events(event, say, logger):
    global chat_log
    global chat_log
    try:
        incoming_msg = event['text']
        answer = ask(incoming_msg, chat_log)
        chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        logger.info(f"# of chars in chat_log: {len(chat_log)}")
        logger.info(chat_log)
        await say(f"{answer}")
    except Exception as e:
        print(f'Error: {e}')

@app.command("/ki-reset")
async def reset_command(ack, say):
    global chat_log
    chat_log = None
    await ack()
    await say(f"Chat log reset done. New conversation from now on ...")

@app.command("/ki-show-chat")
async def reset_command(ack, say):
    global chat_log
    await ack()
    await say(f"Chat Log: \n{chat_log}")

# TODO Is this correct???
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
