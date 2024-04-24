import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import jwt
from slack_sdk.web import WebClient
import os

# getting all the env vars
load_dotenv()
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")
signing_secret = os.getenv("SLACK_SIGNING_SECRET")
slack_bot_user = os.getenv("SLACK_BOT_USER")
graphlit_organization_id = os.getenv("GRAPHLIT_ORG_ID")
graphlit_environment_id = os.getenv("GRAPHLIT_ENV_ID")
graphlit_secret_key = os.getenv("GRAPHLIT_SECRET_KEY")
graphlit_url = os.getenv("GRAPHLIT_URL")
graphlit_conversation_id = os.getenv("GRAPHLIT_CONVERSATION_ID")

# creating flask app
flask_app = Flask(__name__)

def get_graphlit_token(organization_id, 
                       environment_id, secret_key, issuer="graphlit", audience="https://portal.graphlit.io",
                       role = "Owner", expiration_hours = 1) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)

    # Define the payload
    payload = {
        "https://graphlit.io/jwt/claims": {
            "x-graphlit-environment-id": environment_id,
            "x-graphlit-organization-id": organization_id,
            "x-graphlit-role": role,
        },
        "exp": expiration,
        "iss": issuer,
        "aud": audience,
    }

    # Sign the JWT
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    # verify the token
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"], audience=audience)
        print(decoded)
    except jwt.ExpiredSignatureError as ex:
        print("Error: Token has expired")
        raise ex
    except jwt.InvalidTokenError as ex:
        print("Error: Invalid token")
        raise ex
    return token

slack_client = WebClient(token=slack_token)
token = get_graphlit_token(graphlit_organization_id, graphlit_environment_id, graphlit_secret_key)
transport = RequestsHTTPTransport(url=graphlit_url, headers={"Authorization": f"Bearer {token}"})
gql_client = Client(transport=transport)

def graphlit_request(prompt: str) -> dict:
    """
    Wrapper function to make graphlit request
    """
    query = gql(
        """
        mutation PromptConversation($prompt: String!, $promptConversationId: ID) {
        promptConversation(prompt: $prompt, id: $promptConversationId) {
            message {
            message
            }
            messageCount
            conversation {
            id
            }
        }
        }
        """
    )

    variables = {
        "prompt": prompt,
        "promptConversationId": graphlit_conversation_id
    }

    return gql_client.execute(query, variable_values=variables)

@flask_app.route("/slack-incoming", methods=["POST"])
def slack_challenge():
    event_data = request.json
    slack_user_id = slack_client.api_call("auth.test")["user_id"]
    if "challenge" in event_data:
        # Verification challenge to confirm the endpoint
        return jsonify({'challenge': event_data['challenge']})
    elif "event" in event_data:
        event = event_data['event']
        print(f'event type got it: {event.get("type")}')

        # Handle message events
        if event.get("type") == "message" and "subtype" not in event:
            # Process the message
            user = event["user"]
            text = event["text"]
            try:
                response = graphlit_request(text)
                message = response.get("promptConversation").get("message").get("message")
                print(message)
            except Exception as ex:
                # if something goes wrong, respond accordingly.
                message = "I'm sorry something went wrong internally. Please try again."

            # Send the response to Slack
            slack_client.chat_postMessage(channel=slack_channel, text=message) if user !=  slack_user_id else None
    return "OK", 200

if __name__ == "__main__":
    flask_app.run(port=5000, debug=True)
