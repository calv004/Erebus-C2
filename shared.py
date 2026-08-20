command = None

def set_command(cmd, uuid, sleep):
    with open(uuid, "w" ) as f:
        f.write(cmd + ";" + str(sleep))

def read_command(uuid):
    try:
        with open(uuid, "r") as f:
            content = f.read()
            return content if content != "" else None
    except FileNotFoundError:
        return None


def delete_command(uuid):
    with open(uuid, "w") as f:
        f.write("")


