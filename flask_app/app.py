# app.py
# app_http_flask.py
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG)

import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv

from chatbot import ask, append_interaction_to_chat_log

load_dotenv()
chat_log = None

app = App(token=os.environ["SLACK_BOT_TOKEN"],
          signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# Middleware
@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.info(body)
    return next()

""" @app.message("reset")
def message_reset(message, say, logger):
    global chat_log
    chat_log = None
    logger.info(chat_log)
    say(f"Chat log reset done. New conversation from now on ...")
 """
@app.event("message")
def handle_message_events(event, say, logger):
    global chat_log
#    try:
    incoming_msg = event['text']
    answer = ask(incoming_msg, chat_log)
    chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    logger.info(f"# of chars in chat_log: {len(chat_log)}")
    logger.info(chat_log)
    say(f"{answer}")
#    except Exception as e:
#        print(f'Error: {e}')

# @app.event("message")
# def handle_message():
#     pass

@app.command("/ki-reset")
def reset_command(ack, say):
    global chat_log
    chat_log = None
    ack()
    say(f"Chat log reset done. New conversation from now on ...")

@app.command("/ki-show-chat")
def reset_command(ack, say):
    global chat_log
    ack()
    say(f"Chat Log: \n{chat_log}")


from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(debug=True, 
                  host=os.getenv("FLASK_HOST", "127.0.0.1"),
                  port=os.getenv("FLASK_PORT", 3000))


# flask --app app --debug run -p 3000
# python3 app.py
# gunicorn --workers 4 --bind 0.0.0.0:3000 app:flask_app
