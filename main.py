from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import VerticalScroll


class TerminalUI(App):
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(Static("", id="output"))
        yield Input(placeholder="Ask anything")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_input_submitted(self, event):
        text = event.input.value
        self.query_one("#output").update(text)
        event.input.value = ""


if __name__ == "__main__":
    app = TerminalUI()
    app.run()
