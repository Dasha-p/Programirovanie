import dataclasses
import math
import time
import typing as tp

from vkapi import config
from vkapi.exceptions import APIError
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    sfile = Session(config.VK_CONFIG["domain"])
    if fields:
        fields = ",".join(fields)  # type: ignore
    else:
        fields = ""  # type: ignore
    url = f"friends.get?access_token={access_token}&user_id={user_id}&count={count}&offset={offset}&fields={fields}&v={v}"
    otvet = sfile.get(url)
    otvet1 = FriendsResponse(otvet.json()["response"]["count"], otvet.json()["response"]["items"])
    return otvet1


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    sfile = Session(config.VK_CONFIG["domain"])
    otvet = []
    if target_uids:
        tuids = ",".join(list(map(str, target_uids)))
        for i in range((len(target_uids) - 1) // 100 + 1):
            try:
                url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uids={tuids}&order={order}&count={count}&offset={i*100}&v={v}"
                mfriends = sfile.get(url)
                for f in mfriends.json()["response"]:
                    otvet.append(
                        MutualFriends(
                            id=f["id"],
                            common_friends=list(map(int, f["common_friends"])),
                            common_count=f["common_count"],
                        )
                    )
            except:
                pass
            time.sleep(0.5)
        return otvet
    try:
        url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&order={order}&count={count}&offset={offset}&v={v}"
        mfriends = sfile.get(url)
        otvet.extend(mfriends.json()["response"])
    except:
        pass
    return otvet
