import pandas as pd
import datetime

from keiba_common.csv import get_year_from_csv_name
from keiba_common.csv import get_month_from_csv_name
from keiba_common.csv import get_day_from_csv_name

HEADER = ['レースID', '頭数', '枠番', '馬番', 'オッズ', '人気', '着順',
          '騎手', '斤量', '条件', '距離', '馬場状態', '走破タイム', '着差',
          '上がり', '馬体重', '増減', '賞金加算', '父', '母父', '日付']


def remove_duplicate(csv_file_path):
    """
    ①馬のレースデータが重複している箇所があるため、それを取り除く
    ②父、母父を各レースデータに追加
    ③日付でソート
    ④ヘッダーをつけてCSVを書き換える

    Parameters
    ----------
    csv_file_path : str
        CSVのファイルのパス
    """
    df_work = pd.read_csv(csv_file_path)
    # 父・母父取得
    pedigree_list = []
    for column in df_work:
        pedigree_list.append(column)
    # レースデータ取得
    df = pd.read_csv(csv_file_path, header=None, skiprows=[0])
    df = df.drop_duplicates(subset=0)
    df[18] = pedigree_list[0]
    df[19] = pedigree_list[1]
    df[20] = 0
    # 日付でソートする
    for i in range(len(df)):
        year = int(get_year_from_csv_name(df.iat[i, 0]))
        month = int(get_month_from_csv_name(df.iat[i, 0]))
        day = int(get_day_from_csv_name(df.iat[i, 0]))
        date = datetime.date(year, month, day)
        df.iat[i, 20] = date
    df[20] = pd.to_datetime(df[20])
    df = df.sort_values(20)
    df.to_csv(csv_file_path, header=HEADER, index=False)


def add_ground_speed_index(csv_file_path, race_data_path):
    """
    馬場指数とスピード指数をCSVファイルに追加する

    Parameters
    ----------
    csv_file_path : str
        CSVのファイルのパス（馬のデータ）
    race_data_path :str
        レースデータのパス
    """
    # 馬名を取得
    horse_name = csv_file_path.split('/')[-1][:-4]
    df = pd.read_csv(csv_file_path)
    # 馬場指数とスピード指数の初期化
    df['馬場指数'] = 0.0
    df['スピード指数'] = 0.0
    for i in range(len(df)):
        # レースIDを取得
        race_id = df.at[i, 'レースID']
        # レースファイルを取得
        race_file = race_data_path + race_id + '.csv'
        race_df = pd.read_csv(race_file, header=None)
        num = 0
        for j in range(len(race_df)):
            if (horse_name == race_df.iat[j, 0]):
                num = j
                break
        # 馬場指数を取得
        ground_index = race_df.iat[num, 7]
        df.at[i, '馬場指数'] = round(ground_index, 2)
        # スピード指数を取得
        speed_index = race_df.iat[num, 8]
        df.at[i, 'スピード指数'] = round(speed_index, 2)
    # CSVに出力する
    df.to_csv(csv_file_path, index=False)


# def write_dataset_csv():
    