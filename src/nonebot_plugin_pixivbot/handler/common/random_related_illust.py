from typing import TypeVar, Sequence

from lazy import lazy
from nonebot import on_regex, Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import Depends
from nonebot.typing import T_State

from nonebot_plugin_pixivbot.global_context import context
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from nonebot_plugin_pixivbot.utils.errors import BadRequestError
from .common import CommonHandler
from .recorder import Recorder
from ..entry_handler import post_destination
from ..interceptor.record_req_interceptor import RecordReqInterceptor
from ..utils import get_common_query_rule
from ...context import Inject

UID = TypeVar("UID")
GID = TypeVar("GID")


@context.inject
@context.root.register_eager_singleton()
class RandomRelatedIllustHandler(CommonHandler):
    recorder = Inject(Recorder)

    def __init__(self):
        super().__init__()
        self.add_interceptor(context.require(RecordReqInterceptor))

    @classmethod
    def type(cls) -> str:
        return "random_related_illust"

    def enabled(self) -> bool:
        return self.conf.pixiv_random_related_illust_query_enabled

    @lazy
    def matcher(self):
        return on_regex("^不够色$", rule=get_common_query_rule(), priority=1, block=True)

    async def on_match(self, bot: Bot, event: Event, state: T_State, matcher: Matcher,
                       post_dest: PostDestination[UID, GID] = Depends(post_destination)):
        await self.handle(post_dest=post_dest)

    def parse_args(self, args: Sequence[str], post_dest: PostDestination[UID, GID]) -> dict:
        illust_id = self.recorder.get_resp(post_dest.identifier)
        if not illust_id:
            raise BadRequestError("你还没有发送过请求")
        return {"illust_id": illust_id}

    async def actual_handle(self, *, illust_id: int,
                            count: int = 1,
                            post_dest: PostDestination[UID, GID],
                            silently: bool = False):
        illusts = await self.service.random_related_illust(illust_id, count=count)

        await self.post_illusts(illusts,
                                header=f"这是您点的[{illust_id}]的相关图片",
                                post_dest=post_dest)
