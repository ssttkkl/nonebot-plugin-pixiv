from typing import Sequence, Dict, Any

from nonebot_plugin_pixivbot.context import Inject
from nonebot_plugin_pixivbot.handler.interceptor.permission_interceptor import GroupAdminInterceptor, \
    AnyPermissionInterceptor, SuperuserInterceptor
from nonebot_plugin_pixivbot.model import PostIdentifier, WatchType, T_UID, T_GID
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination
from nonebot_plugin_pixivbot.service.pixiv_service import PixivService
from nonebot_plugin_pixivbot.service.watchman import Watchman
from nonebot_plugin_pixivbot.utils.errors import BadRequestError
from .command import CommandHandler, SubCommandHandler
from ..pkg_context import context


async def parse_and_get_user(raw_user: str):
    pixiv = context.require(PixivService)
    # try parse
    try:
        user = int(raw_user)
        return await pixiv.get_user(user)
    except ValueError:
        return await pixiv.get_user(raw_user)


async def build_tasks_msg(identifier: PostIdentifier):
    watchman = context.require(Watchman)
    tasks = [x async for x in watchman.get_by_subscriber(identifier)]
    msg = "当前订阅：\n"
    if len(tasks) > 0:
        for x in tasks:
            args = list(filter(lambda kv: kv[1], x.kwargs.items()))
            if len(args) != 0:
                args_text = ", ".join(map(lambda kv: f'{kv[0]}={kv[1]}', args))
                args_text = f"({args_text})"
            else:
                args_text = ""
            msg += f'[{x.code}] {x.type.name} {args_text}\n'
    else:
        msg += '无\n'
    return msg


async def parse_user_illusts_args(args: Sequence[str]):
    if len(args) < 2:
        raise BadRequestError()

    user = await parse_and_get_user(args[1])

    watch_args = {"user_id": user.id}
    message = f"{user.name}({user.id})老师的插画更新"

    return watch_args, message


async def parse_following_illusts_args(args: Sequence[str], post_dest: PostDestination[T_UID, T_GID]):
    if len(args) > 1:
        user = await parse_and_get_user(args[1])

        watch_args = {"pixiv_user_id": user.id,
                      "sender_user_id": post_dest.user_id}
        message = f"{user.name}({user.id})用户的关注者插画更新"
    else:
        watch_args = {"pixiv_user_id": 0,
                      "sender_user_id": post_dest.user_id}
        message = f"关注者插画更新"

    return watch_args, message


@context.inject
@context.require(CommandHandler).sub_command("watch")
class WatchHandler(SubCommandHandler):
    watchman = Inject(Watchman)

    def __init__(self):
        super().__init__()
        self.add_interceptor(AnyPermissionInterceptor(
            context.require(SuperuserInterceptor),
            context.require(GroupAdminInterceptor)
        ))

    @classmethod
    def type(cls) -> str:
        return "watch"

    def enabled(self) -> bool:
        return True

    async def parse_args(self, args: Sequence[str], post_dest: PostDestination[T_UID, T_GID]) -> dict:
        if len(args) == 0:
            raise BadRequestError()

        try:
            type = WatchType[args[0]]
            if type == WatchType.user_illusts:
                watch_kwargs, message = await parse_user_illusts_args(args)
            elif type == WatchType.following_illusts:
                watch_kwargs, message = await parse_following_illusts_args(args, post_dest)
            else:
                raise KeyError()
        except KeyError as e:
            raise BadRequestError(f"未知订阅类型：{args[0]}") from e

        return {"type": type, "watch_kwargs": watch_kwargs, "success_message": "成功订阅" + message}

    # noinspection PyMethodOverriding
    async def actual_handle(self, *, type: WatchType,
                            watch_kwargs: Dict[str, Any],
                            success_message: str,
                            post_dest: PostDestination[T_UID, T_GID],
                            silently: bool = False, **kwargs):
        ok = await self.watchman.watch(type, watch_kwargs, post_dest)
        if ok:
            await self.post_plain_text(success_message, post_dest)
        else:
            await self.post_plain_text("该订阅已存在", post_dest)

    async def actual_handle_bad_request(self, err: BadRequestError,
                                        *, post_dest: PostDestination[T_UID, T_GID],
                                        silently: bool = False):
        msg = ""
        if err.message:
            msg += err.message
            msg += '\n\n'

        msg += await build_tasks_msg(post_dest.identifier)
        msg += "\n" \
               "命令格式：/pixivbot watch <type> [..args]\n" \
               "参数：\n" \
               "  <type>：可选值有user_illusts, following_illusts\n" \
               "  [...args]：根据<type>不同需要提供不同的参数\n" \
               "示例：/pixivbot watch user_illusts <用户名>\n"
        await self.post_plain_text(message=msg, post_dest=post_dest)


@context.inject
@context.require(CommandHandler).sub_command("unwatch")
class UnwatchHandler(SubCommandHandler):
    watchman = Inject(Watchman)

    def __init__(self):
        super().__init__()
        self.add_interceptor(AnyPermissionInterceptor(
            context.require(SuperuserInterceptor),
            context.require(GroupAdminInterceptor)
        ))

    @classmethod
    def type(cls) -> str:
        return "unwatch"

    def enabled(self) -> bool:
        return True

    def parse_args(self, args: Sequence[str], post_dest: PostDestination[T_UID, T_GID]) -> dict:
        if len(args) == 0:
            raise BadRequestError()
        return {"code": args[0]}

    # noinspection PyMethodOverriding
    async def actual_handle(self, *, code: int,
                            post_dest: PostDestination[T_UID, T_GID],
                            silently: bool = False, **kwargs):
        if await self.watchman.unwatch(post_dest.identifier, code):
            await self.post_plain_text(message="取消订阅成功", post_dest=post_dest)
        else:
            raise BadRequestError("取消订阅失败，不存在该订阅")

    async def actual_handle_bad_request(self, err: BadRequestError,
                                        *, post_dest: PostDestination[T_UID, T_GID],
                                        silently: bool = False):
        msg = ""
        if err.message:
            msg += err.message
            msg += '\n'

        msg += await build_tasks_msg(post_dest.identifier)
        msg += "\n"
        msg += "命令格式：/pixivbot unwatch <id>"
        await self.post_plain_text(message=msg, post_dest=post_dest)
