from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from flask import Flask, request, jsonify, redirect, url_for
import os
import requests
from slack_sdk import WebClient


# Environment variables for client ID and secret
SLACK_CLIENT_ID = "7121533323552.7268736007858"
SLACK_CLIENT_SECRET = "34faad1be66b19a7a99e9cf64b1e2eb6"
SLACK_SIGNING_SECRET = "496770db047189c6a32e1b7d49d41176"
REDIRECT_URI = "https://18.61.57.191:3000/slack/oauth_redirect"

# Initialize a Flask app to handle web requests
flask_app = Flask(__name__)


# Route to initiate OAuth flow
@flask_app.route("/slack/install", methods=["GET"])
def install():
    return redirect(f"https://slack.com/oauth/authorize?client_id={SLACK_CLIENT_ID}&scope=channels:read,groups:read,users:read&redirect_uri={REDIRECT_URI}")


# Handle the OAuth redirect
@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    code = request.args.get("code")
    if not code:
        return "Error: Missing 'code' parameter", 400

    else:
        try:
            print('started')
            response = requests.get("https://slack.com/api/oauth.access", params={
                "client_id": SLACK_CLIENT_ID,
                "client_secret": SLACK_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI
            })

            data = response.json()

            print('hello')

            if not data.get("ok"):
                client = WebClient(token=data["access_token"])

                resp = client.chat_postMessage(channel="U075Y42UAF8", text="Hello from Bolt!")
                print('posted')
                return jsonify(data), 400

            return jsonify(data)

        except Exception as e:
            return f"Error: {str(e)}", 500



# Start the Flask app
if __name__ == "__main__":
    flask_app.run(debug=True, port=443)

