# ORTUI

> A lightweight terminal-based AI chat client powered by OpenRouter.

ORTUI is a terminal user interface (TUI) for chatting with AI models directly from the command line.

It is built with **Python**, **Textual**, and **OpenRouter**.

## Features

- 💬 Chat with an AI directly from the terminal
- 🖥️ Full-screen terminal interface using Textual
- 👤 Separate user and assistant messages
- 🧠 Conversation history is preserved during the session
- 📝 Markdown rendering for AI responses
- ⚡ AI requests run in a background worker so the TUI stays responsive
- 🤖 Uses OpenRouter's `openrouter/free` model router
- 🌙 Toggle between Textual's light and dark themes

## Tech Stack

- Python
- Textual
- Requests
- OpenRouter API

## Project Structure

```text
ortui/
├── main.py
├── ai.py
├── style.tcss
├── .gitignore
└── README.md
```

### `main.py`

Handles the terminal interface, user input, conversation history, and displaying user / assistant messages.

### `ai.py`

Handles communication with OpenRouter and returns the assistant's response.

### `style.tcss`

Contains the Textual CSS used to control the layout and appearance of the chat interface.

## Requirements

- Python 3.10+
- An OpenRouter API key
- Internet connection

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ortui.git
cd ortui
```

Create a virtual environment:

```bash
python3 -m venv env
```

Activate it:

```bash
source env/bin/activate
```

Install the dependencies:

```bash
pip install textual requests
```

## OpenRouter API Key

ORTUI reads the API key from the `OPENROUTER_API_KEY` environment variable.

Set it in your terminal:

```bash
export OPENROUTER_API_KEY="your-api-key"
```

Do **not** commit your API key to GitHub.

You can verify that the variable exists without printing the key itself:

```bash
test -n "$OPENROUTER_API_KEY" && echo "API key is set"
```

## Running ORTUI

Start the application with:

```bash
python main.py
```

You can then type a message into the input box and press **Enter**.

Example:

```text
You:
Explain pointers in C

Assistant:
A pointer is a variable that stores the memory address
of another variable...
```

## How It Works

The application follows this basic flow:

```text
User Input
    ↓
Textual Input Widget
    ↓
on_input_submitted()
    ↓
Add user message to conversation history
    ↓
Send conversation to OpenRouter
    ↓
Receive JSON response
    ↓
Extract assistant response
    ↓
Display assistant message
```

The conversation history is stored as a list of messages and sent to OpenRouter with each request.

## Current Status

ORTUI is currently a **work-in-progress project**.

The core chat functionality is working, but the project is still being developed.

Planned improvements include:

- Streaming AI responses
- Better message styling
- Improved error handling
- Model selection
- Conversation persistence
- Additional keyboard shortcuts
- Configuration options

## Why I Built This

This project was created as a hands-on way to learn:

- Terminal user interfaces with Textual
- Event-driven application design
- HTTP APIs
- JSON-based APIs
- OpenRouter integration
- Background work in Textual
- Building a project from scratch

## Contributing

This project is primarily a learning project, but suggestions, bug reports, and improvements are welcome.

## License

MIT License
