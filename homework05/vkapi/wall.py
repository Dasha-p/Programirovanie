import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import config
from vkapi.exceptions import APIError
from vkapi.session import Session


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass  # test


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    domain = config.VK_CONFIG["domain"]
    token = config.VK_CONFIG["access_token"]
    version = config.VK_CONFIG["version"]
    opens = Session(domain)
    all_posts = []
    for q in range(((count - 1) // max_count) + 1):
        try:
            code = Template(
                """var posts = []; var i = 0; while (i < $attempts) {posts = posts + API.wall.get({"owner_id":$owner_id,"domain":"$domain","offset":$offset + i*100,
                "count":"$count","filter":"$filter","extended":$extended,"fields":'$fields',"v":$version})['items']; i=i+1;} return {'count': posts.length, 'items': posts};"""
            ).substitute(
                owner_id=owner_id if owner_id else 0,
                domain=domain,
                offset=offset + max_count * q,
                count=count - max_count * q if count - max_count * q < 101 else 100,
                attempts=(count - max_count * q - 1) // 100 + 1
                if count - max_count * q < max_count + 1
                else max_count // 100,
                filter=filter,
                extended=extended,
                fields=fields,
                version=str(version),
            )
            posts = opens.post(
                "execute",
                data={
                    "code": code,
                    "access_token": token,
                    "v": version,
                },
            )
            time.sleep(0.7)

            for one in posts.json()["response"]["items"]:
                all_posts.append(one)
        except:
            pass
    return json_normalize(all_posts)
