import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

token = os.getenv('APP_TOKEN')
if not token:
    print("Error: there isn't token")
client = WebClient(token=token)

def list_connections():
    try:
        users_response = client.users_list()
        print("Users:")
        for user in users_response['members']:
            print(f"- {user['name']} ({user['id']})")

        channels_response = client.conversations_list(types="public_channel,private_channel")
        print("\nChannels:")
        for channel in channels_response['channels']:
            print(f"- {channel['name']} ({channel['id']})")

        test_response = client.api_test()
        print("\nAPI Test Response:", test_response)

    except SlackApiError as e:
        print(f"Error: {e.response['error']}")

list_connections()
