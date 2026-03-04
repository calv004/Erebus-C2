import subprocess
import sys

process = None

def start():
    global process

    if process and process.poll() is None:
        print("Flask Server already running")
    else:
        process = subprocess.Popen(["python", "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Flask Server started")

def stop():
    global process
    if process and process.poll() is None:
        process.terminate()
        print("[*] Server stopped")
    else:
        print("[!] Server is not running")

