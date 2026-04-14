# 🤖 SaraAI Max — Next-Gen Autonomous Intelligence

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()
[![Ollama](https://img.shields.io/badge/powered%20by-Ollama-orange.svg)]()
[![Status](https://img.shields.io/badge/status-online-brightgreen.svg)]()

> **The evolution is complete.** SaraAI Max is a JARVIS-inspired, terminal-native AI assistant powered by Ollama — designed to feel like Claude Code, built to think autonomously.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🖥️ **CLI-First Design** | Works exactly like Claude Code / OpenCode — rich terminal UI |
| 🦙 **Ollama Integration** | Auto-detects all installed local models, seamless switching |
| 🔧 **12 Built-in Tools** | File I/O, shell commands, web search, apps, system info, and more |
| 🧠 **Agentic Loop** | Sara autonomously chains tools to complete complex tasks |
| 🌊 **Streaming Responses** | Real-time token streaming with markdown rendering |
| 💾 **Persistent Memory** | Conversation history saved across sessions |
| 🎙️ **Voice I/O** | `--voice` flag enables full speech input/output |
| 🎬 **Animated Startup** | Gradient banner reveal + boot sequence + voice welcome |
| ⚡ **Global Install** | One `pip install -e .` → use `sara` from anywhere |

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+**
2. **Ollama** — [Download here](https://ollama.com/download)
3. **A local LLM** — `ollama pull llama3.2`

### Install

```bash
git clone https://github.com/SelvaUx/SaraAI.git
cd SaraAI/sara-ai-max

# Windows (recommended)
install.bat

# Manual Installation
pip install -e .
```

### Run

```bash
# Interactive mode (like Claude Code)
sara

# One-shot query
sara "explain neural networks"

# Voice mode
sara --voice

# Use a specific model
sara --model mistral

# List installed models
sara --list-models

# Show version
sara --version

# Show help
sara --help
```

---

## 🎬 Animated CLI Startup

When you launch `sara`, you'll see:

```
   ███████╗ █████╗ ██████╗  █████╗      ███╗   ███╗ █████╗ ██╗  ██╗
   ██╔════╝██╔══██╗██╔══██╗██╔══██╗     ████╗ ████║██╔══██╗╚██╗██╔╝
   ███████╗███████║██████╔╝███████║     ██╔████╔██║███████║ ╚███╔╝
   ╚════██║██╔══██║██╔══██╗██╔══██║     ██║╚██╔╝██║██╔══██║ ██╔██╗
   ███████║██║  ██║██║  ██║██║  ██║     ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

             S A R A   A I   M A X   (Selva.Ux)

  ⚡ Initializing SaraAI Max core...
  🧠 Loading autonomous agent engine...
  🔧 Registering tool definitions...
  🌐 Connecting to Ollama backend...
  ✅ All systems online.

╭──────────────────────────────────────────────────────╮
│  SaraAI Max  ·  llama3.2  ·  Next-Gen Autonomous    │
│  Intelligence                                        │
│  Type /help for commands · /exit to quit              │
╰──────────────────────────────────────────────────────╯

🎙 "Welcome back, Sir. SaraAI Max is online and ready."
```

**Startup features:**
- 🌈 Gradient color banner — each line fades from cyan to purple
- ⌨️ Typewriter effect on the subtitle
- ⚡ Animated boot sequence with status indicators
- 🔊 Voice greeting: *"Welcome back, Sir. SaraAI Max is online and ready."*

---

## 💡 Example Prompts & Use Cases

### 📝 Code — Read, Write, Debug
```bash
sara "Read my index.js file, find the bug in the sorting algorithm, and fix it."
sara "Create a Python script that scrapes headlines from Hacker News and saves them to headlines.md."
sara "Search my project for all .py files and tell me which one is the largest."
```

### 💻 System & OS Management
```bash
sara "List all the Python processes running on my machine right now."
sara "Check my system memory and CPU usage — do I have enough RAM to run a 7B model?"
sara "Open Notepad and create a blank document for me."
sara "Take a screenshot of my current screen."
```

### 🌍 Internet Research
```bash
sara "Search the web for the latest release notes of React 19 and summarize them."
sara "Look up 'Quantum Computing' on Wikipedia and explain it to me simply."
sara "What is the current date and time?"
```

### 🧮 Quick Calculations
```bash
sara "Calculate 2^32 - 1"
sara "What is the compound interest on 50000 at 8% for 5 years?"
```

### 🔄 Multi-Step Agentic Tasks
```bash
sara "Read my requirements.txt, check which packages are outdated, and create an updated version."
sara "Find all TODO comments in my codebase and compile them into a task list."
```

---

## 🧠 Model Selection & Memory Behavior

Sara dynamically controls which model gets loaded into memory based on her internal configuration (`~/.sara/config.json`). Because of this, stopping a model manually via `ollama stop` won't prevent Sara from using it—the next command you send will simply force Ollama to reload it instantly.

To permanently change Sara's brain to a different model, use one of these methods:

**Method 1: CLI Flag (On Boot)**
Start Sara and pass your target model. This will boot the session and save the new model as your persistent default.
```bash
sara --model tinyllama:latest
```

**Method 2: Slash Command (Hot-Swap)**
While chatting inside the terminal loop, you can swap models dynamically without restarting:
```text
You › /models
(Sara lists all local Ollama models)

You › /model tinyllama:latest
(Switches engine to tinyllama and saves it as the new default)
```

---

## 💬 CLI Commands (Inside Sara)

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/models` | List available Ollama models |
| `/model <n>` | Switch model by number or name |
| `/tools` | Show all built-in tools |
| `/clear` | Clear screen |
| `/reset` | Clear conversation memory |
| `/history` | Show conversation stats |
| `/save [path]` | Export conversation to file |
| `/voice on\|off` | Toggle voice mode |
| `/config` | Show current config |
| `/sysinfo` | System information |
| `/exit` | Quit Sara |

---

## 🔧 Built-in Tools

Sara can autonomously use these tools:

| Tool | Description |
|------|-------------|
| `read_file` | Read any file from disk |
| `write_file` | Create or edit files |
| `search_files` | Find files by glob pattern |
| `run_command` | Execute shell commands |
| `web_search` | DuckDuckGo internet search |
| `wikipedia` | Wikipedia article lookup |
| `open_app` | Launch Windows apps |
| `get_sysinfo` | System info (OS, RAM, CPU) |
| `calculate` | Math expression evaluator |
| `take_screenshot` | Screen capture |
| `get_datetime` | Current date and time |
| `list_processes` | Running process list |

---

## 📁 Project Structure

```
sara-ai-max/
├── sara/
│   ├── __init__.py         ← Package init + version
│   ├── cli.py              ← Main entry point & REPL
│   ├── agent.py            ← Agentic tool loop (native + ReAct)
│   ├── ollama_client.py    ← Ollama API client
│   ├── tools.py            ← All 12 built-in tools
│   ├── ui.py               ← Rich terminal UI + animated startup
│   ├── voice.py            ← Voice I/O (pyttsx3 + SpeechRecognition)
│   ├── memory.py           ← Conversation history manager
│   └── config.py           ← Config + system prompt
├── setup.py                ← pip installable (console_scripts)
├── requirements.txt
├── install.bat             ← Windows one-click installer
└── README.md
```

---

## ⚙️ Config

Config stored at `~/.sara/config.json`:

```json
{
  "default_model": "llama3.2",
  "ollama_url": "http://localhost:11434",
  "max_history": 100,
  "stream": true,
  "voice_enabled": false,
  "show_tool_calls": true
}
```

---

## 🔮 Sara Evolution

```
v1 → v2 → v2.5 → v3 → v4 → v5 → v6 → SaraAI Max (YOU ARE HERE)
Basic  Wake  Code   AI   C#   Multi  Electron  ██████████████
Voice  Word  Gen   LLM  WPF  Lang   Desktop    Next-Gen AI
```

---

## 👨‍💻 Developer Details

**Selva Pandi (Francis / SelvaUx)**

*Selva Pandi is an Electronics and Communication Engineering student with a strong passion for artificial intelligence and emerging technologies. He focuses on building real-world AI systems, including voice assistants and automation tools, and aims to create futuristic intelligent systems inspired by JARVIS.*

🎓 ECE @ Dr. G.U. Pope College of Engineering
💻 GitHub: [@SelvaUx](https://github.com/SelvaUx)

---

*SaraAI Max — "From a basic voice bot to a next-gen autonomous intelligence. The journey continues."*
