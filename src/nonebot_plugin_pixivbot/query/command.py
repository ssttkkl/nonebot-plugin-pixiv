from lazy import lazy
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State

from nonebot_plugin_pixivbot.global_context import context
from nonebot_plugin_pixivbot.handler import CommandHandler
from nonebot_plugin_pixivbot.query.query import Query
from nonebot_plugin_pixivbot.query.query_manager import QueryManager
from nonebot_plugin_pixivbot.query.utils import get_command_rule, get_post_dest


@context.require(QueryManager).query
class CommandQuery(Query):
    def __init__(self):
        super().__init__()
        self.handler = context.require(CommandHandler)

    @lazy
    def matcher(self):
        return on_command("pixivbot", rule=get_command_rule(), priority=5)

    async def on_match(self, bot: Bot, event: Event, state: T_State, matcher: Matcher):
        args = str(event.get_message()).strip().split()[1:]
        await self.handler.handle(args, post_dest=get_post_dest(bot, event))
