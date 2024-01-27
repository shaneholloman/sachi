import os
from pathlib import Path
from typing import Self

import inquirer
import jinja2
import rich
import tomlkit
import typer
from pydantic import BaseModel, TypeAdapter
from pymediainfo import MediaInfo
from rich.table import Table

from sachi.config import BaseConfig, read_config
from sachi.context import FilebotContext
from sachi.sources.base import (
    MediaType,
    SachiEpisodeModel,
    SachiMovieModel,
    SachiSeriesModel,
    SachiSource,
)
from sachi.utils import FAKE_SLASH, FS_SPECIAL_CHARS, SOURCES_RE


class SachiSeriesMatch(BaseModel):
    series: SachiSeriesModel
    episode: SachiEpisodeModel


class SachiMovieMatch(BaseModel):
    movie: SachiMovieModel


class SachiFile(BaseModel):
    path: Path
    match: SachiSeriesMatch | SachiMovieMatch | None = None

    def get_new_path(self, base: Path) -> Path | None:
        if self.match is None:
            return None
        config = read_config()
        config_model = BaseConfig(**config.unwrap())
        if isinstance(self.match, SachiSeriesMatch):
            template_str = config_model.series.template
        else:
            template_str = config_model.movie.template
        # FIXME: replace FAKE_SLASH with a better solution
        template = jinja2.Template(template_str.replace("/", FAKE_SLASH))
        ctx = self.get_context()
        new_segment = template.render(ctx.model_dump())
        new_segment = FS_SPECIAL_CHARS.sub("", new_segment)
        new_segment = new_segment.replace(FAKE_SLASH, "/")
        return (base / new_segment).with_suffix(self.path.suffix)

    def get_context(self) -> FilebotContext:
        # FIXME: cache it somewhere
        ctx = FilebotContext()
        ctx = self.analyze_filename(ctx)
        ctx = self.analyze_media(ctx)
        ctx = self.analyze_match(ctx)
        return ctx

    def analyze_filename(self, ctx: FilebotContext) -> FilebotContext:
        for k, v in SOURCES_RE.items():
            if v.search(self.path.name):
                ctx.source = k
                break
        return ctx

    def analyze_media(self, ctx: FilebotContext) -> FilebotContext:
        media_info = MediaInfo.parse(self.path)
        if isinstance(media_info, str):
            raise RuntimeError(f"Failed to parse media info: {media_info}")

        video = media_info.video_tracks[0]
        ctx.resolution = f"{video.width}x{video.height}"
        ctx.bitdepth = video.bit_depth
        ctx.vc = video.encoded_library_name

        audio = media_info.audio_tracks[0]
        ctx.ac = audio.format

        return ctx

    def analyze_match(self, ctx: FilebotContext) -> FilebotContext:
        if self.match is not None:
            if isinstance(self.match, SachiSeriesMatch):
                series, episode = self.match.series, self.match.episode
                ctx.n = series.title
                ctx.s = episode.season
                ctx.s00e00 = f"S{episode.season:02}E{episode.episode:02}"
                ctx.t = episode.name
            elif isinstance(self.match, SachiMovieMatch):
                movie = self.match.movie
                ctx.n = movie.title
                ctx.y = movie.year
            else:
                raise RuntimeError(f"Invalid match type: {self.match}")
        return ctx

    def __lt__(self, other: Self):
        return self.path < other.path

    def __le__(self, other: Self):
        return self.path <= other.path

    def __gt__(self, other: Self):
        return self.path > other.path

    def __ge__(self, other: Self):
        return self.path >= other.path


