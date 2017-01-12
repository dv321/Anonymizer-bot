import json

from flask import Flask, request, make_response, redirect
from os import getenv
from slackclient import SlackClient


CLIENT_ID = getenv("SLACK_CLIENT_ID")
CLIENT_SECRET = getenv("SLACK_CLIENT_SECRET")
VERIFICATION_TOKEN = getenv("SLACK_CLIENT_VERIFICATION_TOKEN")
TEST_TOKEN = getenv("SLACK_CLIENT_TEST_TOKEN")

BOT_NAME = "anonymizer-bot"
ANON_CHANNEL = "anonymizer-channel"

slack = SlackClient(TEST_TOKEN)
app = Flask(__name__)


def send_message(channel_id, message):
    slack.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=BOT_NAME
    )


def auth(code):
    """
    Authenticate with OAuth and assign correct scopes.

    Args:
        code : str
            Temporary authorization code sent by Slack to be exchanged for an
            OAuth token
    """

    # yeah yeah globals are evil, sue me
    global slack

    auth_response = slack.api_call(
        "oauth.access",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
    )


@app.route("/oauth", methods=["GET", "POST"])
def oauth_route():
    """This route is called by Slack after the user installs our app."""

    code_arg = request.args.get('code')

    # The bot's auth method to handles exchanging the code for an OAuth token
    auth(code_arg)

    return ""


@app.route("/install", methods=["GET", "POST"])
def install_route():
    """Redirects the user to the slack app installation url. Only asks for the 'bot' scope."""

    scope = "bot"

    url = "https://slack.com/oauth/authorize?scope=%s&client_id=%s" % (scope, CLIENT_ID)

    return redirect(url)


@app.route("/listening", methods=["GET", "POST"])
def listen():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot. It can respond to verification challenges and
    bot events.

    #NOTE: CURRENTLY ASSUMES WE ARE ONLY SUBSCRIBED TO 'MESSAGE.IM' EVENTS
    """

    slack_event = json.loads(request.data)

    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    # For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"})

    if slack_event.get("token") != VERIFICATION_TOKEN:
        return None

    message = "Someone said: %s" % slack_event['event']['text']
    send_message(ANON_CHANNEL, message)

    return ""


if __name__ == "__main__":
    app.run()
