"""
nonebot-plugin-pixivbot

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/ssttkkl/nonebot-plugin-pixivbot
"""
from nonebot.plugin import PluginMetadata

from .config import Config
from .usage import usage

# =========== require dependency ============
from nonebot import require

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_access_control")
require("nonebot_plugin_session")
require("nonebot_plugin_saa")

# =========== plugin meta ============
from nonebot_plugin_saa import __plugin_meta__ as saa_meta

__plugin_meta__ = PluginMetadata(
    name='PixivBot',
    description='发送随机Pixiv插画、画师更新推送、定时订阅推送……',
    usage=usage,
    type="application",
    homepage="https://github.com/bot-ssttkkl/nonebot-plugin-pixivbot",
    config=Config,
    supported_adapters=saa_meta.supported_adapters
)

# =========== register handler & service ============
from . import service
from . import handler

__all__ = ("context", "__plugin_meta__")
