from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Markdown
from textual.containers import Horizontal, VerticalScroll
from ai import ask_ai


class TerminalUI(App):
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]
    CSS_PATH = "style.tcss"

    def __init__(self):
        super().__init__()
        self.messages = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="chat")
        yield Input(placeholder="Ask anything")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_input_submitted(self, event):
        text = event.input.value
        chat = self.query_one("#chat")

        new_message = User_message(text)
        user_row = Horizontal(new_message, classes="message-row user-row")
        chat.mount(user_row)
        self.messages.append({"role": "user", "content": text})

        self.fetch_ai_response(chat)
        event.input.value = ""

    @work(thread=True)
    def fetch_ai_response(self, chat):
        assistant_response = ask_ai(self.messages)
        self.messages.append({"role": "assistant", "content": assistant_response})

        # Safely update the UI back on the main thread
        self.call_from_thread(self.mount_assistant_response, chat, assistant_response)

    def mount_assistant_response(self, chat, response_text):
        assistant_message = Assistant_message(response_text)
        assistant_row = Horizontal(
            assistant_message, classes="message-row assistant-row"
        )
        chat.mount(assistant_row)
        assistant_message.scroll_visible()


class User_message(Static):
    def __init__(self, text):
        super().__init__(text)


class Assistant_message(Markdown):
    def __init__(self, text):
        super().__init__(text)


if __name__ == "__main__":
    app = TerminalUI()
    app.run()
