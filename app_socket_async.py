# app_socket.py
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.ERROR)

import os
from dotenv import load_dotenv

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from chatbot import ask, append_interaction_to_chat_log

load_dotenv()
chat_log = None

# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"],
              raise_error_for_unhandled_request=True)

@app.middleware
async def log_request_headers(logger, body, next):
    logger.error(body)
    return await next()

# @app.middleware  # or app.use(log_request)
# async def log_request(logger, body, next):
#    logger.debug(body)
#    return await next()

@app.event("message")
async def handle_message_events(event, say, logger):
    global chat_log
    incoming_msg = event['text']
    answer = ask(incoming_msg, chat_log)
    chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    logger.error(chat_log)
    await say(f"{answer}")

@app.event("message")
async def handle_message_events(body, logger):
    logger.error(body)


async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())