import csv
from datetime import datetime as dt
from pathlib import Path
import os

from utils.beautiful_util import init_beautifulsoup
from utils.beautiful_util import get_horse_info
from utils.beautiful_util import get_time
from utils.beautiful_util import get_popular_odds
from utils.beautiful_util import get_jockey_weight
from utils.beautiful_util import get_tbody
from keiba_common.search import get_month_day
from keiba_common.search import get_condition
from keiba_common.search import get_race_generation
from keiba_common.search import get_race_stag_or_mare
from keiba_common.search import get_race_class
from keiba_common.search import get_father
from keiba_common.horse import get_horce_name
from keiba_common.odds import get_tansho_fukusho
from keiba_common.odds import get_ren_sanren
from utils.dic import get_kaisai
from utils.tools import normalization
from utils.tools import time_to_sec

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

    Returns
    -------
    file_name : str
        ファイル名
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
    file_name = get_file_name(year, kaisai, condition,
                            distance, generation, mixture,
                            race_class, month, day, race)
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
            write_race_csv(TURF_WORK, i, file_name, csv_out)
        elif (condition == 1):
            write_race_csv(DART_WOWK, i, file_name, csv_out)
        elif (condition == 2):
            pass
    return file_name, soup, condition


def write_race_csv(PATH, i, file_name, csv_out):
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
        with open('{}/{}.csv'.format(PATH, file_name), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)
    else:
        with open('{}/{}.csv'.format(PATH, file_name), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)


def get_file_name(year, kaisai, condition,
                  distance, generation, mixture,
                  race_class, month, day, race):
    """
    ファイル名を作成する

    Parameters
    ----------
    year : str
        年
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

    Returns
    -------
    file_name : str
        ファイル名
    """
    file_name = str(year) + str(kaisai) + str(condition) + str(distance) \
            + str(generation) + str(mixture) + str(race_class) \
            + str(month) + str(day) + str(format(race, '02'))
    return file_name


def make_horse_csv(horse_path, horse_name, csv_out, soup):
    """
    馬のcsvデータを作成する
    """
    horse_path = horse_path + horse_name + '.csv'
    file = Path(horse_path)
    if os.path.exists(horse_path):
        with open(horse_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)
    else:
        file.touch(exist_ok=True)
        father_list = get_father(soup)
        with open(horse_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(father_list)
        with open(horse_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_out)


def write_horse_csv(file_name, url, horse_path):
    year = get_year_from_csv_name(file_name)
    month = get_month_from_csv_name(file_name)
    day = get_day_from_csv_name(file_name)
    # 対象日時を作成
    corresponding_day = str(year) + '/' + str(month) + '/' + str(day)
    horse_dic = get_horce_name(url)
    for key in horse_dic:
        horse_url = horse_dic[key]
        soup = init_beautifulsoup(horse_url)
        # tbodyを取得する
        tbody = get_tbody(soup, corresponding_day)
        tr_all = tbody.find_all('tr')
        # 対象レースのtrを取得する
        tr = get_tr(tr_all, corresponding_day)
        # csvに記載するデータを取得する
        horse_data = get_horse_data(tr, file_name)
        make_horse_csv(horse_path, key, horse_data, soup)


def get_horse_data(tr, file_name):
    horse_data_list = []
    # レースIDを取得（ファイル名）
    race_id = file_name
    horse_data_list.append(race_id)
    # 頭数取得
    horse_many = int(tr.find_all('td')[6].text)
    horse_data_list.append(horse_many)
    # 枠番取得
    horse_waku = int(tr.find_all('td')[7].text)
    horse_data_list.append(horse_waku)
    # 馬番取得
    horse_num = int(tr.find_all('td')[8].text)
    horse_data_list.append(horse_num)
    # オッズ取得
    odds = float(tr.find_all('td')[9].text)
    horse_data_list.append(odds)
    # 人気取得
    popular = int(tr.find_all('td')[10].text)
    horse_data_list.append(popular)
    # 着順取得
    result = tr.find_all('td')[11].text
    horse_data_list.append(result)
    # ジョッキー取得
    jokey = tr.find_all('td')[12].text
    jokey = normalization(jokey)[1]
    horse_data_list.append(jokey)
    # 斤量を取得
    weight = float(tr.find_all('td')[13].text)
    horse_data_list.append(weight)
    # 条件を取得
    condition = get_condition_from_csv_name(file_name)
    horse_data_list.append(condition)
    # 距離を取得
    distance = get_distance_from_csv_name(file_name)
    horse_data_list.append(distance)
    # 馬場状態を取得
    groud_info = tr.find_all('td')[15].text
    horse_data_list.append(groud_info)
    # 走破タイムを取得
    run_time = tr.find_all('td')[17].text
    run_time = dt.strptime(run_time, '%M:%S.%f')
    run_time_second = time_to_sec(run_time)
    horse_data_list.append(run_time_second)
    # 着差を取得
    diff = float(tr.find_all('td')[18].text)
    horse_data_list.append(diff)
    # 上がり3Fを取得
    last3f = float(tr.find_all('td')[22].text)
    horse_data_list.append(last3f)
    # 馬体重を取得
    horse_weight_all = tr.find_all('td')[23].text
    horse_weight = horse_weight_all[:3]
    horse_weight_inc_dec = horse_weight_all[4:][:-1]
    horse_data_list.append(horse_weight)
    horse_data_list.append(horse_weight_inc_dec)
    # 賞金を取得
    prize_money = tr.find_all('td')[-1].text
    if (prize_money == '\xa0'):
        prize_money = 0
    horse_data_list.append(prize_money)
    return horse_data_list


def make_odds_csv(race_id, path, soup):
    file = path + race_id + '.csv'
    header, result, payout = get_odds_data(soup)
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(result)
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(payout)


def get_odds_data(soup):
    tansho = get_tansho_fukusho(soup, True)
    hukusho = get_tansho_fukusho(soup, False)
    umaren = get_ren_sanren(soup, '馬連')
    wide = get_ren_sanren(soup, 'ワイド')
    umatan = get_ren_sanren(soup, '馬単')
    sanrenhuku = get_ren_sanren(soup, '三連複')
    sanrentan = get_ren_sanren(soup, '三連単')
    # ヘッダー
    header = tansho[0] + hukusho[0] \
            + umaren[0] + wide[0] + umatan[0] \
            + sanrenhuku[0] + sanrentan[0]
    # 結果
    result = tansho[1] + hukusho[1] \
            + umaren[1] + wide[1] + umatan[1] \
            + sanrenhuku[1] + sanrentan[1]
    # 払い戻し
    payout = tansho[2] + hukusho[2] \
            + umaren[2] + wide[2] + umatan[2] \
            + sanrenhuku[2] + sanrentan[2]
    return header, result, payout


def get_tr(tr_all, corresponding_day):
    """
    対象のtrを取得する

    Parameters
    ----------
    tr_all : tr
        戦績全て
    corresponding_day : str
        対象日時

    Returns
    -------
    tr : tr
        対象日のtr
    """
    for i in range(0, len(tr_all)):
        if(tr_all[i].find_all('td')[0].text == corresponding_day):
            index = i
            break
    tr = tr_all[index]
    return tr


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

