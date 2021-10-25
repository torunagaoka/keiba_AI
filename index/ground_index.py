import glob
import pandas as pd
from datetime import datetime as dt
import os

from utils.tools import time_to_sec
from utils.tools import time_avg
from keiba_common.csv import get_distance_from_csv_name
from keiba_common.csv import get_condition_from_csv_name
from keiba_common.csv import get_kaisai_from_csv_name
from keiba_common.csv import get_generantion_from_csv_name
from keiba_common.csv import get_mixture_from_csv_name
from keiba_common.csv import get_race_class_from_csv_name
from utils.dic import return_base_time
from utils.dic import return_class_index
from utils.dic import return_distance_correction

TURF_WORK = './work/芝/*.csv'
DART_WOWK = './work/ダート/*.csv'


def make_ground_index(condition):
    """
    その日の馬場指数を求める

    Parameters
    ----------
    condition : int
        条件 ⇨芝：0,ダート:1

    Returns
    -------
    ground_index_avg : float
        馬場指数の平均
    """
    if (condition == 0):
        # 芝の馬場指数を作成する
        path = glob.glob(TURF_WORK)
    elif (condition == 1):
        path = glob.glob(DART_WOWK)
    # 馬場指数用のリスト
    ground_index_list = []
    for race in range(len(path)):
        # ファイル名を取得する
        file_name = os.path.split(path[race])[1]
        # 開催を取得する
        kaisai = get_kaisai_from_csv_name(file_name)
        # 距離を取得する
        distance = get_distance_from_csv_name(file_name)
        # 条件を取得する
        condition = get_condition_from_csv_name(file_name)
        # 世代限定戦かどうかを取得する
        generation = get_generantion_from_csv_name(file_name)
        # 混合戦かどうか
        mixed = get_mixture_from_csv_name(file_name)
        # レースクラス
        race_class = get_race_class_from_csv_name(file_name)
        # リストの初期化
        run_time_list = []
        run_last3f_list = []
        df = pd.read_csv(path[race], header=None)
        # 上位3頭で走破タイム平均・上がり3F平均を求める
        for num in range(3):
            # 走破タイムを取得
            run_time_str = df.at[num, 2]
            run_time = dt.strptime(run_time_str, '%M:%S.%f')
            run_time_second = time_to_sec(run_time)
            # 上がり3Fを取得
            run_last3f_str = df.at[num, 3]
            # リストに格納
            run_time_list.append(run_time_second)
            run_last3f_list.append(run_last3f_str)
        # 走破タイムの平均値
        run_time_avg = time_avg(run_time_list)
        # 上がり3Fの平均値
        run_last3f_avg = time_avg(run_last3f_list)
        # スローペース補正を求める
        SP = -((run_time_avg / (int(distance[:2]) * 2)) * 12 - run_last3f_avg) * 10
        # 距離指数
        distance_correction = return_distance_correction(
            str(condition) + str(distance)
        )
        # 馬場指数用基準タイム
        ground_index_base_time = ground_index_basetime(
            kaisai, condition, distance, generation, mixed, race_class
            )
        # 馬場指数
        ground_index = ((run_time_avg - ground_index_base_time) * 10) + (SP * distance_correction)
        ground_index_list.append(ground_index)
    ground_index_avg = time_avg(ground_index_list)
    return ground_index_avg


def ground_index_basetime(kaisai, condition, distance,
                          generation, mixed, race_class):
    """
    馬場指数用のベースタイムを求める
    馬場指数用基準タイム ＝ 基準タイム － (クラス指数 × 距離指数)

    Parameters
    ----------
    kaisai : str
        開催
    condition : int
        条件
    distance : int
        距離
    generation : int
        世代限定戦かどうか
    mixed : int
        混合戦かどうか
    race_class : int
        レースのクラス


    Returns
    -------
    ground_index_avg : float
        馬場指数の平均
    """
    # 基準タイム用のキー
    base_time_key = str(kaisai) + str(condition) + str(distance)
    # 基準タイムを取得
    base_time = return_base_time(base_time_key)
    # クラス指数のキー
    class_index_key = str(condition) + str(generation) \
                        + str(mixed) + str(race_class)
    # クラス指数
    class_index = return_class_index(class_index_key)
    # 距離補正のキー
    distance_index_key = str(condition) + str(distance)
    # 距離補正
    distance_index = return_distance_correction(distance_index_key)
    # 馬場指数用の基準タイム
    ground_index_base_time = base_time - (class_index * distance_index * 0.1)
    return ground_index_base_time


def ground_index_add(condition):
    if (condition == 0):
        # 芝の馬場指数を作成する
        path = glob.glob(TURF_WORK)
    elif (condition == 1):
        path = glob.glob(DART_WOWK)
    for race in range(len(path)):
        df = pd.read_csv(path[race], header=None)
        df[7] = make_ground_index(condition)
        df.to_csv(path[race], header=None, index=None)
        # shutil.move(path[race], race_path)
