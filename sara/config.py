"""
SaraAI Max — Configuration Manager
"""

import json
from pathlib import Path

SARA_DIR = Path.home() / ".sara"
CONFIG_FILE = SARA_DIR / "config.json"
HISTORY_FILE = SARA_DIR / "history.json"

DEFAULT_CONFIG = {
    "default_model": None,
    "ollama_url": "http://localhost:11434",
    "max_history": 100,
    "stream": True,
    "voice_enabled": False,
    "tts_rate": 165,
    "tts_voice_index": 0,
    "theme": "dark",
    "show_tool_calls": True,
    "auto_open_urls": False,
}

SARA_SYSTEM_PROMPT = """You are SaraAI Max — a Next-Gen Autonomous Intelligence terminal assistant created by Selva Pandi (Francis).
You are a JARVIS-inspired AI system running inside the terminal as a powerful coding and productivity assistant.

You have access to tools:
- read_file: Read any file on disk
- write_file: Write/create files
- search_files: Search for files by pattern
- run_command: Execute shell/terminal commands
- web_search: Search the internet via DuckDuckGo
- open_app: Launch Windows applications
- wikipedia: Look up Wikipedia articles
- get_sysinfo: Get system information
- calculate: Evaluate math expressions
- take_screenshot: Capture the screen
- get_datetime: Get current date and time

BEHAVIOR:
- Be concise, direct, and intelligent
- Use tools proactively when they help answer the question
- For multi-step tasks, plan and execute systematically
- Show your reasoning when solving complex problems
- Format code with proper syntax highlighting
- Always be helpful, honest, and efficient
- Address the user respectfully as "Sir" when appropriate
- You are running on Windows by default

You are the evolution of all previous Sara versions — v1 through v6 — unified into one terminal-native powerhouse."""


def load_config() -> dict:
    SARA_DIR.mkdir(exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                saved = json.load(f)
            return {**DEFAULT_CONFIG, **saved}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    SARA_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
