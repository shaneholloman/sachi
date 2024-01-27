from abc import ABCMeta, abstractmethod
from enum import StrEnum
from typing import Self

from pydantic import BaseModel


class MediaType(StrEnum):
    SERIES = "series"
    MOVIE = "movie"


class SachiSeriesModel(BaseModel):
    title: str


class SachiEpisodeModel(BaseModel):
    season: int
    episode: int
    name: str | None = None


class SachiMovieModel(BaseModel):
    title: str
    year: int


class SachiSourceMeta(type, metaclass=ABCMeta):
    sources: dict[MediaType, dict[str, type["SachiSource"]]] = {
        k: {} for k in MediaType
    }

    def __new__(cls, name, bases, namespace, **kwargs):
        media_types = kwargs.pop("media_types", None)
        service = kwargs.pop("service", None)
        klass = super().__new__(cls, name, bases, namespace, **kwargs)
        if media_types is not None and service is not None:
            for media_type in media_types:
                cls.sources[media_type][service] = klass
        return klass


class SachiSource(metaclass=SachiSourceMeta):
    _instance: Self | None = None

    @abstractmethod
    def series_search(
        self, query: str
    ) -> tuple[SachiSeriesModel, list[SachiEpisodeModel]]:
        ...

    @abstractmethod
    def movie_search(self, query: str) -> SachiMovieModel:
        ...

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
