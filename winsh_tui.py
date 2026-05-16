from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, DataTable
import json
import os

CONFIG_FILE = "winshield_config.json"
WATCHED_DIR = r"C:\WinShieldProtected"

class WinShieldTUI(App):
    CSS = """
    Screen { background: #1e1e2e; }
    #sidebar { width: 30; background: #252538; border-right: solid #45475a; padding: 1; }
    #main-content { padding: 1; }
    .status-card { background: #a6e3a1; color: #11111b; font-weight: bold; text-align: center; height: 3; margin-bottom: 1; content-align: center middle; }
    .header-text { font-weight: bold; color: #cdd6f4; margin-bottom: 1; }
    """

    BINDINGS = [
        ("q", "quit", "Beenden"),
        ("l", "toggle_mode", "Modus wechseln"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, title="WinShield Terminal Control Center")
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("🛡️ WINSH PANEL", classes="header-text")
                yield Static("STATUS: SCHARF", id="status-widget", classes="status-card")
                yield Button("Modus Umschalten", id="btn-toggle", variant="primary")
                yield Button("Profile Neuladen", id="btn-reload", variant="default")
            with Vertical(id="main-content"):
                yield Static("Whitelist-Profile (Erlaubte Programme):", classes="header-text")
                yield DataTable(id="profile-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.add_columns("Programmname", "Überwachtes Verzeichnis")
        table.cursor_type = "row"
        self.reload_profiles()

    def reload_profiles(self) -> None:
        table = self.query_one("#profile-table", DataTable)
        table.clear()
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                for folder, apps in config.items():
                    for app in apps:
                        table.add_row(app, folder)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-reload":
            self.reload_profiles()
        elif event.button.id == "btn-toggle":
            status_widget = self.query_one("#status-widget", Static)
            if "SCHARF" in str(status_widget.renderable):
                status_widget.update("STATUS: LERNEN")
                status_widget.styles.background = "#f9e2af"
            else:
                status_widget.update("STATUS: SCHARF")
                status_widget.styles.background = "#a6e3a1"
