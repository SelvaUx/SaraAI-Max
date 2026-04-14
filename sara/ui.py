"""
SaraAI Max — Terminal UI
Rich-powered CLI interface with animated startup sequence.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.rule import Rule
from rich import box
from rich.theme import Theme
from rich.live import Live
from rich.align import Align
import re
import time
import sys
import random

SARA_THEME = Theme({
    "sara.banner": "bold cyan",
    "sara.user_prompt": "bold green",
    "sara.sara_prompt": "bold cyan",
    "sara.tool_name": "bold yellow",
    "sara.tool_result": "dim white",
    "sara.error": "bold red",
    "sara.success": "bold green",
    "sara.info": "dim cyan",
    "sara.model": "magenta",
    "sara.slash": "bold yellow",
})

console = Console(theme=SARA_THEME, highlight=True)


BANNER = r"""
   ███████╗ █████╗ ██████╗  █████╗      ███╗   ███╗ █████╗ ██╗  ██╗
   ██╔════╝██╔══██╗██╔══██╗██╔══██╗     ████╗ ████║██╔══██╗╚██╗██╔╝
   ███████╗███████║██████╔╝███████║     ██╔████╔██║███████║ ╚███╔╝ 
   ╚════██║██╔══██║██╔══██╗██╔══██║     ██║╚██╔╝██║██╔══██║ ██╔██╗ 
   ███████║██║  ██║██║  ██║██║  ██║     ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

SUBTITLE = "             S A R A   A I   M A X   (Selva.Ux)"

VERSION = "1.0.0"
TAGLINE = "Next-Gen Autonomous Intelligence"

# Gradient color palette for the animated banner
GRADIENT_COLORS = [
    "#00d4ff", "#00c8ff", "#00bcff", "#00b0ff", "#00a4ff",
    "#0098ff", "#008cff", "#0080ff", "#0074ff", "#0068ff",
    "#005cff", "#0050ff", "#6644ff", "#8833ff", "#aa22ff",
]


def _animate_typing(text: str, style: str = "bold cyan", delay: float = 0.008):
    """Type-writer effect for text output."""
    for char in text:
        console.print(f"[{style}]{char}[/{style}]", end="")
        sys.stdout.flush()
        time.sleep(delay)


def _animate_banner():
    """Animate the banner with a line-by-line reveal and gradient colors."""
    lines = BANNER.strip().splitlines()
    console.print()

    for i, line in enumerate(lines):
        color = GRADIENT_COLORS[i % len(GRADIENT_COLORS)]
        console.print(f"[{color}]{line}[/{color}]")
        time.sleep(0.06)

    # Animate the subtitle with a typing effect
    console.print()
    for char in SUBTITLE:
        if char == " ":
            console.print(" ", end="")
        else:
            console.print(f"[bold white]{char}[/bold white]", end="")
        sys.stdout.flush()
        time.sleep(0.025)
    console.print()


def _animate_loading():
    """Show a quick animated loading sequence at startup."""
    boot_steps = [
        ("⚡", "Initializing SaraAI Max core...", "bold cyan"),
        ("🧠", "Loading autonomous agent engine...", "bold magenta"),
        ("🔧", "Registering tool definitions...", "bold yellow"),
        ("🌐", "Connecting to Ollama backend...", "bold green"),
        ("✅", "All systems online.", "bold green"),
    ]

    console.print()
    for icon, msg, style in boot_steps:
        console.print(f"  [{style}]{icon} {msg}[/{style}]")
        time.sleep(0.25)
    console.print()


def _speak_welcome():
    """Speak 'Welcome back, Sir' using pyttsx3 in a background thread."""
    try:
        import pyttsx3
        import threading

        def _speak():
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 165)
                voices = engine.getProperty("voices")
                # Try to use a female/clear voice if available
                if voices and len(voices) > 1:
                    engine.setProperty("voice", voices[1].id)
                engine.say("Welcome back, Sir. SaraAI Max is online and ready.")
                engine.runAndWait()
            except Exception:
                pass

        t = threading.Thread(target=_speak, daemon=True)
        t.start()
    except ImportError:
        pass


