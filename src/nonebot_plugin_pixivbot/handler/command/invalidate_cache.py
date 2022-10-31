from typing import TypeVar, Sequence

from nonebot_plugin_pixivbot.data.pixiv_repo import PixivRepo
from nonebot_plugin_pixivbot.global_context import context
from nonebot_plugin_pixivbot.handler.interceptor.permission_interceptor import SuperuserInterceptor
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from .command import SubCommandHandler, CommandHandler
from ...context import Inject

UID = TypeVar("UID")
GID = TypeVar("GID")


@context.inject
@context.require(CommandHandler).sub_command("invalidate_cache")
class InvalidateCacheHandler(SubCommandHandler):
    repo = Inject(PixivRepo)

    def __init__(self):
        super().__init__()
        self.add_interceptor(context.require(SuperuserInterceptor))

    @classmethod
    def type(cls) -> str:
        return "invalidate_cache"

    def enabled(self) -> bool:
        return True

    def parse_args(self, args: Sequence[str], post_dest: PostDestination[UID, GID]) -> dict:
        return {}

    async def actual_handle(self, *, post_dest: PostDestination[UID, GID],
                            silently: bool = False, **kwargs):
        await self.repo.invalidate_cache()
        await self.post_plain_text(message="ok", post_dest=post_dest)
