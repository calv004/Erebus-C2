# ███████╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗
# ██╔════╝██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
# █████╗  ██████╔╝█████╗  ██████╔╝██║   ██║███████╗
# ██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║
# ███████╗██║  ██║███████╗██████╔╝╚██████╔╝███████║
# ╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝
#                   C2 FRAMEWORK

---

> **"From the depths, control begins."**

Erebus is a lightweight Command & Control (C2) Framework written in Python. It provides a simple CLI-driven interface to manage a Flask-based C2 server and communicate with remote agents.

---

## ⚠️ Disclaimer

This project is intended **for educational purposes and authorized penetration testing only.**
Do not use Erebus against systems you do not own or have explicit written permission to test.
The author takes no responsibility for any misuse of this tool.

---

## 🗂️ Project Structure

```
Erebus-C2/
├── main.py               # CLI interface & main entry point
├── server.py             # Flask C2 server
├── server_controlling.py # Server start/stop control via subprocess
├── shared.py             # Shared command file bridge
└── README.md
```

---

## ⚙️ Features

- CLI-driven interface with ASCII banner
- Flask-based HTTP C2 server
- Agent registration with unique UUID
- Command dispatching to agents via HTTP
- Clean start/stop server control
- Modular and extensible project structure

---

## 🚀 Installation

**Requirements:**
- Python 3.10+
- pip

**Install dependencies:**
```bash
pip install flask requests
```

---

## 🖥️ Usage

Start Erebus:
```bash
python main.py
```

**Available CLI commands:**

| Command   | Description                        |
|-----------|------------------------------------|
| `start`   | Start the Flask C2 server          |
| `stop`    | Stop the Flask C2 server           |
| `command` | Send a command to an active agent  |
| `list`    | List all registered agents         |
| `help`    | Show available commands            |
| `exit`    | Exit Erebus                        |

---

## 🌐 API Endpoints

| Method | Endpoint                        | Description                        |
|--------|---------------------------------|------------------------------------|
| GET    | `/`                             | Server status check                |
| GET    | `/agent/register`               | Register a new agent, returns UUID |
| GET    | `/agent/<agent_guid>`           | Check if agent is registered       |
| GET    | `/agent/<agent_guid>/command`   | Agent polls for pending command    |

---

## 🤖 Agent Flow

This is just an idea. It will be developed in near future.
```
1. Agent starts on target system
2. Agent sends GET /agent/register → receives unique UUID
3. Agent polls GET /agent/<uuid>/command in a loop
4. Operator sends command via CLI → agent receives and executes it
5. Agent returns output (future feature)

```

## 🛣️ Roadmap

- [ ] Agent for Windows written in C
- [ ] Multiple concurrent agent support
- [ ] Encrypted communication (HTTPS / AES)
- [ ] Agent sleep interval control
- [ ] Persistence mechanisms
