import re

from utils.beautiful_util import init_beautifulsoup
from utils.char_util import str_format


def search_number_of_times_held(url_org, year, where):
    """
    manyのmaxを検索する

    Parameters
    ----------
    url_org : str
        ベースのURL
    year : str
        年
    where : str
        開催場所

    Returns
    -------
    max_many : int
        maxのmany
    """
    for i in range(1, 10):
        url_search = url_org + str(year) \
                    + str_format(where, '02') \
                    + str_format(i, '02') \
                    + str_format(1, '02') \
                    + str_format(1, '02')
        soup_search = init_beautifulsoup(url_search)
        take_out = soup_search.find_all('span', attrs={'class': 'Horse_Name'})
        if len(take_out) == 0:
            max_many = i
            break
    return int(max_many)


def search_number_of_days(url_org, year, where, many):
    """
    dayのmaxを検索する

    Parameters
    ----------
    url_org : str
        ベースのURL
    year : str
        年
    where : str
        開催場所
    many : str
        開催日数

    Returns
    -------
    max_day : int
        maxのday
    """
    for i in range(1, 20):
        url_search = url_org + str(year) \
                    + str_format(where, '02') \
                    + str_format(many, '02') \
                    + str_format(i, '02') \
                    + str_format(1, '02')
        soup_search = init_beautifulsoup(url_search)
        take_out = soup_search.find_all('span', attrs={'class': 'Horse_Name'})
        if len(take_out) == 0:
            max_day = i
            break
    return int(max_day)


def search_number_of_race(url, year, where, many, day):
    """
    raceのmaxを検索する

    Parameters
    ----------
    url_org : str
        ベースのURL
    year : str
        年
    where : str
        開催場所
    many : str
        開催日数
    day : str
        開催

    Returns
    -------
    max_race : int
        maxのrace
    """
    for i in range(12, 1, -1):
        url_search = url + str(year)\
                    + str_format(where, '02') \
                    + str_format(many, '02') \
                    + str_format(day, '02') \
                    + str_format(i, '02')
        soup_search = init_beautifulsoup(url_search)
        take_out = soup_search.find_all('span', attrs={'class': 'Horse_Name'})
        if len(take_out) != 0:
            max_race = i + 1
            break
    return int(max_race)


def get_condition(soup):
    """
    条件を取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    turf : int
        芝⇨0
        ダート⇨1
        障害⇨2
    """
    # 条件を取得
    condition = soup.select_one('.RaceData01').text.split('/')[1][:6]
    if ('障' in condition):
        turf = 2
    elif('ダ' in condition):
        turf = 1
    elif('芝' in condition):
        turf = 0
    distance = condition[2:]
    return turf, distance


def get_month_day(soup):
    """
    月・日を取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    month : str
        月
    day : str
        日
    """
    cal = soup.find('dd', attrs={'class': 'Active'}).text
    if '月' in cal:
        month_elm = re.match(r'(.*)(?=月[0-9])', cal)
        month = format(int(month_elm.group()), '02')
        day_elm = re.match(r'(.*)(?=日\()', cal)
        day_group = day_elm.group()
        day_work = re.search(r'(?<=月)(.*)', day_group)
        day = format(int(day_work.group()), '02')
    else:
        month_elm = cal.split('/')[0]
        day_elm = cal.split('/')[1]
        month = format(int(month_elm), '02')
        day = format(int(day_elm), '02')
    return month, day


def whether_grade_race(soup):
    """
    重賞かどうか取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    grade : int
        G1⇨6
        G2、G3⇨5
        OP⇨0
    """
    if (soup.select_one('.Icon_GradeType3')):
        grade = 5
    elif(soup.select_one('.Icon_GradeType2')):
        grade = 5
    elif(soup.select_one('.Icon_GradeType1')):
        grade = 6
    else:
        grade = 0
    return grade


def get_race_generation(soup):
    """
    レースの世代区分を返す

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    mixed : int
        世代限定戦⇨0
        世代限定戦ではない⇨1
    """
    race_class_div = soup.select_one('.RaceData02')
    race_generation = race_class_div.find_all('span')[3].text
    if ('以上' not in race_generation):
        mixed = 0
    else:
        mixed = 1
    return mixed


def get_race_class(soup):
    """
    レースの格を返す

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    race_class : int
        新馬・未勝利⇨0
        1勝クラス・500万⇨1
        2勝クラス・1000万⇨2
        3勝クラス・1600万⇨3
        OP・L⇨4
        G2・G3⇨5
        G1⇨6
    """
    race_class_div = soup.select_one('.RaceData02')
    race_class_work = race_class_div.find_all('span')[4].text
    if ('新馬' in race_class_work) | ('未勝利' in race_class_work):
        race_class = 0
    elif ('１勝' in race_class_work) | ('５００万' in race_class_work):
        race_class = 1
    elif ('２勝' in race_class_work) | ('１０００万' in race_class_work):
        race_class = 2
    elif ('３勝' in race_class_work) | ('１６００万' in race_class_work):
        race_class = 3
    elif ('オープン' in race_class_work):
        class_work = whether_grade_race(soup)
        if (class_work == 0):
            race_class = 4
        else:
            race_class = class_work
    return race_class


def get_race_stag_or_mare(soup):
    """
    混合戦かどうかを返す

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    whether : int
        混合戦⇨0
        牝馬限定戦⇨1
    """
    race_class_div = soup.select_one('.RaceData02')
    info = race_class_div.find_all('span')[5].text
    if ('牡' in info):
        whether = 0
    elif('牝' in info):
        whether = 1
    else:
        whether = 0
    return whether


# def get_race_info(soup, where):
#     # 条件を取得
#     condition = get_condition(soup)
#     # 月・日を取得
#     month, day = get_month_day(soup)
#     # 開催場所を取得
#     kaisai = get_kaisai(where)
#     # 世代限定戦かどうか
#     generation = get_race_generation(soup)
#     # 牡馬・牝馬混合戦かどうか
#     mixture = get_race_stag_or_mare(soup)
#     # レースクラス
#     race_class = get_race_class(soup)
#     return condition, month, day, kaisai, generation, mixture, race_class


