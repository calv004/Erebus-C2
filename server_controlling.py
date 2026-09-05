import subprocess
import sys
import time

process = None

def start(register_url, command_url, base_url, port_config):
    global process

    if process and process.poll() is None:
        print("Flask Server already running")
    else:
        process = subprocess.Popen(
            [sys.executable, "server.py", register_url, command_url, base_url, port_config],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)

        if process.poll() is None:
            print("Flask Server started")
        else:
            print("Flask Server failed to start:")
            print(process.stderr.read().decode())

def stop():
    global process
    if process and process.poll() is None:
        process.terminate()
        print("Server stopped")
    else:
        print("Server is not running")