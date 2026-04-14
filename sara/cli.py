"""
SaraAI Max — Main CLI Entry Point
The OpenCode / Claude Code style terminal interface.

Usage:
    sara                        # Interactive mode
    sara "your question"        # One-shot query
    sara --voice                # Voice mode
    sara --model llama3.2       # Specific model
    sara --list-models          # Show models
    sara --version              # Show version
"""

import sys
import os
import argparse
from pathlib import Path

# Make sure sara package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from sara.ollama_client import OllamaClient
from sara.memory import Memory
from sara.agent import SaraAgent
from sara.config import load_config, save_config
from sara import ui

try:
    from sara.voice import VoiceHandler
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


# ─── Slash Command Handler ─────────────────────────────────────────────────────

def handle_slash_command(
    cmd: str,
    agent: SaraAgent,
    memory: Memory,
    config: dict,
    ollama: OllamaClient,
    models: list[str],
    voice_handler,
) -> str | None:
    """
    Handle /commands. Returns "exit" to quit, "continue" to keep running,
    or None if not a slash command.
    """
    cmd = cmd.strip()
    if not cmd.startswith("/"):
        return None

    parts = cmd.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if command in ("/exit", "/quit", "/q"):
        memory.save()
        ui.print_info("Session saved. Goodbye, sir! 👋")
        return "exit"

    elif command == "/help":
        ui.print_help()
        return "continue"

    elif command == "/clear":
        os.system("cls" if os.name == "nt" else "clear")
        ui.print_banner(agent.model, animate=False)
        return "continue"

    elif command == "/reset":
        memory.clear()
        ui.print_success("Conversation memory cleared.")
        return "continue"

    elif command == "/history":
        stats = memory.get_stats()
        ui.print_info(
            f"Messages: {stats['total']} total  ({stats['user']} from you, {stats['sara']} from Sara)"
        )
        return "continue"

    elif command == "/save":
        path = args.strip() or str(Path.home() / "sara_conversation.txt")
        try:
            memory.export(path)
            ui.print_success(f"Conversation saved to: {path}")
        except Exception as e:
            ui.print_error(f"Save failed: {e}")
        return "continue"

    elif command == "/models":
        refreshed = ollama.list_models()
        ui.print_model_list(refreshed)
        return "continue"

    elif command == "/model":
        if not args:
            ui.print_info(f"Current model: {agent.model}")
            return "continue"
        # Select by number or name
        refreshed = ollama.list_models()
        if args.isdigit():
            idx = int(args) - 1
            if 0 <= idx < len(refreshed):
                new_model = refreshed[idx]
            else:
                ui.print_error(f"Invalid model number. Use /models to see list.")
                return "continue"
        else:
            matches = [m for m in refreshed if args.lower() in m.lower()]
            if not matches:
                ui.print_error(f"No model matching '{args}'. Use /models to see list.")
                return "continue"
            new_model = matches[0]
        agent.model = new_model
        agent._uses_native_tools = None
        config["default_model"] = new_model
        save_config(config)
        ui.print_success(f"Switched to model: {new_model}")
        return "continue"

    elif command == "/tools":
        ui.print_tools_list()
        return "continue"

    elif command == "/voice":
        arg = args.strip().lower()
        if not VOICE_AVAILABLE:
            ui.print_error("Voice not available. Install: pip install pyttsx3 SpeechRecognition pyaudio")
            return "continue"
        if arg == "on":
            config["voice_enabled"] = True
            save_config(config)
            ui.print_success("Voice mode ON. Sara will speak her responses.")
        elif arg == "off":
            config["voice_enabled"] = False
            save_config(config)
            ui.print_success("Voice mode OFF.")
        else:
            status = "ON" if config.get("voice_enabled") else "OFF"
            ui.print_info(f"Voice mode is {status}. Use /voice on or /voice off.")
        return "continue"

    elif command == "/config":
        import json
        from rich.syntax import Syntax
        from sara.ui import console
        cfg_str = json.dumps({k: v for k, v in config.items()}, indent=2)
        syntax = Syntax(cfg_str, "json", theme="monokai", line_numbers=False)
        console.print(syntax)
        return "continue"

    elif command == "/sysinfo":
        from sara.tools import get_sysinfo
        info = get_sysinfo()
        ui.print_info(info)
        return "continue"

    else:
        ui.print_error(f"Unknown command: {command}. Type /help for available commands.")
        return "continue"


# ─── Main Loop ─────────────────────────────────────────────────────────────────

