import server_controlling

print(""" 

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
          exit (Exit the program)
          """)
    elif user_input.lower() == "exit":
        break

    elif user_input.lower() == "start":
        server_controlling.start()

    elif user_input.lower() == "stop":
        server_controlling.stop()

    else:
        print("Command not recognized")



