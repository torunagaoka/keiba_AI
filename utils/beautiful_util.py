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


def get_horse_info(soup):
    """
    馬名と馬齢をリストで取得する

    Parameters
    ----------
    soup : soup
        soup

    Returns
    -------
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
    return horse_list[:list_len], horse_age[:list_len]


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


