from utils.beautiful_util import init_beautifulsoup
from utils.beautiful_util import get_horse_info
from utils.tools import normalization


def get_horce_name(url):
    """
    馬名とurlを取得する

    Parameters
    ----------
    url : str
        URL

    Returns
    -------
    horce_dic : dec
        {馬名:馬のurl}の辞書
    """
    soup = init_beautifulsoup(url)
    horse_num = get_horse_info(soup, True)
    horce_dic = {}
    for i in range(1, horse_num+1):
        horce = soup.find_all(class_='Horse_Name')[i]
        horce = horce.find('a')
        horce_url = horce.get('href')
        horce_name = soup.find_all(class_='Horse_Name')[i].text
        horce_name = normalization(horce_name)[0]
        horce_dic[horce_name] = horce_url
    return horce_dic

