import aiobungie
from os import environ
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

baseurl = "https://localhost:5000"

app = Flask(__name__)
CORS(app)

load_dotenv(".env")

key = environ["key"]
client_id = environ["client_id"]
client_secret = environ["client_secret"]

client = aiobungie.Client(key)

@app.route("/oauth-url", methods=["GET"])
async def getOauthUrl():
    url = await generate_oauth_url()
    return url

@app.route("/authorize")
async def authorizeUser():
    async with aiobungie.RESTClient(key, client_id=int(client_id), client_secret=client_secret) as restClient:
        code = request.args.to_dict()["code"]
        tokens = await restClient.fetch_oauth2_tokens(code)
        response = {
            "access_token":tokens.access_token,
            "refresh_token":tokens.refresh_token,
            "expires_in":tokens.expires_in,
            "token_type":tokens.token_type,
            "refresh_expires_in":tokens.refresh_expires_in,
            "membership_id":tokens.membership_id
        }
        return response

@app.route("/player")
async def getPlayer(token=None, internal=False):
    if not token:
        token = request.headers["Authorization"]
    player = await client.fetch_current_user_memberships(token)
    if internal:
        return player
    return str(player.primary_membership_id)

async def generate_oauth_url() -> None:
    async with aiobungie.RESTClient(key, client_id=client_id, client_secret=client_secret) as restClient:
        return restClient.build_oauth2_url()

if __name__ == "__main__":
    app.run()