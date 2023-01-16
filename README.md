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

## Notizen

https://pipenv.pypa.io/en/latest/

https://stackoverflow.com/questions/57919110/how-to-set-pipenv-venv-in-project-on-per-project-basis
python3 -m virtualenv -p python3 .venv
pipenv install

https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html

https://flask.palletsprojects.com/en/1.0.x/deploying/mod_wsgi/

https://phoenixnap.com/kb/how-to-install-python-3-centos-7

http://wiki.centos-webpanel.com/how-to-deploy-django-apps-using-apache-with-mod-wsgi-and-nginx
https://phoenixnap.com/kb/how-to-install-python-3-centos-7

https://dev.to/brandonwallace/deploy-flask-the-easy-way-with-gunicorn-and-nginx-jgc

https://docs.gunicorn.org/en/stable/deploy.html#using-virtualenv
