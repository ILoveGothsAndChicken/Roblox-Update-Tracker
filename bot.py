import os
import json
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
DISCORD_USER_ID = os.environ["DISCORD_USER_ID"]

VERSION_URL = (
    "https://clientsettingscdn.roblox.com"
    "/v2/client-version/WindowsPlayer"
)

STATE_FILE = "last_version.json"


def check_roblox_version():

    response = requests.get(VERSION_URL, timeout=20)
    response.raise_for_status()

    data = response.json()

    current_version = data["version"]
    current_hash = data["clientVersionUpload"]

    print(f"Roblox version: {current_version}")
    print(f"Roblox build: {current_hash}")

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            previous_data = json.load(file)

        previous_version = previous_data.get("version")
        previous_hash = previous_data.get("clientVersionUpload")
    else:
        previous_version = None
        previous_hash = None

    if not previous_hash:

        print("Initial Roblox build saved. No notification needed.")

    elif current_hash != previous_hash:

        print("Roblox build changed!")

        message = (
            f"<@{DISCORD_USER_ID}> Roblox has updated!\n\n"
            f"**New Version:** `{current_hash}`\n\n"
            f"**Previous Version:** `{previous_hash}`\n\n"
            "Hurry up and fix the external."
        )

        notification = requests.post(
            WEBHOOK_URL,
            json={
                "content": message,
                "allowed_mentions": {
                    "users": [DISCORD_USER_ID]
                }
            },
            timeout=20
        )

        notification.raise_for_status()

        print("Discord notification sent!")

    else:
        print("No Roblox update detected.")

    with open(STATE_FILE, "w") as file:
        json.dump({
            "version": current_version,
            "clientVersionUpload": current_hash
        }, file)


if __name__ == "__main__":
    check_roblox_version()
