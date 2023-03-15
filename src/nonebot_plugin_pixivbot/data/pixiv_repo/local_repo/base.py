from typing import List, Union

from nonebot_plugin_pixivbot.enums import RankingMode
from nonebot_plugin_pixivbot.model import Illust, User
from ..base import PixivRepo
from ..lazy_illust import LazyIllust
from ..models import PixivRepoMetadata


class LocalPixivRepo(PixivRepo):
    async def update_illust_detail(self, illust: Illust, metadata: PixivRepoMetadata):
        ...

    async def update_user_detail(self, user: User, metadata: PixivRepoMetadata):
        ...

    async def invalidate_search_illust(self, word: str):
        ...

    async def append_search_illust(self, word: str,
                                   content: List[Union[Illust, LazyIllust]],
                                   metadata: PixivRepoMetadata) -> bool:
        ...

    async def invalidate_search_user(self, word: str):
        ...

    async def append_search_user(self, word: str, content: List[User],
                                 metadata: PixivRepoMetadata) -> bool:
        ...

    async def invalidate_user_illusts(self, user_id: int):
        ...

    async def append_user_illusts(self, user_id: int,
                                  content: List[Union[Illust, LazyIllust]],
                                  metadata: PixivRepoMetadata,
                                  append_at_begin: bool = False) -> bool:
        ...

    async def invalidate_user_bookmarks(self, user_id: int):
        ...

    async def append_user_bookmarks(self, user_id: int,
                                    content: List[Union[Illust, LazyIllust]],
                                    metadata: PixivRepoMetadata,
                                    append_at_begin: bool = False) -> bool:
        ...

    async def invalidate_recommended_illusts(self):
        ...

    async def append_recommended_illusts(self, content: List[Union[Illust, LazyIllust]],
                                         metadata: PixivRepoMetadata) -> bool:
        ...

    async def invalidate_related_illusts(self, illust_id: int):
        ...

    async def append_related_illusts(self, illust_id: int,
                                     content: List[Union[Illust, LazyIllust]],
                                     metadata: PixivRepoMetadata) -> bool:
        ...

    async def invalidate_illust_ranking(self, mode: RankingMode):
        ...

    async def append_illust_ranking(self, mode: RankingMode,
                                    content: List[Union[Illust, LazyIllust]],
                                    metadata: PixivRepoMetadata) -> bool:
        ...

    async def update_image(self, illust_id: int, page: int, content: bytes,
                           metadata: PixivRepoMetadata):
        ...

    async def invalidate_all(self):
        ...
