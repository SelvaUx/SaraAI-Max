"""
SaraAI Max — Conversation Memory
Persistent chat history across sessions.
"""

import json
from datetime import datetime
from pathlib import Path
from .config import HISTORY_FILE, SARA_DIR


class Memory:
    def __init__(self, max_messages: int = 100):
        self.max_messages = max_messages
        self.messages: list = []
        self.session_start = datetime.now().isoformat()
        SARA_DIR.mkdir(exist_ok=True)

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            # Keep system context, trim oldest
            self.messages = self.messages[-self.max_messages:]

    def add_tool_result(self, tool_name: str, result: str):
        self.messages.append({
            "role": "tool",
            "content": result,
            "name": tool_name,
        })

    def get_messages(self) -> list:
        return self.messages.copy()

    def clear(self):
        self.messages = []

    def save(self):
        try:
            history = []
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE) as f:
                    history = json.load(f)
        except Exception:
            history = []

        session = {
            "timestamp": self.session_start,
            "messages": self.messages,
        }
        history.append(session)
        # Keep last 20 sessions
        history = history[-20:]

        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

    def load_last_session(self):
        try:
            if HISTORY_FILE.exists():
                with open(HISTORY_FILE) as f:
                    history = json.load(f)
                if history:
                    self.messages = history[-1]["messages"]
                    return True
        except Exception:
            pass
        return False

    def export(self, path: str):
        with open(path, "w") as f:
            for msg in self.messages:
                role = msg["role"].upper()
                content = msg["content"]
                f.write(f"[{role}]\n{content}\n\n")

    def get_stats(self) -> dict:
        user_msgs = sum(1 for m in self.messages if m["role"] == "user")
        sara_msgs = sum(1 for m in self.messages if m["role"] == "assistant")
        return {
            "total": len(self.messages),
            "user": user_msgs,
            "sara": sara_msgs,
        }