def run_interactive(agent: SaraAgent, memory: Memory, config: dict, ollama: OllamaClient,
                    models: list[str], voice_handler, voice_mode: bool):
    """Main interactive REPL loop."""
    ui.print_banner(agent.model, animate=True)

    while True:
        try:
            if voice_mode and voice_handler and voice_handler.available:
                ui.print_info("🎙  Listening... (say your command)")
                user_input = voice_handler.listen()
                if user_input:
                    ui.console.print(f"\n[sara.user_prompt]You ›[/sara.user_prompt] [white]{user_input}[/white]")
                else:
                    ui.print_error("Didn't catch that. Try again.")
                    continue
            else:
                user_input = ui.get_user_input()

            if not user_input:
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                result = handle_slash_command(
                    user_input, agent, memory, config, ollama, models, voice_handler
                )
                if result == "exit":
                    break
                continue

            # Regular chat
            response = agent.chat(user_input)

            # Voice output
            if voice_mode and voice_handler and voice_handler.available and response:
                voice_handler.speak(response)

        except KeyboardInterrupt:
            ui.console.print()
            ui.print_info("Interrupted. Type /exit to quit or continue chatting.")
            continue
        except EOFError:
            break

    memory.save()


def main():
    parser = argparse.ArgumentParser(
        prog="sara",
        description="SaraAI Max — Terminal Intelligence by Selva Pandi",
    )
    parser.add_argument("query", nargs="?", help="One-shot query (optional)")
    parser.add_argument("--model", "-m", help="Ollama model to use")
    parser.add_argument("--voice", action="store_true", help="Enable voice mode")
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--no-tools", action="store_true", help="Disable tool use")
    parser.add_argument("--url", default=None, help="Ollama server URL (default: http://localhost:11434)")
    args = parser.parse_args()

    if args.version:
        print("SaraAI Max v1.0.0 — Next-Gen Autonomous Intelligence — by Selva Pandi (SelvaUx)")
        sys.exit(0)

    config = load_config()
    if args.url:
        config["ollama_url"] = args.url

    ollama = OllamaClient(config["ollama_url"])

    # Check Ollama
    if not ollama.is_running():
        from rich.console import Console
        c = Console()
        c.print("\n[bold red]✗ Ollama is not running![/bold red]")
        c.print("[dim]Start it with:[/dim] [bold white]ollama serve[/bold white]\n")
        sys.exit(1)

    # List models flag
    models = ollama.list_models()

    if args.list_models:
        ui.print_model_list(models)
        sys.exit(0)

    # No models installed
    if not models:
        from rich.console import Console
        c = Console()
        c.print("\n[bold red]✗ No models installed![/bold red]")
        c.print("[dim]Install one with:[/dim] [bold white]ollama pull llama3.2[/bold white]\n")
        sys.exit(1)

    # Resolve model
    if args.model:
        model = args.model
    elif config.get("default_model") and config["default_model"] in models:
        model = config["default_model"]
    else:
        # Auto-select best installed model to avoid interactive prompt crash when used non-interactively
        preferred = ["llama3.2:latest", "llama3.2", "llama3.1:latest", "llama3.1", "mistral:latest", "mistral", "qwen2.5"]
        selected = next((p for p in preferred if p in models), models[0])
        model = selected
        config["default_model"] = model
        save_config(config)

    # Setup
    memory = Memory(config.get("max_history", 100))

    voice_handler = None
    if (args.voice or config.get("voice_enabled")) and VOICE_AVAILABLE:
        voice_handler = VoiceHandler(
            tts_rate=config.get("tts_rate", 165),
            voice_index=config.get("tts_voice_index", 0),
        )
        if not voice_handler.available:
            ui.print_error("Voice libraries not fully installed. Run: pip install pyttsx3 SpeechRecognition pyaudio")
            voice_handler = None

    agent = SaraAgent(
        ollama=ollama,
        memory=memory,
        model=model,
        stream=config.get("stream", True),
        show_tool_calls=config.get("show_tool_calls", True),
    )

    if args.no_tools:
        from sara import tools as t_module
        t_module.TOOL_DEFINITIONS.clear()

    voice_mode = args.voice or config.get("voice_enabled", False)

    # One-shot mode
    if args.query:
        agent.chat(args.query)
        memory.save()
        return

    # Interactive loop
    run_interactive(agent, memory, config, ollama, models, voice_handler, voice_mode)


if __name__ == "__main__":
    main()
