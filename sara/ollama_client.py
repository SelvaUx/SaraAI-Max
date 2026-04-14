"""
SaraAI Max — Ollama Client
Handles all communication with the local Ollama server.
"""

import json
import requests
from typing import Generator, Optional


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")

    def is_running(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list[str]:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            r.raise_for_status()
            data = r.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    def chat_stream(
        self,
        model: str,
        messages: list,
        tools: Optional[list] = None,
    ) -> Generator[dict, None, None]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools

        try:
            with requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
        except requests.exceptions.ConnectionError:
            yield {"error": "Cannot connect to Ollama. Is it running? Run: ollama serve"}
        except Exception as e:
            yield {"error": str(e)}

    def chat_sync(
        self,
        model: str,
        messages: list,
        tools: Optional[list] = None,
    ) -> dict:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools
        try:
            r = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120,
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to Ollama. Is it running? Run: ollama serve"}
        except Exception as e:
            return {"error": str(e)}

    def pull_model(self, model: str) -> Generator[str, None, None]:
        payload = {"name": model, "stream": True}
        try:
            with requests.post(
                f"{self.base_url}/api/pull",
                json=payload,
                stream=True,
                timeout=600,
            ) as resp:
                for line in resp.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            yield chunk.get("status", "")
                        except Exception:
                            continue
        except Exception as e:
            yield f"Error: {e}"
