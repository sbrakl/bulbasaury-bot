import slack
import os
import logging
from config import config
from flask import Flask
from slackeventsapi import SlackEventAdapter
from pprint import pformat
from bsbslackhelpers.bsbSlackMessage import BSB_SlackMessage

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
app = Flask(__name__)
logger = logging.getLogger('bs')

def setLoggingUp():
    logging.basicConfig(level=logging.INFO,
            format='[%(levelname)s-%(name)s] %(message)s')
    

def main():
    config.loadConf()
    setLoggingUp()
    signing_secret = os.environ["SLACK_APP_SIGNING_SECRET"]
    slack_event_adapter = SlackEventAdapter(signing_secret ,'/slack/events', app)
    bot_id = client.api_call('auth.test')['user_id'] #Another way to call the Slack API
    logger.info(f"bot id: {bot_id}")

    @slack_event_adapter.on('message')
    def reply_message(payload):
        logger.debug("Slack payload received")
        logger.debug(pformat(payload))
        bsb_slack_msg = BSB_SlackMessage(payload, bot_id)
        if bsb_slack_msg.HasMessageEvent:
            event = bsb_slack_msg.event()
            channel_id = event.get('channel')
            logger.info(f"Channel id: {channel_id}")
            user_id = event.get('user')
            logger.info(f"User id: {user_id}")
            text = event.get('text')
            logger.info(f"text: {text}")
            subtype = event.get('subtype', '')
            logger.info(f"subtype: {subtype}")
            
            dm = bsb_slack_msg.IsDirectMessage()
            mb = bsb_slack_msg.IsMessageFromBot()
            logger.info(f"Is Direct message: {dm}, Is Message from bot: {mb}")
            if bsb_slack_msg.IsDirectMessage() and not bsb_slack_msg.IsMessageFromBot():
                client.chat_postMessage(channel=channel_id, text=text)

    if __name__ == "__main__":
        app.run()

@app.route('/')
def index():
    return "Hello from bulbasaury-bot"


def sendhelloMessage():
    client.chat_postMessage(channel='#slackbot-development', text="Hello from bulbasaury-bot!")

main()