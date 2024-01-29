from pathlib import Path

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from sachi.models import SachiFile


class RenameScreen(Screen):
    SUB_TITLE = "Rename"
    CSS_PATH = __file__.replace(".py", ".tcss")
    BINDINGS = [
        ("d", "remove_element", "Remove"),
        ("p", "apply_renames", "Apply"),
    ]

    files: reactive[list[SachiFile]] = reactive([])

    def __init__(self, file_or_dir: Path, **kwargs):
        super().__init__(**kwargs)
        self.load(file_or_dir)
        self.files.sort()
        self.base_dir = file_or_dir.parent if file_or_dir.is_file() else file_or_dir

    def compose(self) -> ComposeResult:
        yield Header()
        table = DataTable(fixed_rows=1, zebra_stripes=True)
        table.add_columns("From", "To")
        yield table
        yield Footer()

    # Methods

    def load(self, file_or_dir: Path):
        if file_or_dir.name.startswith("."):
            return
        if file_or_dir.is_file():
            self.files.append(SachiFile(path=file_or_dir))
        elif file_or_dir.is_dir():
            for file in file_or_dir.iterdir():
                self.load(file)
        else:
            raise RuntimeError(f"Invalid file or directory: {file_or_dir}")

    # Event handlers

    async def on_mount(self):
        table = self.query_one(DataTable)
        for file in self.files:
            new_path = await file.new_path(self.base_dir)
            file.row_key = table.add_row(
                str(file.path.relative_to(self.base_dir)),
                str(new_path.relative_to(self.base_dir)) if new_path else None,
            )
        table.focus()

    async def on_screen_resume(self):
        table = self.query_one(DataTable)
        table.clear()
        for file in self.files:
            new_path = await file.new_path(self.base_dir)
            file.row_key = table.add_row(
                str(file.path.relative_to(self.base_dir)),
                str(new_path.relative_to(self.base_dir)) if new_path else None,
            )
        table.focus()

    # Key bindings

    def action_remove_element(self):
        table = self.query_one(DataTable)
        cood = table.cursor_coordinate
        keys = table.coordinate_to_cell_key(cood)
        if cood.column == 0:
            del self.files[cood.row]
            table.remove_row(keys.row_key)
        if cood.column == 1:
            self.files[cood.row].match = None
            table.update_cell_at(cood, None)

    async def action_apply_renames(self):
        table = self.query_one(DataTable)
        renamed = []
        for i, file in enumerate(self.files):
            new_path = await file.new_path(self.base_dir)
            if new_path is not None:
                new_path.parent.mkdir(parents=True, exist_ok=True)
                file.path.rename(new_path)
                renamed.append(i)
                if file.row_key is not None:
                    table.remove_row(file.row_key)
        for i in reversed(renamed):
            del self.files[i]
