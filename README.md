# openai-bot

Testing GPT-3 with python

Heavily based on:
[https://www.twilio.com/blog/openai-gpt-3-chatbot-python-twilio-sms]

and

[https://github.com/slackapi/bolt-python/tree/main/examples/getting_started]

## Running locally

### 1. Setup environment variables

```zsh
# edit .env

OPENAI_KEY=<your-openai-api-key>
SLACK_BOT_TOKEN=<your-bot-token>
SLACK_SIGNING_SECRET=<your-signing-secret>
SLACK_APP_TOKEN=<your-app-token>
```

### 2. Setup your local project

```zsh
# Clone this project onto your machine
git clone https://github.com/swaldtmann/openai-bot

# Change into this project
cd openai-bot

# Setup virtual environment
pipenv install
```

### 3. Run socket app

```zsh
pipenv shell
python3 app_socket.py
```

### 4. Or http based server

```zsh
pipenv shell
python3 app_http.py &
ngrok http 3000
```
