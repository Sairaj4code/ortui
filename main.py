from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Label
from textual.containers import VerticalScroll


class TerminalUI(App):
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]
    CSS_PATH = "main.tcss"

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
        new_label = Label(text)

        chat.mount(new_label)
        new_label.scroll_visible()
        event.input.value = ""


if __name__ == "__main__":
    app = TerminalUI()
    app.run()
