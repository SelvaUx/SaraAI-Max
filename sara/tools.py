"""
SaraAI Max — Tool Registry
All built-in tools: file ops, shell, web, apps, system, etc.
"""

import os
import sys
import json
import math
import platform
import subprocess
import datetime
from pathlib import Path
from typing import Any


# ─── Tool Registry ────────────────────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file from disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative path to the file."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates the file if it doesn't exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file."},
                    "content": {"type": "string", "description": "Content to write."},
                    "mode": {"type": "string", "description": "'w' to overwrite (default) or 'a' to append.", "enum": ["w", "a"]},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for files matching a pattern in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Directory to search in."},
                    "pattern": {"type": "string", "description": "Glob pattern like '*.py' or '*.txt'."},
                    "recursive": {"type": "boolean", "description": "Search recursively. Default true."},
                },
                "required": ["directory", "pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell/terminal command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run."},
                    "cwd": {"type": "string", "description": "Working directory for the command."},
                    "timeout": {"type": "integer", "description": "Timeout in seconds. Default 30."},
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for current information using DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query."},
                    "max_results": {"type": "integer", "description": "Max results to return. Default 5."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "wikipedia",
            "description": "Look up a topic on Wikipedia and get a summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic to look up."},
                    "sentences": {"type": "integer", "description": "Number of sentences. Default 5."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open/launch an application on Windows by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "App name e.g. 'notepad', 'chrome', 'vscode', 'spotify'."},
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_sysinfo",
            "description": "Get system information: OS, CPU, RAM, disk, Python version.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression e.g. '2**10 + sqrt(144)'. STRICT RULE: use ** for exponentiation, absolutely never use ^."},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Take a screenshot and save it to disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Save path. Default: Desktop/sara_screenshot.png"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_datetime",
            "description": "Get the current date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_processes",
            "description": "List currently running processes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "description": "Filter by process name (optional)."},
                },
            },
        },
    },
]


# ─── Tool Implementations ─────────────────────────────────────────────────────

def read_file(path: str) -> str:
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"Error: File not found: {path}"
        if p.stat().st_size > 2 * 1024 * 1024:  # 2MB limit
            return f"Error: File too large (>{2}MB). Use a specific line range."
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str, mode: str = "w") -> str:
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, mode, encoding="utf-8") as f:
            f.write(content)
        action = "appended to" if mode == "a" else "written to"
        return f"✓ Successfully {action} {p} ({len(content)} chars)"
    except Exception as e:
        return f"Error writing file: {e}"


def search_files(directory: str, pattern: str, recursive: bool = True) -> str:
    try:
        d = Path(directory).expanduser().resolve()
        if not d.exists():
            return f"Error: Directory not found: {directory}"
        if recursive:
            matches = list(d.rglob(pattern))
        else:
            matches = list(d.glob(pattern))
        if not matches:
            return f"No files matching '{pattern}' in {directory}"
        lines = [f"Found {len(matches)} file(s):"]
        for m in matches[:50]:  # cap at 50
            lines.append(f"  {m}")
        if len(matches) > 50:
            lines.append(f"  ... and {len(matches) - 50} more")
        return "\n".join(lines)
    except Exception as e:
        return f"Error searching files: {e}"


