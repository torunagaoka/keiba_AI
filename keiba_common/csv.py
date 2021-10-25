import csv
import glob

from utils.beautiful_util import init_beautifulsoup
from utils.beautiful_util import get_horse_info
from utils.beautiful_util import get_time
from utils.beautiful_util import get_popular_odds
from utils.beautiful_util import get_jockey_weight
from keiba_common.search import get_month_day
from keiba_common.search import get_condition
from keiba_common.search import get_race_generation
from keiba_common.search import get_race_stag_or_mare
from keiba_common.search import get_race_class
from utils.dic import get_kaisai

TURF_WORK = './work/芝'
DART_WOWK = './work/ダート'
HINDRANCE_WORK = './work/障害'


def make_race_csv(url, RACE_PATH, year, where, race):
    """
    レースのCSVを作成する

    Parameters
    ----------
    url : str
        URL
    RACE_PATH : str
        レースデータの保存先
    year : int
        年
    where : int
        開催場所
    race :int
        レース数
    """
    soup = init_beautifulsoup(url)
    # 条件を取得する
    condition, distance = get_condition(soup)
    # 月と日を取得する
    month, day = get_month_day(soup)
    # 開催場所を取得する
    kaisai = get_kaisai(where)
    # 世代限定戦かどうか
    generation = get_race_generation(soup)
    # 混合戦かどうか
    mixture = get_race_stag_or_mare(soup)
    # レースのクラス
    race_class = get_race_class(soup)
    # 馬名のリストを取得する
    horse_list, horse_age_list = get_horse_info(soup, False)
    # タイムを取得する
    times, last3fs = get_time(soup)
    # オッズ等を取得する
    popular_list, odds_list = get_popular_odds(soup)
    # 斤量を取得する
    weight_list = get_jockey_weight(soup)
    for i in range(len(horse_list)):
        csv_out = []
        csv_out.append(horse_list[i])
        csv_out.append(horse_age_list[i])
        csv_out.append(times[i])
        csv_out.append(last3fs[i])
        csv_out.append(popular_list[i])
        csv_out.append(odds_list[i])
        csv_out.append(weight_list[i])
        if (condition == 0):
            write_race_csv(TURF_WORK, i, year, kaisai, condition, distance, generation, mixture, race_class, month, day, race, csv_out)
        elif (condition == 1):
            write_race_csv(DART_WOWK, i, year, kaisai, condition, distance, generation, mixture, race_class, month, day, race, csv_out)
        elif (condition == 2):
            write_race_csv(HINDRANCE_WORK, i, year, kaisai, condition, distance, generation, mixture, race_class, month, day, race, csv_out)


def write_race_csv(PATH, i, year, kaisai, condition,
                   distance, generation, mixture,
                   race_class, month, day, race, csv_out):
    """
    レース情報をCSVヘ記載する

    Parameters
    ----------
    PATH : str
        書き込む先のファイルパス
    i : int
        番号（i=0ならcsvを上書きするために必要
    kaisai : str
        開催場所
    condition : str
        条件
    distance : str
        距離
    generation : str
        世代限定戦かどうか
    mixture : str
        混合戦かどうか
    race_class : str
        レースクラス
    month : str
        月
    day : str
        日
    race : str
        レース
    csv_out : list
        csvに出力するリスト
    """
    if(i == 0):
        with open('{}/{}.csv'.format(PATH, str(year)+str(kaisai)+str(condition)+str(distance)+str(generation)+str(mixture)+str(race_class)+str(month)+str(day)+str(format(race, '02'))), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)
    else:
        with open('{}/{}.csv'.format(PATH, str(year)+str(kaisai)+str(condition)+str(distance)+str(generation)+str(mixture)+str(race_class)+str(month)+str(day)+str(format(race, '02'))), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)


def get_year_from_csv_name(csv_name):
    """
    CSVの名前から年を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    year : str
        年
    """
    year = str(csv_name[0:4])
    return year


def get_kaisai_from_csv_name(csv_name):
    """
    CSVの名前から開催場所を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    kaisai : str
        開催場所
    """
    kaisai = str(csv_name[4:6])
    return kaisai


def get_condition_from_csv_name(csv_name):
    """
    CSVの名前から条件を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    condition : str
        条件（芝orダート）
    """
    condition = str(csv_name[6])
    return condition


def get_distance_from_csv_name(csv_name):
    """
    CSVの名前から距離を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    distance : str
        距離
    """
    distance = str(csv_name[7:11])
    return distance


def get_generantion_from_csv_name(csv_name):
    """
    CSVの名前から世代限定戦かどうかを取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    generation : str
        世代限定戦かどうか
    """
    generation = str(csv_name[11])
    return generation


def get_mixture_from_csv_name(csv_name):
    """
    CSVの名前から混合戦かどうかを取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    mixture : str
        混合戦かどうか
    """
    mixture = str(csv_name[12])
    return mixture


def get_race_class_from_csv_name(csv_name):
    """
    CSVの名前からレースのクラスを取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    race_class : str
        レースクラス
    """
    race_class = str(csv_name[13])
    return race_class


def get_month_from_csv_name(csv_name):
    """
    CSVの名前から月を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    month : str
        月
    """
    month = str(csv_name[14:16])
    return month


def get_day_from_csv_name(csv_name):
    """
    CSVの名前から日を取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    day : str
        月
    """
    day = str(csv_name[16:18])
    return day


def get_race_from_csv_name(csv_name):
    """
    CSVの名前からレースを取得する

    Parameters
    ----------
    csv_name : str
        CSVのファイル名

    Returns
    -------
    race : str
        レース
    """
    day = str(csv_name[18:20])
    return day

