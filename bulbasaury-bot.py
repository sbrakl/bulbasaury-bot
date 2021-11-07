import slack
import os
from config import config


def main():
    config.loadConf()
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#slackbot-development', text="Hello from bulbasaury-bot!")

main()