import pandas as pd
import glob
from datetime import datetime as dt
import shutil
import os

from utils.dic import return_base_time
from utils.dic import return_distance_correction
from utils.tools import time_to_sec
from keiba_common.csv import get_distance_from_csv_name
from keiba_common.csv import get_condition_from_csv_name
from keiba_common.csv import get_kaisai_from_csv_name

TURF_WORK = './work/芝/*.csv'
DART_WOWK = './work/ダート/*.csv'


def make_speed_index(condition, race_path):
    """
    スピード指数を求める
    スピード指数 ＝ ( 基準タイム － 走破タイム ) × 距離指数 ＋ 馬場指数 ＋ ( 斤量－５５) × ２ ＋ ８０

    Parameters
    ----------
    condition : int
        条件
    race_path : str
        レースデータの保存先

    Returns
    -------
    speed_index : int
        スピード指数
    """
    if (condition == 0):
        path = glob.glob(TURF_WORK)
    elif (condition == 1):
        path = glob.glob(DART_WOWK)
    for race in range(len(path)):
        # ファイル名を取得する
        file_name = os.path.split(path[race])[1]
        # 開催を取得する
        kaisai = get_kaisai_from_csv_name(file_name)
        # 距離を取得する
        distance = get_distance_from_csv_name(file_name)
        # 条件を取得する
        condition = get_condition_from_csv_name(file_name)
        # 基準タイム
        base_time = return_base_time(str(kaisai)+str(condition)+str(distance))
        # 距離指数
        distance_correction = return_distance_correction(str(condition)+str(distance))
        # 読み込む
        df = pd.read_csv(path[race], header=None)
        # スピード指数を求める
        speed_index_list = []
        for j in range(len(df)):
            run_time = dt.strptime(df.at[j, 2], '%M:%S.%f')
            run_time = time_to_sec(run_time)
            SPEED_INDEX =  10 * (base_time - run_time) * distance_correction + df.at[j, 7] + (df.at[j, 6] - 55) * 2 + 80
            speed_index_list.append(SPEED_INDEX)
        df[8] = speed_index_list
        df.to_csv(path[race], header=None, index=None)
        shutil.move(path[race], race_path)

