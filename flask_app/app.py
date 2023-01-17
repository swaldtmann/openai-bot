# app.py
# app_http_flask.py
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from dotenv import load_dotenv

from chatbot import ask, append_interaction_to_chat_log, chat_log_to_str

load_dotenv()
data = dict()
data['chat_log'] = None

app = App(token=os.environ["SLACK_BOT_TOKEN"],
          signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# Middleware
@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()

@app.event("message")
def handle_message_events(event, say, logger):
    global data
    incoming_msg = event['text']
    answer = ask(incoming_msg, data['chat_log'])
    if answer:
        data['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, data['chat_log'])
        logger.info(data['chat_log'])
        logger.info(f"# of chars in chat_log: {len(chat_log_to_str(data['chat_log']))}")
        say(f"{answer}")
    else:
        say(f"No answer from bot ...")

# @app.event("message")
# def handle_message():
#     pass

@app.command("/ki-reset")
def reset_command(ack, say):
    global data
    data['chat_log'] = None
    ack()
    say(f"Chat log reset done. New conversation from now on ...")

@app.command("/ki-show-chat")
def reset_command(ack, say):
    global data
    ack()
    if data['chat_log']:
        chat_log_str = chat_log_to_str(data['chat_log'])
    else:
        chat_log_str = "Chat log is empty."
    say(f"Chat Log: \n{chat_log_str}")


from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(debug=True, 
                  threaded=True,
                  host=os.getenv("FLASK_HOST", "127.0.0.1"),
                  port=os.getenv("FLASK_PORT", 3000))


# flask --app app --debug run -p 3000
# python3 app.py
# gunicorn --workers 4 --bind 0.0.0.0:3000 app:flask_app
