import json

import server_controlling
import random
import shared
import requests
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(""" 
command 
███████╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
█████╗  ██████╔╝█████╗  ██████╔╝██║   ██║███████╗
██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║
███████╗██║  ██║███████╗██████╔╝╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝
                    C 2  F R A M E W O R K \n

""")

parser = argparse.ArgumentParser(description="Please provide your server config")
parser.add_argument("arg1", type=str, help="The first argument (string)")
args = parser.parse_args()

# Access and use the arguments
print(f"Argument 1: {args.arg1}")

with open(args.arg1, "r") as f:
    for line in f:
        if line.startswith("server:"):
            server_config = line
        elif line.startswith("port:"):
            port_config = line
        elif line.startswith("sleep:"):
            sleep = line
        elif line.startswith("register_url:"):
            register_url = line
        elif line.startswith("command_url:"):
            command_url = line
        elif line.startswith("base_url:"):
            base_url = line

server_config = server_config.replace("server:", "").strip("\"\n")
port_config = port_config.replace("port:", "").strip("\"\n")
sleep = sleep.replace("sleep:", "").strip("\"\n")
register_url = register_url.replace("register_url:", "").strip("\"\n")
command_url = command_url.replace("command_url:", "").strip("\"\n")
base_url = base_url.replace("base_url:", "").strip("\"\n")
uuid = ""

while True:
    user_input = input("command>:")

    if user_input.lower() == "help":
        print(""" 
          
          start (Start FLask Server)
          stop (Stop Flask Server)
          use agent (set Agent UUID)
          command (Send Command to the Agent)
          command_output (Output for Agent commands)
          sleep (Change Sleep of Agent)
          list (list active Agents)
          exit (Exit the program)
          
          """)
    elif user_input.lower() == "exit":
        break

    elif user_input.lower() == "start":
        server_controlling.start(register_url, command_url, base_url, port_config)

    elif user_input.lower() == "stop":
        server_controlling.stop()

    elif user_input.lower() == "command":
        command = input("Which cmd should be executed: ")
        shared.set_command(command, uuid, sleep)

    elif user_input.lower() == "command_output":
        agent_uuid = input("Enter Agent UUID: ")
        response = requests.get(
            url=f"https://127.0.0.1:{port_config}{base_url}/{agent_uuid}/output",
            verify=False
        )
        print(response.text)

    elif user_input.lower() == "list":
        response = requests.get(f"https://127.0.0.1:{port_config}{base_url}/list", headers={'X-Auth-ID': 'MyErebusToken'}, verify=False)

        data = json.loads( response.text)

        for key, value in data.items():
            print(f"{key}: {value}")

    elif user_input.lower() == "sleep":
        sleep = input("Sleep Time: ")

    elif user_input.lower() == "use agent":
        uuid = input("Enter Agent UUID: ")

    else:
        print("Command not recognized")



