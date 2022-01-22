import aiobungie
from os import environ
from dotenv import load_dotenv
from flask import Flask, request, redirect

baseurl = "https://localhost:5000"

app = Flask(__name__)

@app.route("/login")
def login():
    url = client.run(generate_oauth_url())
    return redirect(url)

@app.route("/authorize")
def authorize():
    return request.args.to_dict()

load_dotenv(".env")

key = environ["key"]
client_id = environ["client_id"]
client_secret = environ["client_secret"]

client = aiobungie.Client(key)

async def generate_oauth_url() -> None:
    async with aiobungie.RESTClient(key,client_id=client_id,client_secret=client_secret) as restClient:
        return restClient.build_oauth2_url()

if __name__ == "__main__":
    app.run(ssl_context='adhoc')