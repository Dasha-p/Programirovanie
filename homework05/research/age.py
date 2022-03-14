import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"]).items
    now = dt.datetime.now()
    year = now.year
    age = []
    for friend in friends:
        if "bdate" in friend:  # type: ignore
            if len(friend["bdate"]) >= 8:  # type: ignore
                age.append(year - int(friend["bdate"][-4:]))  # type: ignore
    srznach = statistics.mean(age) if age else None
    return srznach
