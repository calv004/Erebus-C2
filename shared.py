command = None

def set_command(cmd, uuid, sleep):
    with open("command.txt", "w" ) as f:
        f.write(cmd + ";" + uuid + ":" + sleep)

def read_command():
    try:
        with open("command.txt", "r") as f:
            content = f.read()
            return content if content != "" else None
    except FileNotFoundError:
        return None


def delete_command():
    with open("command.txt", "w") as f:
        f.write("")


