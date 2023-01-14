# openai-bot
Testing GPT-3 with python


Heavily based on:
https://www.twilio.com/blog/openai-gpt-3-chatbot-python-twilio-sms

and 

https://github.com/slackapi/bolt-python/tree/main/examples/getting_started

## Running locally

### 1. Setup environment variables

```zsh
# edit .env

OPENAI_KEY=<your-openai-api-key-here>
SLACK_BOT_TOKEN=<your-bot-token>
SLACK_SIGNING_SECRET=<your-signing-secret>
```

### 2. Setup your local project

```zsh
# Clone this project onto your machine
git clone https://github.com/???

# Change into this project
cd ???

# Setup virtual environment
pipenv install
```

### 3. Start servers

```zsh
pipenv shell
python3 app.py
ngrok http 3000
```