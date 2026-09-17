# Erebus C2 Framework

```
███████╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝
█████╗  ██████╔╝█████╗  ██████╔╝██║   ██║███████╗
██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║
███████╗██║  ██║███████╗██████╔╝╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝
                    C 2  F R A M E W O R K
```

A lightweight Python-based Command &amp; Control framework for authorized penetration testing and security research. Erebus provides a CLI operator console and a Flask-backed HTTPS listener for managing remote agents.

> **Legal notice:** This tool is intended exclusively for authorized penetration testing, red team exercises, and educational research. You must have explicit written permission from the system owner before deploying any component of this framework. Unauthorized use against systems you do not own or have permission to test is illegal. The author assumes no liability for misuse.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Operator (main.py)                             │
│  ┌──────────────┐     ┌───────────────────────┐ │
│  │  CLI Console │────▶│  server_controlling   │ │
│  └──────┬───────┘     └──────────┬────────────┘ │
│         │                        │ subprocess    │
│         │ shared.py (file IPC)   ▼               │
│         │             ┌──────────────────────┐   │
│         └────────────▶│  server.py (Flask)   │   │
│                        └──────────┬───────────┘   │
└───────────────────────────────────┼───────────────┘
                                    │ HTTPS
                              ┌─────▼──────┐
                              │   Agent(s) │
                              └────────────┘
```

| Component | File | Purpose |
|---|---|---|
| CLI Console | `main.py` | Operator REPL — sends commands, manages agents |
| C2 Listener | `server.py` | Flask HTTPS server — handles agent registration and tasking |
| Process Manager | `server_controlling.py` | Spawns and terminates the Flask subprocess |
| Command Bus | `shared.py` | File-based IPC between the console and listener |

---

## Requirements

- Python 3.10+
- Flask
- Requests
- urllib3
- A self-signed TLS certificate (`local.crt` / `local.key`) for the listener

```bash
pip install flask requests urllib3
```

Generate a self-signed cert for local testing:

```bash
openssl req -x509 -newkey rsa:4096 -keyout local.key -out local.crt -days 365 -nodes \
  -subj "/CN=localhost"
```

---

## Configuration File

The operator console reads a plain-text config file on startup. Create one before running:

```
server: 127.0.0.1
port: 5000
sleep: 5
register_url: /register
command_url: /command
base_url: /erebus
```

| Key | Description |
|---|---|
| `server` | IP or hostname of the C2 listener |
| `port` | Port the Flask listener binds to |
| `sleep` | Default agent polling interval (seconds) |
| `register_url` | Endpoint path agents use to register |
| `command_url` | Endpoint path agents poll for tasks |
| `base_url` | URL prefix for all API routes |

---

## Usage

### Start the operator console

```bash
python main.py config.txt
```

You will land in the interactive REPL:

```
command>:
```

### Console commands

| Command | Description |
|---|---|
| `start` | Launch the Flask C2 listener as a subprocess |
| `stop` | Terminate the Flask listener |
| `list` | List all registered agents and their source IPs |
| `use agent` | Set the active agent by UUID |
| `command` | Send a shell command to the active agent |
| `command_output` | Retrieve output from an agent |
| `sleep` | Override the agent sleep interval |
| `generate agent` | Render an agent template with current server config |
| `help` | Print command reference |
| `exit` | Exit the console |

### Typical operator workflow

```
command>: start
Flask Server started

command>: list
1234-5678-9012-3456: {'ip': '192.168.1.50'}

command>: use agent
Enter Agent UUID: 1234-5678-9012-3456

command>: command
Which cmd should be executed: whoami

command>: command_output
Enter Agent UUID: 1234-5678-9012-3456
desktop-abc\calvin
```

---

## API Reference

All routes are served over HTTPS. The `{base_url}` prefix comes from the config.

| Method | Route | Auth | Description |
|---|---|---|---|
| `GET` | `/` | None | Health check — returns `"Erebus C2 is Online !"` |
| `GET` | `/{base_url}/{register_url}` | None | Register a new agent — returns a UUID |
| `GET` | `/{base_url}/{agent_guid}` | None | Verify an agent is registered |
| `GET` | `/{base_url}/{agent_guid}{command_url}` | None | Poll for a pending command |
| `POST` | `/{base_url}/{agent_guid}/output` | None | Submit command output (body = raw text) |
| `GET` | `/{base_url}/{agent_guid}/output` | None | Retrieve last command output |
| `GET` | `/{base_url}/list` | `X-Auth-ID: MyErebusToken` | Return all registered agents as JSON |

### Agent lifecycle

1. Agent calls `GET /{base_url}/{register_url}` → receives UUID
2. Agent polls `GET /{base_url}/{agent_guid}{command_url}` on the configured sleep interval
3. When a command is pending, the server returns it and clears it
4. Agent executes the command, then `POST`s output to `/{base_url}/{agent_guid}/output`

---

## Agent Template

The `generate agent` command reads a C source template and replaces the following placeholders before writing `generate.c`:

| Placeholder | Replaced with |
|---|---|
| `{{SERVER}}` | `server` from config |
| `{{PORT}}` | `port` from config |
| `{{AGENT}}` | `base_url` from config |
| `{{SLEEP}}` | current sleep value |
| `{{REGISTER}}` | `register_url` from config |
| `{{COMMAND}}` | `command_url` from config |

---

## Project Structure

```
Erebus-C2/
├── main.py                  # Operator CLI entry point
├── server.py                # Flask C2 listener
├── server_controlling.py    # Subprocess lifecycle manager
├── shared.py                # File-based command IPC
├── config.txt               # Your server config (not committed)
├── local.crt                # TLS certificate (not committed)
└── local.key                # TLS private key (not committed)
```

---

## Roadmap

- [ ] **Crystal Palace** — shellcode compilation utility for generating position-independent payloads
- [ ] Encrypted agent communications
- [ ] BOF Integration
- [ ] Command output collection improvements


---

## Disclaimer

This project is for **educational and authorized security research purposes only**. Obtain explicit written authorization before testing any system you do not own. The author is not responsible for any unlawful use of this software.
