from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

import aiohttp


class MediaType(StrEnum):
    SERIES = "series"
    MOVIE = "movie"


@dataclass
class SachiParentModel[RefIdType]:
    media_type: MediaType
    refId: RefIdType
    title: str
    year: int | None = None


@dataclass
class SachiEpisodeModel[RefIdType]:
    refId: RefIdType
    season: int
    episode: int
    name: str | None = None


class SachiSource[RefIdType](AbstractAsyncContextManager):
    media_type: MediaType
    service: str
    _instance: Self | None = None

    async def __aenter__(self) -> Self:
        self.session = aiohttp.ClientSession(raise_for_status=True)
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.session.close()

    @abstractmethod
    async def search(self, query: str) -> list[SachiParentModel[RefIdType]]:
        ...

    @abstractmethod
    async def get_episodes(
        self, parent: SachiParentModel[RefIdType]
    ) -> list[SachiEpisodeModel[RefIdType]]:
        ...

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init_subclass__(cls, /, media_type: MediaType, service: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.media_type = media_type
        cls.service = service
