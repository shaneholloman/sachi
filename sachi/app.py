from pathlib import Path

from textual.app import App

from sachi.screens.episodes import EpisodesScreen
from sachi.screens.rename import RenameScreen


class SachiApp(App):
    TITLE = "Sachi"
    CSS_PATH = __file__.replace(".py", ".tcss")
    SCREENS = {
        "episodes": EpisodesScreen(),
    }
    BINDINGS = [
        ("1", "switch_screen('rename')", "Rename"),
        ("2", "switch_screen('episodes')", "Episodes"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, file_or_dir: Path = Path.cwd(), **kwargs):
        super().__init__(**kwargs)
        self.file_or_dir = file_or_dir

    def on_mount(self):
        rename_screen = RenameScreen(self.file_or_dir)
        self.install_screen(rename_screen, name="rename")
        self.push_screen(rename_screen)
