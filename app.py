from __future__ import annotations
import aiobungie
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import pprint # debugging purposes only
from inspect import getmembers # debugging purposes only
import dill
import sqlite3

baseurl = "https://localhost:5000"

app = Flask(__name__)
CORS(app)

load_dotenv(".env")

key = environ["key"]
client_id = environ["client_id"]
client_secret = environ["client_secret"]

pp = pprint.PrettyPrinter(indent=4)

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

async def generate_oauth_url():
    async with aiobungie.RESTClient(key, client_id=client_id, client_secret=client_secret) as restClient:
        return restClient.build_oauth2_url()

@app.route("/quests", methods=["GET"])
async def getQuests():
    try:
        client = aiobungie.Client(key)
        user = await client.fetch_current_user_memberships(request.headers["Authorization"])
        memberships = user.destiny
        primary_membership = user.primary_membership_id
        membership = list(filter(lambda membership: membership.id == primary_membership, memberships))[0]
        component = await membership.fetch_self_profile(*(aiobungie.ComponentType.CHARACTER_INVENTORY, aiobungie.ComponentType.ITEM_OBJECTIVES, aiobungie.ComponentType.ITEM_INSTANCES, aiobungie.ComponentType.CHARACTERS))
        inventories = [inventory for inventory in component.character_inventories.values()][2]
        items = []
        for item in inventories:
            try:
                items.append(await item.fetch_self())
            except Exception as e:
                if ("tierTypeName" in str(e)) or ("ItemTier" in str(e)):
                    continue
                else:
                    raise e
        quests = list(filter(lambda item: item.type == aiobungie.ItemType.BOUNTY, items))
        return str(quests)

    except Exception as e:
        raise e
    finally:
        await client.rest.close()
@app.route("/manifest", methods=["POST"])
async def fetchManifest():
    async with aiobungie.RESTClient(key) as restClient:
        await restClient.download_manifest()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run()