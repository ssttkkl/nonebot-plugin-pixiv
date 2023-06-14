from typing import Sequence

from nonebot import on_regex
from nonebot.internal.params import Depends
from nonebot.params import RegexGroup

from nonebot_plugin_pixivbot.plugin_service import random_illust_service
from nonebot_plugin_pixivbot.protocol_dep.post_dest import post_destination
from .base import RecordCommonHandler
from ..pkg_context import context
from ..utils import get_common_query_rule, get_count
from ...config import Config
from ...service.pixiv_service import PixivService

conf = context.require(Config)
service = context.require(PixivService)


class RandomIllustHandler(RecordCommonHandler, service=random_illust_service):
    @classmethod
    def type(cls) -> str:
        return "random_illust"

    @classmethod
    def enabled(cls) -> bool:
        return conf.pixiv_random_illust_query_enabled

    async def parse_args(self, args: Sequence[str]) -> dict:
        return {"word": args[0]}

    # noinspection PyMethodOverriding
    async def actual_handle(self, *, word: str,
                            count: int = 1):
        illusts = await service.random_illust(word, count=count,
                                              exclude_r18=(not await self.is_r18_allowed()),
                                              exclude_r18g=(not await self.is_r18g_allowed()))

        await self.post_illusts(illusts,
                                header=f"这是您点的{word}图")


@on_regex("^来(.*)?张(.+)图$", rule=get_common_query_rule(), priority=5).handle()
async def on_match(matched_groups=RegexGroup(),
                   post_dest=Depends(post_destination)):
    word = matched_groups[1]
    await RandomIllustHandler(post_dest).handle(word, count=get_count(matched_groups))
