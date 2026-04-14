"""
SaraAI Max — Agent Core
Agentic loop: Ollama LLM + tool calling + streaming.
Supports both native tool-calling models and ReAct fallback.
"""

import json
import re
from typing import Generator

from .ollama_client import OllamaClient
from .memory import Memory
from .tools import TOOL_DEFINITIONS, call_tool
from .config import SARA_SYSTEM_PROMPT
from . import ui


REACT_SYSTEM_ADDON = """
When you need to use a tool, respond EXACTLY in this format:
<tool_call>
{"name": "tool_name", "arguments": {"key": "value"}}
</tool_call>

After getting the tool result, continue your response naturally.
Available tools: read_file, write_file, search_files, run_command, web_search, wikipedia, open_app, get_sysinfo, calculate, take_screenshot, get_datetime, list_processes
"""


class SaraAgent:
    def __init__(
        self,
        ollama: OllamaClient,
        memory: Memory,
        model: str,
        stream: bool = True,
        show_tool_calls: bool = True,
    ):
        self.ollama = ollama
        self.memory = memory
        self.model = model
        self.stream = stream
        self.show_tool_calls = show_tool_calls
        self._uses_native_tools = None  # auto-detect

    def _build_messages(self) -> list:
        system = {"role": "system", "content": SARA_SYSTEM_PROMPT}
        return [system] + self.memory.get_messages()

    def _detect_tool_support(self) -> bool:
        """Check if the model supports native tool calling."""
        # Models known to support tools
        native_tool_models = [
            "llama3.1", "llama3.2", "llama3.3",
            "mistral", "mistral-nemo", "mistral-large",
            "qwen2", "qwen2.5", "command-r",
            "firefunction", "nexusraven",
            "granite3", "granite-3",
        ]
        model_lower = self.model.lower()
        return any(m in model_lower for m in native_tool_models)

    def chat(self, user_input: str) -> str:
        """Main chat method - returns full response after tool loop."""
        self.memory.add("user", user_input)

        if self._uses_native_tools is None:
            self._uses_native_tools = self._detect_tool_support()

        if self._uses_native_tools:
            return self._chat_with_tools(user_input)
        else:
            return self._chat_react(user_input)

    def _chat_with_tools(self, user_input: str) -> str:
        """Native tool calling loop for supported models."""
        max_tool_rounds = 5
        full_response = ""

        for round_num in range(max_tool_rounds):
            messages = self._build_messages()

            if self.stream and round_num == 0:
                # Stream the first response
                ui.print_sara_prefix()
                response_text = ""
                tool_calls = []
                current_tool_call = None

                for chunk in self.ollama.chat_stream(self.model, messages, TOOL_DEFINITIONS):
                    if "error" in chunk:
                        ui.print_error(chunk["error"])
                        return chunk["error"]

                    msg = chunk.get("message", {})
                    delta_content = msg.get("content", "")
                    delta_tools = msg.get("tool_calls", [])

                    if delta_content:
                        response_text += delta_content
                        ui.print_streaming_token(delta_content)

                    if delta_tools:
                        tool_calls.extend(delta_tools)

                    if chunk.get("done"):
                        break

                ui.print_response_end()

                if not tool_calls:
                    self.memory.add("assistant", response_text)
                    full_response = response_text
                    break

                # Execute tool calls
                self.memory.add("assistant", response_text or "")
                tool_results = self._execute_tool_calls(tool_calls)

                # Add tool results to memory
                for tool_call, result in tool_results:
                    self.memory.add("tool", result)

                full_response = response_text

            else:
                # Non-streaming or follow-up rounds
                resp = self.ollama.chat_sync(self.model, messages, TOOL_DEFINITIONS)
                if "error" in resp:
                    ui.print_error(resp["error"])
                    return resp["error"]

                msg = resp.get("message", {})
                content = msg.get("content", "")
                tool_calls = msg.get("tool_calls", [])

                if content and round_num > 0:
                    ui.print_sara_prefix()
                    ui.render_markdown(content)

                if not tool_calls:
                    self.memory.add("assistant", content)
                    full_response = content
                    break

                self.memory.add("assistant", content or "")
                tool_results = self._execute_tool_calls(tool_calls)
                for _, result in tool_results:
                    self.memory.add("tool", result)
                full_response = content

        return full_response

    def _chat_react(self, user_input: str) -> str:
        """ReAct-style tool calling for models without native support."""
        system_with_react = {"role": "system", "content": SARA_SYSTEM_PROMPT + "\n" + REACT_SYSTEM_ADDON}
        max_steps = 5

        for step in range(max_steps):
            messages = [system_with_react] + self.memory.get_messages()

            ui.print_sara_prefix()
            response_text = ""

            for chunk in self.ollama.chat_stream(self.model, messages):
                if "error" in chunk:
                    ui.print_error(chunk["error"])
                    return chunk["error"]

                content = chunk.get("message", {}).get("content", "")
                if content:
                    response_text += content
                    # Don't print tool_call blocks
                    if "<tool_call>" not in response_text:
                        ui.print_streaming_token(content)

                if chunk.get("done"):
                    break

            ui.print_response_end()

            # Check for tool calls in the response
            tool_call_match = re.search(
                r"<tool_call>\s*([\s\S]*?)\s*</tool_call>", response_text
            )

            if not tool_call_match:
                self.memory.add("assistant", response_text)
                return response_text

            # Parse and execute tool call
            try:
                raw = tool_call_match.group(1)
                call_data = json.loads(raw)
                tool_name = call_data.get("name", "")
                tool_args = call_data.get("arguments", {})

                if self.show_tool_calls:
                    ui.print_tool_call(tool_name, tool_args)

                result = call_tool(tool_name, tool_args)

                if self.show_tool_calls:
                    ui.print_tool_result(result, tool_name)

                # Remove tool_call from response and add clean version
                clean_response = response_text[:tool_call_match.start()].strip()
                if clean_response:
                    self.memory.add("assistant", clean_response)

                # Add tool result as user message (ReAct style)
                self.memory.add("user", f"[Tool Result for {tool_name}]\n{result}")

            except json.JSONDecodeError:
                self.memory.add("assistant", response_text)
                return response_text

        return ""

    def _execute_tool_calls(self, tool_calls: list) -> list[tuple]:
        """Execute a list of tool calls and return (call, result) pairs."""
        results = []
        for tc in tool_calls:
            fn = tc.get("function", tc)  # handle both formats
            name = fn.get("name", "")
            args_raw = fn.get("arguments", {})

            # Parse args if string
            if isinstance(args_raw, str):
                try:
                    args = json.loads(args_raw)
                except Exception:
                    args = {}
            else:
                args = args_raw

            if self.show_tool_calls:
                ui.print_tool_call(name, args)

            result = call_tool(name, args)

            if self.show_tool_calls:
                ui.print_tool_result(result, name)

            results.append((tc, result))

        return results

    def switch_model(self, new_model: str):
        self.model = new_model
        self._uses_native_tools = None  # re-detect on next call
