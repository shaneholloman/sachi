import asyncio
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Self, assert_never, cast

import jinja2
from guessit import guessit
from pymediainfo import MediaInfo
from textual.widgets.data_table import RowKey

from sachi.config import BaseConfig, read_config
from sachi.context import FileBotContext
from sachi.sources.base import (
    MediaType,
    SachiEpisodeModel,
    SachiParentModel,
)
from sachi.utils import FAKE_SLASH, FS_SPECIAL_CHARS


@dataclass
class SachiMatch:
    parent: SachiParentModel
    episode: SachiEpisodeModel | None


class SachiFile:
    def __init__(self, path: Path):
        self.path = path
        self._match: SachiMatch | None = None

        self.ctx = FileBotContext()
        self.analyze_filename()
        self.media_analysis_done = asyncio.Event()

        self.row_key: RowKey | None = None

    @property
    def match(self) -> SachiMatch | None:
        return self._match

    @match.setter
    def match(self, value: SachiMatch | None):
        self._match = value
        self.analyze_match()
        if not self.media_analysis_done.is_set():
            asyncio.create_task(asyncio.to_thread(self.analyze_media))

    def analyze_filename(self):
        guess = cast(dict, guessit(self.path.name))
        self.ctx.source = guess.get("source", None)

    def analyze_media(self):
        media_info = MediaInfo.parse(self.path)
        if isinstance(media_info, str):
            raise RuntimeError(f"Failed to parse media info: {media_info}")

        video = media_info.video_tracks[0]
        self.ctx.resolution = f"{video.width}x{video.height}"
        self.ctx.bitdepth = video.bit_depth
        self.ctx.vc = video.encoded_library_name

        audio = media_info.audio_tracks[0]
        self.ctx.ac = audio.format

        self.media_analysis_done.set()

    def analyze_match(self):
        if self.match is None:
            return
        parent, episode = self.match.parent, self.match.episode

        self.ctx.n = parent.title

        if episode is not None:
            self.ctx.s = episode.season
            self.ctx.s00e00 = f"S{episode.season:02}E{episode.episode:02}"
            self.ctx.t = episode.name

    async def new_path(self, base: Path) -> Path | None:
        if self.match is None:
            return None

        await self.media_analysis_done.wait()

        config = read_config()
        config_model = BaseConfig(**config.unwrap())

        match self.match.parent.media_type:
            case MediaType.SERIES:
                template_str = config_model.series.template
            case MediaType.MOVIE:
                template_str = config_model.movie.template
            case _:
                assert_never(self.match.parent.media_type)

        # FIXME: replace FAKE_SLASH with a better solution
        template = jinja2.Template(template_str.replace("/", FAKE_SLASH))
        new_segment = template.render(asdict(self.ctx))
        new_segment = FS_SPECIAL_CHARS.sub("", new_segment)
        new_segment = new_segment.replace(FAKE_SLASH, "/")
        return (base / new_segment).with_suffix(self.path.suffix)

    def __eq__(self, other: object):
        return isinstance(other, SachiFile) and self.path == other.path

    def __lt__(self, other: Self):
        return self.path < other.path

    def __le__(self, other: Self):
        return self.path <= other.path

    def __gt__(self, other: Self):
        return self.path > other.path

    def __ge__(self, other: Self):
        return self.path >= other.path
