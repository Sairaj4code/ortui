import json
import os
import requests
from dotenv import load_dotenv
from tools.file_tools import search_and_read_file, write_file

load_dotenv()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_and_read_file",
            "description": "Recursively search for a file within a base directory and read its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_dir": {
                        "type": "string",
                        "description": "The base directory to start the search from (e.g., current directory '.' or a project path).",
                    },
                    "file_name": {
                        "type": "string",
                        "description": "The exact name of the file to search for (e.g., 'port_scanner.go').",
                    },
                },
                "required": ["base_dir", "file_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or write text/code content to a file within a base directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_dir": {
                        "type": "string",
                        "description": "The base directory where the file should be created (e.g., current directory '.').",
                    },
                    "file_name": {
                        "type": "string",
                        "description": "The name or relative path of the file to write (e.g., 'main.py' or 'utils/helper.py').",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full code or text content to write into the file.",
                    },
                },
                "required": ["base_dir", "file_name", "content"],
            },
        },
    },
    {"type": "openrouter:web_search"},
]


def ask_ai(messages_list):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",
                "messages": messages_list,
                "tools": TOOLS,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]

        # Check if the model wants to call a tool
        if "tool_calls" in message and message["tool_calls"]:
            # Push the assistant's tool-call request into the conversation history
            messages_list.append(message)

            for tool_call in message["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call["id"]

                # Run our local file tool implementation
                if func_name == "search_and_read_file":
                    tool_output = search_and_read_file(
                        base_dir=func_args.get("base_dir", "."),
                        file_name=func_args.get("file_name", ""),
                    )
                elif func_name == "write_file":
                    tool_output = write_file(
                        base_dir=func_args.get("base_dir", "."),
                        file_name=func_args.get("file_name", ""),
                        contents=func_args.get("content", ""),
                    )
                elif func_name == "openrouter:web_search":
                    tool_output = "Web search executed by open router"
                else:
                    tool_output = f"Error: Tool {func_name} not found."

                # Send the tool result back to the model with role 'tool'
                messages_list.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_output,
                    }
                )

            # Do a recursive call so the model reads the tool output and replies to the user
            return ask_ai(messages_list)

        # Standard text reply
        return message.get("content", "")

    except Exception as e:
        return f"Error connecting to AI: {e}"
