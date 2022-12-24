from nonebot_plugin_pixivbot.global_context import context

from .base import PixivRepo
from .lazy_illust import LazyIllust
from .mediator_repo import MediatorPixivRepo

context.bind(PixivRepo, MediatorPixivRepo)

__all__ = ("PixivRepo", "LazyIllust",)
