from typing import cast

import backoff
import inquirer
import requests
import tomlkit
import typer
from inquirer.questions import TaggedValue
from pydantic import BaseModel, TypeAdapter
from yarl import URL

from sachi.config import read_config, write_config
from sachi.sources.base import (
    MediaType,
    SachiEpisodeModel,
    SachiSeriesModel,
    SachiSource,
)


class ConfigModel(BaseModel):
    tvdb: "TVDBConfigModel"


class TVDBConfigModel(BaseModel):
    apiKey: str
    token: str | None = None


class LoginModel(BaseModel):
    token: str


class SearchResultModel(BaseModel):
    tvdb_id: int
    name: str
    translations: dict[str, str]


class EpisodeModel(BaseModel):
    seasonNumber: int
    number: int
    name: str | None


def giveup(e: Exception):
    assert isinstance(e, requests.HTTPError)
    assert e.response is not None
    return e.response.status_code != 401


class TVDBSource(SachiSource, media_types=[MediaType.SERIES], service="TheTVDB"):
    server = URL("https://api4.thetvdb.com/v4")

    def __init__(self) -> None:
        super().__init__()
        self.config: TVDBConfigModel = self._load_config()

    def _load_config(self) -> TVDBConfigModel:
        config_doc = read_config()
        model = ConfigModel(**config_doc.unwrap())
        return model.tvdb

    def _save_config(self):
        config_doc = read_config()
        table = tomlkit.table()
        table.update(self.config.model_dump())
        config_doc["tvdb"] = table
        write_config(config_doc)

    def _login(self):
        resp = requests.post(
            str(self.server / "login"),
            json=dict(apikey=self.config.apiKey),
        )
        resp.raise_for_status()
        model = LoginModel(**resp.json()["data"])
        self.config.token = model.token
        self._save_config()

    def series_search(
        self, query: str
    ) -> tuple[SachiSeriesModel, list[SachiEpisodeModel]]:
        @backoff.on_exception(
            backoff.expo,
            requests.HTTPError,
            giveup=giveup,
            on_backoff=lambda _: self._login(),
        )
        def _search():
            resp = requests.get(
                str(self.server / "search"),
                params=dict(query=query, type="series"),
                headers=dict(Authorization=f"Bearer {self.config.token}"),
            )
            resp.raise_for_status()
            return TypeAdapter(list[SearchResultModel]).validate_python(
                resp.json()["data"]
            )

        search_res = _search()
        questions = [
            inquirer.List(
                "series",
                message="Select one result",
                choices=[
                    (
                        f"{sr.translations.get("eng", sr.name)}",
                        str(sr.tvdb_id),
                    )
                    for sr in search_res
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            raise typer.Abort()
        series = cast(TaggedValue, answers["series"])

        sachi_series = SachiSeriesModel(title=series.label)

        @backoff.on_exception(
            backoff.expo,
            requests.HTTPError,
            giveup=giveup,
            on_backoff=lambda _: self._login(),
        )
        def _episodes():
            resp = requests.get(
                str(self.server / "series" / series.tag / "episodes" / "default"),
                headers=dict(Authorization=f"Bearer {self.config.token}"),
            )
            resp.raise_for_status()
            return TypeAdapter(list[EpisodeModel]).validate_python(
                resp.json()["data"]["episodes"]
            )

        episodes = _episodes()
        sachi_eps = [
            SachiEpisodeModel(season=ep.seasonNumber, episode=ep.number, name=ep.name)
            for ep in episodes
        ]

        doc = tomlkit.document()
        doc.add(tomlkit.comment("Select the episodes you want to keep"))

        array = tomlkit.array()
        for ep in sachi_eps:
            ep_table = tomlkit.inline_table()
            ep_table.update(ep.model_dump(exclude_none=True))
            array.append(ep_table)
        array = array.multiline(True)
        doc.add("episodes", array)

        res = typer.edit(tomlkit.dumps(doc), extension=".toml", require_save=False)
        if res is None:
            raise typer.Abort()

        doc = tomlkit.parse(res)
        sachi_eps = TypeAdapter(list[SachiEpisodeModel]).validate_python(
            doc["episodes"]
        )

        return sachi_series, sachi_eps