def run_command(command: str, cwd: str = None, timeout: int = 30) -> str:
    try:
        is_windows = platform.system() == "Windows"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            encoding="utf-8",
            errors="replace",
        )
        output = []
        if result.stdout.strip():
            output.append(result.stdout.strip())
        if result.stderr.strip():
            output.append(f"[stderr]\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"[exit code: {result.returncode}]")
        return "\n".join(output) if output else "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout}s"
    except Exception as e:
        return f"Error running command: {e}"


def web_search(query: str, max_results: int = 5) -> str:
    try:
        import urllib.request
        import urllib.parse
        import re

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Extract results from DuckDuckGo HTML
        results = []
        # Find result titles and snippets
        title_pattern = re.compile(r'class="result__title"[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)
        snippet_pattern = re.compile(r'class="result__snippet"[^>]*>(.*?)</div>', re.DOTALL)

        titles = title_pattern.findall(html)
        snippets = snippet_pattern.findall(html)

        clean = re.compile(r'<[^>]+>')
        for i, (url_found, title) in enumerate(titles[:max_results]):
            t = clean.sub('', title).strip()
            s = clean.sub('', snippets[i]).strip() if i < len(snippets) else ""
            results.append(f"{i+1}. {t}\n   {s}\n   URL: {url_found}")

        if not results:
            return f"No results found for: {query}"
        return f"Search results for '{query}':\n\n" + "\n\n".join(results)

    except Exception as e:
        return f"Web search error: {e}. (Tip: install requests for better search)"


def wikipedia(query: str, sentences: int = 5) -> str:
    try:
        import urllib.request
        import urllib.parse
        import json

        # Use Wikipedia API
        params = urllib.parse.urlencode({
            "action": "query",
            "format": "json",
            "titles": query,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "exsentences": sentences,
        })
        url = f"https://en.wikipedia.org/w/api.php?{params}"
        headers = {"User-Agent": "SaraAI Max"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                return f"Wikipedia: No article found for '{query}'"
            title = page.get("title", query)
            extract = page.get("extract", "No content available.")
            return f"**{title}** (Wikipedia)\n\n{extract}"
        return "Wikipedia: No results found."
    except Exception as e:
        return f"Wikipedia error: {e}"


APP_MAP = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "taskmgr": "taskmgr.exe",
    "control panel": "control.exe",
    "settings": "ms-settings:",
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "vscode": "code",
    "vs code": "code",
    "spotify": "spotify",
    "discord": "discord",
    "telegram": "telegram",
    "whatsapp": "whatsapp",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "vlc": "vlc",
}

def open_app(name: str) -> str:
    try:
        key = name.lower().strip()
        cmd = APP_MAP.get(key, key)

        if platform.system() == "Windows":
            if cmd.startswith("ms-"):
                subprocess.Popen(["start", "", cmd], shell=True)
            else:
                # Try Windows Search first (like v4.0)
                subprocess.Popen(
                    f'start "" "{cmd}"',
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            subprocess.Popen([cmd])

        return f"✓ Launched: {name}"
    except Exception as e:
        return f"Error launching '{name}': {e}"


def get_sysinfo(**kwargs) -> str:
    try:
        import shutil
        info = {
            "OS": f"{platform.system()} {platform.version()}",
            "Machine": platform.machine(),
            "Processor": platform.processor() or "Unknown",
            "Python": platform.python_version(),
            "Hostname": platform.node(),
        }
        try:
            import psutil
            mem = psutil.virtual_memory()
            info["RAM"] = f"{mem.total // (1024**3)}GB total, {mem.available // (1024**3)}GB free"
            disk = psutil.disk_usage("/")
            info["Disk"] = f"{disk.total // (1024**3)}GB total, {disk.free // (1024**3)}GB free"
            info["CPU Cores"] = str(psutil.cpu_count(logical=True))
            info["CPU Usage"] = f"{psutil.cpu_percent(interval=0.5)}%"
        except ImportError:
            pass

        lines = ["System Information:"]
        for k, v in info.items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error getting system info: {e}"


def calculate(expression: str, **kwargs) -> str:
    try:
        # Replace hallucinated caret exponentiation
        expression = expression.replace("^", "**")
        
        # Safe eval with math functions
        safe_env = {
            "__builtins__": {},
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow,
        }
        for name in dir(math):
            if not name.startswith("_"):
                safe_env[name] = getattr(math, name)

        result = eval(expression, safe_env)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Calculation error: {e}"


def take_screenshot(path: str = None, **kwargs) -> str:
    try:
        import pyautogui
        if path is None:
            desktop = Path.home() / "Desktop"
            desktop.mkdir(exist_ok=True)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = str(desktop / f"sara_screenshot_{ts}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f"✓ Screenshot saved: {path}"
    except ImportError:
        return "Error: pyautogui not installed. Run: pip install pyautogui"
    except Exception as e:
        return f"Screenshot error: {e}"


def get_datetime(**kwargs) -> str:
    now = datetime.datetime.now()
    return (
        f"Date: {now.strftime('%A, %B %d, %Y')}\n"
        f"Time: {now.strftime('%I:%M:%S %p')}\n"
        f"Timestamp: {now.isoformat()}"
    )


def list_processes(filter: str = None) -> str:
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "status"]):
            name = p.info["name"] or ""
            if filter and filter.lower() not in name.lower():
                continue
            procs.append(f"  PID {p.info['pid']:6d}  {name}")
        if not procs:
            return f"No processes found matching '{filter}'" if filter else "No processes found."
        return f"Running processes ({len(procs)}):\n" + "\n".join(procs[:50])
    except ImportError:
        # Fallback using tasklist (Windows)
        cmd = f"tasklist /FI \"IMAGENAME eq *{filter}*\"" if filter else "tasklist"
        return run_command(cmd, timeout=10)
    except Exception as e:
        return f"Error listing processes: {e}"


# ─── Dispatcher ───────────────────────────────────────────────────────────────

TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
    "run_command": run_command,
    "web_search": web_search,
    "wikipedia": wikipedia,
    "open_app": open_app,
    "get_sysinfo": get_sysinfo,
    "calculate": calculate,
    "take_screenshot": take_screenshot,
    "get_datetime": get_datetime,
    "list_processes": list_processes,
}


def call_tool(name: str, args: dict) -> str:
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return f"Unknown tool: {name}"
    try:
        return func(**args)
    except TypeError as e:
        return f"Tool argument error ({name}): {e}"
    except Exception as e:
        return f"Tool execution error ({name}): {e}"