def print_banner(model: str = "No model selected", animate: bool = True):
    """Print the startup banner. If animate=True, shows the full animated boot sequence."""
    if animate:
        _animate_banner()
        _animate_loading()
        _speak_welcome()
    else:
        console.print()
        console.print(f"[bold cyan]{BANNER}[/bold cyan]", end="")

    console.print(
        Panel(
            f"[bold white]SaraAI Max[/bold white]  ·  "
            f"[sara.model]{model}[/sara.model]  ·  "
            f"[dim]{TAGLINE}[/dim]\n"
            f"[dim]Type [/dim][sara.slash]/help[/sara.slash][dim] for commands · "
            f"[/dim][sara.slash]/exit[/sara.slash][dim] to quit[/dim]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    console.print()


def print_model_list(models: list[str]) -> str:
    if not models:
        console.print("[sara.error]No Ollama models found. Run: ollama pull llama3.2[/sara.error]")
        return None

    table = Table(
        title="[bold cyan]Available Models[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold white",
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Model Name", style="bold white")
    table.add_column("Tag", style="magenta")

    for i, m in enumerate(models, 1):
        parts = m.split(":")
        name = parts[0]
        tag = parts[1] if len(parts) > 1 else "latest"
        table.add_row(str(i), name, tag)

    console.print(table)
    return None


def print_help():
    table = Table(
        title="[bold cyan]Sara Commands[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold white",
    )
    table.add_column("Command", style="bold yellow", min_width=20)
    table.add_column("Description", style="white")

    commands = [
        ("/help", "Show this help menu"),
        ("/clear", "Clear the screen"),
        ("/history", "Show conversation history stats"),
        ("/save", "Save conversation to file"),
        ("/models", "List available Ollama models"),
        ("/model <name>", "Switch to a different model"),
        ("/tools", "List all available tools"),
        ("/voice on|off", "Toggle voice I/O"),
        ("/config", "Show current configuration"),
        ("/reset", "Clear conversation memory"),
        ("/sysinfo", "Show system information"),
        ("/exit or /quit", "Exit SaraAI Max"),
    ]
    for cmd, desc in commands:
        table.add_row(cmd, desc)

    console.print()
    console.print(table)
    console.print()


def print_tools_list():
    from .tools import TOOL_DEFINITIONS
    table = Table(
        title="[bold cyan]Available Tools[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold white",
    )
    table.add_column("Tool", style="bold yellow", min_width=18)
    table.add_column("Description", style="white")

    for t in TOOL_DEFINITIONS:
        fn = t["function"]
        table.add_row(fn["name"], fn["description"])

    console.print()
    console.print(table)
    console.print()


def print_user_message(text: str):
    console.print()
    console.print(f"[sara.user_prompt]You ›[/sara.user_prompt] [white]{text}[/white]")


def print_sara_prefix():
    console.print()
    console.print(f"[sara.sara_prompt]Sara ›[/sara.sara_prompt] ", end="")


def print_tool_call(tool_name: str, args: dict):
    args_str = ", ".join(f"{k}={repr(v)[:40]}" for k, v in args.items())
    console.print()
    console.print(
        f"  [sara.tool_name]⚙ Tool:[/sara.tool_name] [bold white]{tool_name}[/bold white]"
        f"[dim]({args_str})[/dim]"
    )


def print_tool_result(result: str, tool_name: str = ""):
    lines = result.strip().split("\n")
    preview = lines[0][:120] + ("..." if len(result) > 120 else "")
    console.print(f"  [dim]  └─ {preview}[/dim]")


def print_streaming_token(token: str):
    console.print(token, end="", highlight=False)


def print_response_end():
    console.print()


def print_error(msg: str):
    console.print()
    console.print(f"[sara.error]✗ {msg}[/sara.error]")
    console.print()


def print_info(msg: str):
    console.print(f"[sara.info]ℹ {msg}[/sara.info]")


def print_success(msg: str):
    console.print(f"[sara.success]✓ {msg}[/sara.success]")


def print_separator():
    console.print(Rule(style="dim"))


def render_markdown(text: str):
    try:
        md = Markdown(text)
        console.print(md)
    except Exception:
        console.print(text)


def prompt_model_selection(models: list[str]) -> str:
    print_model_list(models)
    while True:
        try:
            choice = console.input(
                "\n[bold cyan]Select model[/bold cyan] [dim](number or name, Enter for 1)[/dim]: "
            ).strip()
            if not choice:
                return models[0]
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    return models[idx]
            elif choice in models:
                return choice
            else:
                # Check if partial match
                matches = [m for m in models if choice.lower() in m.lower()]
                if len(matches) == 1:
                    return matches[0]
            console.print("[sara.error]Invalid selection, try again.[/sara.error]")
        except (KeyboardInterrupt, EOFError):
            return models[0]


def get_user_input(voice_mode: bool = False) -> str | None:
    try:
        text = console.input("\n[sara.user_prompt]You ›[/sara.user_prompt] ").strip()
        return text if text else None
    except (KeyboardInterrupt, EOFError):
        return "/exit"
