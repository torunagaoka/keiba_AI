import requests
from bs4 import BeautifulSoup as bs4
from time import sleep
import re

from utils.char_util import str_format


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


