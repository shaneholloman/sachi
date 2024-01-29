from sachi.sources.base import SachiSource
from sachi.sources.tvdb import TVDBSource

SOURCE_CLASSES: list[type[SachiSource]] = [
    TVDBSource,
]