class SachiEngine:
    def __init__(self, media_type: MediaType):
        self.media_type = media_type
        self.files: list[SachiFile] = []
        self.common_path: Path = Path("/")

    @property
    def table(self) -> Table:
        table = Table("From", "To", title="Pending Renames")
        for file in self.files:
            new_path = file.get_new_path(self.common_path)
            table.add_row(
                str(file.path.relative_to(self.common_path)),
                str(new_path.relative_to(self.common_path))
                if new_path is not None
                else None,
            )
        return table

    def load(self, file_or_dir: Path):
        self._load(file_or_dir)
        self.common_path = Path(os.path.commonpath([f.path for f in self.files]))

    def _load(self, file_or_dir: Path):
        if file_or_dir.name.startswith("."):
            return
        if file_or_dir.is_file():
            self.files.append(SachiFile(path=file_or_dir))
        elif file_or_dir.is_dir():
            for file in file_or_dir.iterdir():
                self._load(file)
        else:
            raise RuntimeError(f"Invalid file or directory: {file_or_dir}")

    def select(self):
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Select the files you want to rename"))
        array = tomlkit.array()
        for f in sorted(self.files):
            array.append(str(f.path.relative_to(self.common_path)))
        array = array.multiline(True)
        doc.add("files", array)

        res = typer.edit(tomlkit.dumps(doc), extension=".toml", require_save=False)
        if res is None:
            raise typer.Abort()

        doc = tomlkit.parse(res)

        class SelectModel(BaseModel):
            files: list[str]

        model = SelectModel(**doc.unwrap())
        self.files = [SachiFile(path=self.common_path / line) for line in model.files]

    def series_search(self) -> tuple[SachiSeriesModel, list[SachiEpisodeModel]]:
        questions = [
            inquirer.List(
                "source",
                message="Which source do you want to use?",
                choices=sorted(SachiSource.sources[self.media_type].keys()),
            ),
            inquirer.Text(
                "query",
                message="Enter your query",
                validate=lambda _, x: len(x.strip()) > 0,
            ),
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            raise typer.Abort()
        klass = SachiSource.sources[self.media_type][answers["source"]]
        source = klass.get_instance()
        return source.series_search(answers["query"].strip())

    def match_episodes(
        self, series: SachiSeriesModel, episodes: list[SachiEpisodeModel]
    ):
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Match the files"))

        aot = tomlkit.aot()
        i = 0
        for file in self.files:
            table = tomlkit.table()
            if file is not None:
                table.add("file", str(file.path.relative_to(self.common_path)))

            match_series = None
            match_ep = None
            if file.match is not None:
                assert isinstance(file.match, SachiSeriesMatch)
                match_series = file.match.series
                match_ep = file.match.episode
            elif i < len(episodes):
                match_series = series
                match_ep = episodes[i]
                i += 1
            if match_series is not None and match_ep is not None:
                match_table = tomlkit.table()
                series_it = tomlkit.inline_table()
                series_it.update(match_series.model_dump(exclude_none=True))
                match_table.add("series", series_it)
                ep_it = tomlkit.inline_table()
                ep_it.update(match_ep.model_dump(exclude_none=True))
                match_table.add("episode", ep_it)
                table.add("item", match_table)

            aot.append(table)

        # remaining episodes
        # FIXME: dedupe code
        for j in range(i, len(episodes)):
            table = tomlkit.table()
            match_table = tomlkit.table()
            series_it = tomlkit.inline_table()
            series_it.update(series.model_dump(exclude_none=True))
            match_table.add("series", series_it)
            ep_it = tomlkit.inline_table()
            ep_it.update(episodes[j].model_dump(exclude_none=True))
            match_table.add("episode", ep_it)
            table.add("item", match_table)
            aot.append(table)

        doc.add("matches", aot)

        res = typer.edit(tomlkit.dumps(doc), extension=".toml", require_save=False)
        if res is None:
            raise typer.Abort()

        doc = tomlkit.parse(res)

        class MatchItemModel(BaseModel):
            file: str | None = None
            item: SachiSeriesMatch | None = None

        model_li = TypeAdapter(list[MatchItemModel]).validate_python(
            doc["matches"].unwrap()
        )
        files = []
        for model in model_li:
            if model.file is not None:
                files.append(
                    SachiFile(path=self.common_path / model.file, match=model.item)
                )
        self.files = files

    def apply_renames(self):
        for file in self.files:
            new_path = file.get_new_path(self.common_path)
            assert new_path is not None
            new_path.parent.mkdir(parents=True, exist_ok=True)
            file.path.rename(new_path)
            rich.print(f"[red]{file.path}[/red]\n-> [green]{new_path}[/green]\n")

    def __call__(self, file_or_dir: Path):
        self.load(file_or_dir)
        self.select()

        while any(f.match is None for f in self.files):
            rich.print(self.table)
            match self.media_type:
                case MediaType.SERIES:
                    series, episodes = self.series_search()
                    self.match_episodes(series, episodes)

                case MediaType.MOVIE:
                    ...

                case _:
                    raise RuntimeError(f"Invalid media type: {self.media_type}")

        rich.print(self.table)
        res = inquirer.confirm("Do you want to rename these files?")
        if not res:
            raise typer.Abort()

        self.apply_renames()
        rich.print("[blue]Done!")
        raise typer.Exit()
