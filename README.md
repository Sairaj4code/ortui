# ORTUI

> A lightweight terminal-based AI chat client powered by OpenRouter.

ORTUI is a terminal user interface (TUI) for chatting with AI models directly from the command line.

The project is built with **Python**, **Textual**, **Requests**, and **OpenRouter**.

## Features

- 💬 Chat with AI directly from the terminal
- 🖥️ Full-screen terminal interface using Textual
- 👤 Separate user and assistant messages
- 🧠 Conversation history maintained during the session
- 📝 Markdown rendering for AI responses
- ⚡ API requests run in a background worker
- 🤖 Uses OpenRouter's `openrouter/free` model router
- 🌙 Light / dark theme toggle
- 🔐 API key loaded from a local `.env` file

## Tech Stack

- Python
- Textual
- Requests
- python-dotenv
- OpenRouter API

## Project Structure

```text
ortui/
├── main.py
├── ai.py
├── style.tcss
├── .env
├── .gitignore
└── README.md
```

### `main.py`

Handles the terminal interface, user input, conversation history, and displaying user and assistant messages.

### `ai.py`

Handles communication with OpenRouter using the Requests library and returns the assistant's response.

### `style.tcss`

Contains the Textual CSS used for the layout and appearance of the application.

### `.env`

Stores the OpenRouter API key locally.

**This file should never be committed to GitHub.**

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

Activate the virtual environment:

```bash
source env/bin/activate
```

Install the dependencies:

```bash
pip install textual requests python-dotenv
```

## Configuration

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your-openrouter-api-key
```

ORTUI loads the API key from this file using `python-dotenv`.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
env/
.venv/
__pycache__/
*.pyc
```

**Never upload your API key to GitHub.**

## Running ORTUI

Start the application:

```bash
python main.py
```

You can then type a message into the input field and press **Enter**.

Example:

```text
You:
Explain pointers in C

Assistant:
A pointer is a variable that stores the memory address
of another variable...
```

## How It Works

The application follows this flow:

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

Conversation history is stored in memory and included with subsequent requests during the current session.

## Architecture

```text
                ORTUI
                  │
        ┌─────────┴─────────┐
        │                   │
     main.py              ai.py
        │                   │
     Textual            Requests
        │                   │
        └─────────┬─────────┘
                  │
             OpenRouter
                  │
                  ▼
             AI Response
                  │
                  ▼
          Assistant Message
```

## Current Status

ORTUI is currently a **work-in-progress project**.

The core conversational functionality is working, including:

- Terminal chat interface
- User and assistant message separation
- Conversation history
- OpenRouter integration
- Markdown AI responses
- Background API requests

Future improvements may include:

- Streaming AI responses
- Better message styling
- Web search
- Local file reading
- Tool calling
- Model selection
- Persistent conversations
- Additional keyboard shortcuts

## Why I Built This

ORTUI started as a hands-on project to learn how to build a terminal application that communicates with a modern AI API.

The project has helped me explore:

- Terminal user interfaces with Textual
- Event-driven programming
- HTTP requests
- JSON APIs
- LLM API integration
- Conversation state
- Background workers
- Markdown rendering

## License

MIT License
