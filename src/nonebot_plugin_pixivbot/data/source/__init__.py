from typing import Protocol, Callable, Union, Awaitable

from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.config import Config
from nonebot_plugin_pixivbot.enums import DataSourceType


class DataSource(Protocol):
    async def initialize(self):
        ...

    async def close(self):
        ...

    def on_initialized(self, func: Callable[[], Union[None, Awaitable[None]]]):
        ...

    def on_closed(self, func: Callable[[], Union[None, Awaitable[None]]]):
        ...


conf = context.require(Config)
if conf.pixiv_data_source == DataSourceType.mongo:
    from .mongo import MongoDataSource

    context.bind(DataSource, MongoDataSource)
else:
    from .sql import SqlDataSource

    context.bind(DataSource, SqlDataSource)

__all__ = ("DataSource",)
