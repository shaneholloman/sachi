from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class FilebotContext(BaseModel):
    n: str | None = Field(
        default=None,
        description="movie / series name",
        examples=["Dark Angel"],
    )
    y: int | None = Field(
        default=None,
        description="movie / series year",
        examples=["2009"],
    )
    s: int | None = Field(
        default=None,
        description="season number",
        examples=["3"],
    )
    e: int | None = Field(
        default=None,
        description="episode number",
        examples=["1"],
    )
    sxe: str | None = Field(
        default=None,
        description="season / episode number",
        examples=["1x01"],
    )
    s00e00: str | None = Field(
        default=None,
        description="season / episode number",
        examples=["S01E01"],
    )
    t: str | None = Field(
        default=None,
        description="episode title",
        examples=["Labyrinth"],
    )
    d: datetime | None = Field(
        default=None,
        description="airdate",
        examples=["2009-06-01"],
    )
    startdate: datetime | None = Field(
        default=None,
        description="series start date",
        examples=["2002-09-20"],
    )
    absolute: int | None = Field(
        default=None,
        description="absolute episode number",
        examples=["42"],
    )
    ny: str | None = Field(
        default=None,
        description="name (year)",
        examples=["Avatar (2009)"],
    )
    es: list[int] | None = Field(
        default=None,
        description="episode numbers",
        examples=["[1, 2, 3]"],
    )
    sy: list[int] | None = Field(
        default=None,
        description="season years",
        examples=["[2002, 2003]"],
    )
    sc: int | None = Field(
        default=None,
        description="season count",
        examples=["5"],
    )
    di: int | None = Field(
        default=None,
        description="duplicate index",
        examples=["1"],
    )
    dc: int | None = Field(
        default=None,
        description="duplicate count",
        examples=["2"],
    )
    age: int | None = Field(
        default=None,
        description="age in days",
        examples=["7"],
    )
    special: int | None = Field(
        default=None,
        description="special number",
        examples=["1"],
    )
    episode: str | None = Field(
        default=None,
        description="episode object",
        examples=["Firefly - 1x01 - Serenity"],
    )
    series: dict[str, Any] | None = Field(
        default=None,
        description="series object",
        examples=["<series properties>"],
    )
    primaryTitle: str | None = Field(
        default=None,
        description="primary name",
        examples=["Juuni Kokuki"],
    )
    alias: str | None = Field(
        default=None,
        description="alias names",
        examples=["[Juuni Kokuki, ...]"],
    )
    movie: dict[str, Any] | None = Field(
        default=None,
        description="movie object",
        examples=["Avatar (2009)"],
    )
    id: int | None = Field(
        default=None,
        description="movie / series ID",
        examples=["1437"],
    )
    tmdbid: int | None = Field(
        default=None,
        description="TheMovieDB ID",
        examples=["1437"],
    )
    tvdbid: int | None = Field(
        default=None,
        description="TheTVDB ID",
        examples=["78874"],
    )
    imdbid: str | None = Field(
        default=None,
        description="IMDb ID",
        examples=["tt0756683"],
    )
    pi: int | None = Field(
        default=None,
        description="part index",
        examples=["1"],
    )
    pc: int | None = Field(
        default=None,
        description="part count",
        examples=["2"],
    )
    lang: str | None = Field(
        default=None,
        description="subtitle language",
        examples=["eng"],
    )
    subt: str | None = Field(
        default=None,
        description="subtitle tag",
        examples=[".eng.forced"],
    )
    plex: Path | None = Field(
        default=None,
        description="Plex Naming Standard",
        examples=["<relative path>"],
    )
    kodi: Path | None = Field(
        default=None,
        description="Kodi Naming Standard",
        examples=["<relative path>"],
    )
    emby: Path | None = Field(
        default=None,
        description="Emby Naming Standard",
        examples=["<relative path>"],
    )
    jellyfin: Path | None = Field(
        default=None,
        description="Jellyfin Naming Standard",
        examples=["<relative path>"],
    )
    az: str | None = Field(
        default=None,
        description="sort collection letter",
        examples=["A"],
    )
    object: Any | None = Field(
        default=None,
        description="match object",
        examples=["Firefly - 1x01 - Serenity"],
    )
    type: str | None = Field(
        default=None,
        description="object type",
        examples=["Episode"],
    )
    anime: bool | None = Field(
        default=None,
        description="is anime episode",
        examples=["false"],
    )
    regular: bool | None = Field(
        default=None,
        description="is regular episode",
        examples=["true"],
    )
    music: str | None = Field(
        default=None,
        description="music object",
        examples=["Leona Lewis - I See You"],
    )
    medium: int | None = Field(
        default=None,
        description="medium index",
        examples=["1"],
    )
    album: str | None = Field(
        default=None,
        description="album",
        examples=["Avatar"],
    )
    artist: str | None = Field(
        default=None,
        description="track artist",
        examples=["Leona Lewis"],
    )
    albumArtist: str | None = Field(
        default=None,
        description="album artist",
        examples=["James Horner"],
    )
    actors: list[str] | None = Field(
        default=None,
        description="list of actors",
        examples=["[Zoe Saldana, ...]"],
    )
    director: str | None = Field(
        default=None,
        description="movie director",
        examples=["James Cameron"],
    )
    collection: str | None = Field(
        default=None,
        description="movie collection",
        examples=["Avatar Collection"],
    )
    ci: int | None = Field(
        default=None,
        description="movie collection index",
        examples=["1"],
    )
    cy: list[int] | None = Field(
        default=None,
        description="movie collection years",
        examples=["[1977, 2019]"],
    )
    decade: int | None = Field(
        default=None,
        description="movie decade",
        examples=["1970"],
    )
    genre: str | None = Field(
        default=None,
        description="primary genre",
        examples=["Science Fiction"],
    )
    genres: list[str] | None = Field(
        default=None,
        description="all genres",
        examples=["[Science Fiction, ...]"],
    )
    language: str | None = Field(
        default=None,
        description="original language",
        examples=["eng"],
    )
    languages: list[str] | None = Field(
        default=None,
        description="spoken languages",
        examples=["[eng]"],
    )
    country: str | None = Field(
        default=None,
        description="origin country",
        examples=["KR"],
    )
    runtime: int | None = Field(
        default=None,
        description="movie / episode runtime",
        examples=["162"],
    )
    certification: str | None = Field(
        default=None,
        description="content rating",
        examples=["PG-13"],
    )
    rating: float | None = Field(
        default=None,
        description="movie rating",
        examples=["7.4"],
    )
    votes: int | None = Field(
        default=None,
        description="movie votes",
        examples=["17720"],
    )
    vcf: str | None = Field(
        default=None,
        description="video compression format",
        examples=["HEVC"],
    )
    vc: str | None = Field(
        default=None,
        description="video codec library",
        examples=["x264"],
    )
    ac: str | None = Field(
        default=None,
        description="audio codec",
        examples=["ac3"],
    )
    cf: str | None = Field(
        default=None,
        description="container format",
        examples=["mkv"],
    )
    vf: str | None = Field(
        default=None,
        description="standard video format",
        examples=["1080p"],
    )
    hpi: str | None = Field(
        default=None,
        description="exact video format",
        examples=["384i"],
    )
    aco: str | None = Field(
        default=None,
        description="audio codec profile",
        examples=["TrueHD+Atmos"],
    )
    acf: str | None = Field(
        default=None,
        description="audio channel format",
        examples=["DD5.1"],
    )
    af: str | None = Field(
        default=None,
        description="audio channel count",
        examples=["6ch"],
    )
    channels: str | None = Field(
        default=None,
        description="audio channel layout",
        examples=["5.1"],
    )
    resolution: str | None = Field(
        default=None,
        description="video resolution",
        examples=["3840x2160"],
    )
    width: int | None = Field(
        default=None,
        description="video width",
        examples=["3840"],
    )
    height: int | None = Field(
        default=None,
        description="video height",
        examples=["2160"],
    )
    bitdepth: int | None = Field(
        default=None,
        description="video bitdepth",
        examples=["10"],
    )
    hdr: str | None = Field(
        default=None,
        description="high dynamic range",
        examples=["HDR"],
    )
    dovi: str | None = Field(
        default=None,
        description="Dolby Vision",
        examples=["Dolby Vision"],
    )
    bitrate: str | None = Field(
        default=None,
        description="overall bitrate",
        examples=["2.0 Mbps"],
    )
    vbr: str | None = Field(
        default=None,
        description="video bitrate",
        examples=["1.6 Mbps"],
    )
    abr: str | None = Field(
        default=None,
        description="audio bitrate",
        examples=["192 kbps"],
    )
    fps: str | None = Field(
        default=None,
        description="frame rate",
        examples=["23.976 fps"],
    )
    khz: str | None = Field(
        default=None,
        description="sampling rate",
        examples=["44.1 kHz"],
    )
    ar: str | None = Field(
        default=None,
        description="aspect ratio",
        examples=["16∶9"],
    )
    ws: str | None = Field(
        default=None,
        description="widescreen tag",
        examples=["WS"],
    )
    hd: str | None = Field(
        default=None,
        description="video definition class",
        examples=["UHD"],
    )
    dt: datetime | None = Field(
        default=None,
        description="media creation date",
        examples=["<date and time>"],
    )
    vs: str | None = Field(
        default=None,
        description="source class",
        examples=["BluRay"],
    )
    source: str | None = Field(
        default=None,
        description="source match",
        examples=["BD25"],
    )
    edition: str | None = Field(
        default=None,
        description="movie edition",
        examples=["Extended Edition"],
    )
    tags: list[str] | None = Field(
        default=None,
        description="movie tags",
        examples=["[Extended Edition]"],
    )
    s3d: str | None = Field(
        default=None,
        description="stereoscopic 3D tag",
        examples=["3D SBS"],
    )
    group: str | None = Field(
        default=None,
        description="release group",
        examples=["ALLiANCE"],
    )
    original: str | None = Field(
        default=None,
        description="original file name",
        examples=["Serenity"],
    )
    historic: dict[str, Any] | None = Field(
        default=None,
        description="original path",
        examples=["<bindings>"],
    )
    info: dict[str, Any] | None = Field(
        default=None,
        description="extended metadata",
        examples=["<all properties>"],
    )
    omdb: dict[str, Any] | None = Field(
        default=None,
        description="OMDb info",
        examples=["<all properties>"],
    )
    localize: dict[str, Any] | None = Field(
        default=None,
        description="dynamic localization",
        examples=["<languages>"],
    )
    order: dict[str, Any] | None = Field(
        default=None,
        description="dynamic episode order",
        examples=["<episode orders>"],
    )
    db: dict[str, Any] | None = Field(
        default=None,
        description="dynamic cross-reference",
        examples=["<mapper>"],
    )
    fn: str | None = Field(
        default=None,
        description="current file name",
        examples=["Serenity"],
    )
    ext: str | None = Field(
        default=None,
        description="file extension",
        examples=["mkv"],
    )
    f: Path | None = Field(
        default=None,
        description="file object",
        examples=["<file path>"],
    )
    folder: Path | None = Field(
        default=None,
        description="folder object",
        examples=["<folder path>"],
    )
    drive: Path | None = Field(
        default=None,
        description="file system root",
        examples=["<folder path>"],
    )
    files: list[Path] | None = Field(
        default=None,
        description="file group",
        examples=["<file paths>"],
    )
    relativeFile: Path | None = Field(
        default=None,
        description="relative library path",
        examples=["<relative path>"],
    )
    mediaFile: Path | None = Field(
        default=None,
        description="primary media file",
        examples=["<file path>"],
    )
    mediaFileName: str | None = Field(
        default=None,
        description="primary media file name",
        examples=["Serenity"],
    )
    mediaTitle: str | None = Field(
        default=None,
        description="embedded media title",
        examples=["Serenity"],
    )
    audioLanguages: list[str] | None = Field(
        default=None,
        description="audio streams",
        examples=["<audio languages>"],
    )
    textLanguages: list[str] | None = Field(
        default=None,
        description="subtitle streams",
        examples=["<subtitle languages>"],
    )
    duration: str | None = Field(
        default=None,
        description="media duration",
        examples=["PT23M9.974S"],
    )
    seconds: int | None = Field(
        default=None,
        description="duration in seconds",
        examples=["1389"],
    )
    minutes: int | None = Field(
        default=None,
        description="duration in minutes",
        examples=["23"],
    )
    hours: str | None = Field(
        default=None,
        description="duration in HH:mm",
        examples=["0:23"],
    )
    bytes: str | None = Field(
        default=None,
        description="file size",
        examples=["356 MB"],
    )
    megabytes: str | None = Field(
        default=None,
        description="file size in MB",
        examples=["356 MB"],
    )
    gigabytes: str | None = Field(
        default=None,
        description="file size in GB",
        examples=["0.4 GB"],
    )
    ct: datetime | None = Field(
        default=None,
        description="file creation date",
        examples=["<date and time>"],
    )
    crc32: str | None = Field(
        default=None,
        description="CRC32 checksum",
        examples=["3E16AF40"],
    )
    media: dict[str, str] | None = Field(
        default=None,
        description="media properties",
        examples=["<media properties>"],
    )
    video: list[dict[str, str]] | None = Field(
        default=None,
        description="video streams",
        examples=["<video streams>"],
    )
    audio: list[dict[str, str]] | None = Field(
        default=None,
        description="audio streams",
        examples=["<audio streams>"],
    )
    text: list[dict[str, str]] | None = Field(
        default=None,
        description="subtitle streams",
        examples=["<subtitle streams>"],
    )
    image: dict[str, str] | None = Field(
        default=None,
        description="image properties",
        examples=["<image properties>"],
    )
    exif: dict[str, str] | None = Field(
        default=None,
        description="EXIF image metadata",
        examples=["<image properties>"],
    )
    camera: dict[str, str] | None = Field(
        default=None,
        description="photo camera",
        examples=["<camera properties>"],
    )
    location: dict[str, str] | None = Field(
        default=None,
        description="photo location",
        examples=["<location properties>"],
    )
    today: datetime | None = Field(
        default=None,
        description="current date",
        examples=["2022-08-08"],
    )
    home: Path | None = Field(
        default=None,
        description="user home folder",
        examples=["<folder path>"],
    )
    output: Path | None = Field(
        default=None,
        description="--output folder",
        examples=["<folder path>"],
    )
    defines: dict[str, str] | None = Field(
        default=None,
        description="--def parameters",
        examples=["<script parameters>"],
    )
    label: str | None = Field(
        default=None,
        description="--def label value",
        examples=["<label parameter>"],
    )
    self: dict[str, Any] | None = Field(
        default=None,
        description="match bindings",
        examples=["<bindings>"],
    )
    model: list[dict[str, Any]] | None = Field(
        default=None,
        description="match context",
        examples=["<list of bindings>"],
    )
    episodelist: list[dict[str, Any]] | None = Field(
        default=None,
        description="series context",
        examples=["<list of bindings>"],
    )
    AnimeList: str | None = Field(
        default=None,
        description="Anime Lists mapper",
        examples=["<mapping>"],
    )
    XEM: str | None = Field(
        default=None,
        description="XEM mapper",
        examples=["<mapping>"],
    )
