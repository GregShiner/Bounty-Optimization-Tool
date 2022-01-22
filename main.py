import aiobungie
from os import environ
from dotenv import load_dotenv

load_dotenv(".env")

key=environ["key"]
client_id=environ["client_id"]
client_secret=environ["client_secret"]

client = aiobungie.Client(key)

async def main() -> None:
    async with aiobungie.RESTClient(key,client_id=client_id,client_secret=client_secret) as restClient:
        print(restClient.build_oauth2_url())
    """
    users = await client.search_users('Gman1230321')
    for user in users:
        if str(user.type) != "STADIA":
            print(user.name, user.type, user.id)
            profile = await client.fetch_profile(user.id, user.type)
            print(profile.character_ids)
    """

client.run(main())