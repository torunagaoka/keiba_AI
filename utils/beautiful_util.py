import requests
from bs4 import BeautifulSoup as bs4
from time import sleep

from utils.char_util import normalization


def init_beautifulsoup(url):
    """
    BeautifulSoupを初期化する関数

    Parameters
    ----------
    url : str
        初期化するURL

    Returns
    -------
    fruit_price : soup
        初期化したsoup
    """
    res = requests.get(url)
    sleep(3)
    soup = bs4(res.content, 'html.parser')
    return soup


def get_resultTableWrap(soup):
    """
    レース結果のResultTableWrapを取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    result_table_wrap : soup
        ResultTableWrap
    """
    result_table_wrap = soup.select_one('.ResultTableWrap')
    return result_table_wrap


def get_horse_info(soup, count_true):
    """
    馬名と馬齢をリストで取得する

    Parameters
    ----------
    soup : soup
        soup
    count_true：boolean
        頭数を返す場合はtrue

    Returns
    -------
    count_true ⇨ true
        list_len : int
            頭数
    count_true ⇨ false
        horse_list : list
            馬名のリスト
        horse_age : list
            馬齢のリスト
    """
    horse_list = []
    horse_age = []
    horce_info = soup.select('.Horse_Info')
    exclusion = count_exclusion(soup)
    for i in range(1, len(horce_info)):
        if(i % 2 == 0):
            horse_age.append(normalization(horce_info[i].text)[3])
        else:
            horse_list.append(normalization(horce_info[i].text)[1])
    list_len = len(horse_list) - exclusion
    if (count_true):
        return list_len
    else:
        return horse_list[:list_len], horse_age[:list_len]


def get_time(soup):
    """
    レース結果のtimeを取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    times : list
        走破タイム
    last3fs : list
        上がり3Fのタイム
    """
    time_th = soup.find_all(class_="Time")
    horse_num = get_horse_info(soup, True)
    # 走破タイムを取得
    times = []
    for i in range(1, horse_num*3, 3):
        time = time_th[i].text.splitlines()[1]
        times.append(time)
    # 上がり3Fを取得
    last3fs = []
    for j in range(3, horse_num*3+1, 3):
        last3f = time_th[j].text.splitlines()[1]
        last3fs.append(last3f)
    return times, last3fs


def get_popular_odds(soup):
    """
    レースのtimeを取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    popular_list : list
        人気のリスト
    odds_list : list
        オッズのリスト
    """
    odds_th = soup.find_all(class_="Odds")
    horse_num = get_horse_info(soup, True)
    odds_list = []
    popular_list = []
    for i in range(1, horse_num*2, 2):
        popular_list.append(odds_th[i].text.splitlines()[1])
    for j in range(2, horse_num*2+1, 2):
        odds_list.append(odds_th[j].text.splitlines()[1])
    return popular_list, odds_list


def count_exclusion(soup):
    """
    除外、取消、競走中止、失格頭数をカウントする

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
    count : int
        除外のカウント
    """
    cancel_list = ['取', '中', '除', '失']
    cancel_info = soup.select('.Result_Num')
    count = 0
    for i in range(1, len(cancel_info)):
        for j in range(len(cancel_list)):
            if (cancel_list[j] in normalization(cancel_info[i].text)[1]):
                count += 1
    return count


def get_jockey_weight(soup):
    weight_info = soup.select('.JockeyWeight')
    horse_num = get_horse_info(soup, True)
    weight_list = []
    for i in range(horse_num):
        weight_list.append(weight_info[i].text)
    return weight_list

