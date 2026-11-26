import os
import json
import requests

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
DISCORD_USER_ID = os.environ["DISCORD_USER_ID"]

VERSION_URL = (
    "https://clientsettings.roblox.com"
    "/v2/client-version/WindowsPlayer"
)

STATE_FILE = "last_version.json"


def check_roblox_version():
    response = requests.get(VERSION_URL, timeout=20)
    response.raise_for_status()

    current_version = response.json()["version"]

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            previous_version = json.load(file)["version"]
    else:
        previous_version = None

    if previous_version is None:
        print(f"Initial Roblox version: {current_version}")

    elif current_version != previous_version:
        print("Roblox version changed!")

        message = (
            f"<@{DISCORD_USER_ID}> "
            "Roblox has updated! Hurry up and fix the external."
        )

        requests.post(
            WEBHOOK_URL,
            json={
                "content": message,
                "allowed_mentions": {
                    "users": [DISCORD_USER_ID]
                }
            },
            timeout=20
        ).raise_for_status()

    with open(STATE_FILE, "w") as file:
        json.dump({"version": current_version}, file)


if __name__ == "__main__":
    check_roblox_version()
