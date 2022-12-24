from typing import Union

import pytest

from tests import MyTest


class FakePostmanManagerMixin(MyTest):
    @pytest.fixture(autouse=True)
    def FakePostmanManager(self, load_pixivbot):
        from nonebot_plugin_pixivbot.global_context import context
        from nonebot_plugin_pixivbot.model.message import IllustMessageModel, IllustMessagesModel
        from nonebot_plugin_pixivbot.protocol_dep.postman import PostmanManager
        from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination

        @context.bind_singleton_to(PostmanManager)
        class FakePostmanManager:
            def __init__(self):
                self.calls = []

            def assert_not_called(self, post_dest: PostDestination[int, int]):
                for pd, _ in self.calls:
                    assert pd != post_dest

            def assert_called(self, post_dest: PostDestination[int, int],
                              message: Union[str, IllustMessageModel, IllustMessagesModel]):
                assert (post_dest, message) in self.calls

            async def send_plain_text(self, message: str,
                                      *, post_dest: PostDestination[int, int]):
                self.calls.append((post_dest, message))
                print(f"send plain text: {message} to {post_dest}")

            async def send_illust(self, model: IllustMessageModel,
                                  *, post_dest: PostDestination[int, int]):
                self.calls.append((post_dest, model))
                print(f"send illust: {model} to {post_dest}")

            async def send_illusts(self, model: IllustMessagesModel,
                                   *, post_dest: PostDestination[int, int]):
                self.calls.append((post_dest, model))
                print(f"send illusts: {model} to {post_dest}")

        from nonebot_plugin_pixivbot.handler.base import Handler
        Handler.__context__.bind(PostmanManager, FakePostmanManager)

        return FakePostmanManager
