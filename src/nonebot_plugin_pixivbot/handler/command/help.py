from typing import Union, Awaitable, TypeVar, Sequence

from nonebot_plugin_pixivbot import help_text
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from .command import SubCommandHandler, CommandHandler
from ..pkg_context import context

UID = TypeVar("UID")
GID = TypeVar("GID")


@context.require(CommandHandler).sub_command("help")
class HelpHandler(SubCommandHandler):
    @classmethod
    def type(cls) -> str:
        return "help"

    def enabled(self) -> bool:
        return True

    def parse_args(self, args: Sequence[str], post_dest: PostDestination[UID, GID]) \
            -> Union[dict, Awaitable[dict]]:
        return {}

    async def actual_handle(self, *, post_dest: PostDestination[UID, GID],
                            silently: bool = False, **kwargs):
        await self.post_plain_text(help_text, post_dest=post_dest)
