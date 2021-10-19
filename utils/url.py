from utils.char_util import str_format


def create_url(base_url, year, where, many, day, race_num):
    """
    URLを作成する

    Parameters
    ----------
    base_url : str
        ベースのURL
    year : int
        年
    where : int
        開催場所
    many : int
        開催日数
    day : int
        開催
    race_num : int
        レース数

    Returns
    -------
    url : str
        作成したURL
    """
    url = base_url + str(year) + str_format(where, '02') \
        + str_format(many, '02') + str_format(day, '02') \
        + str_format(race_num, '02')
    return url

