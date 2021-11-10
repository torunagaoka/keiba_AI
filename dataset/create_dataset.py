import pandas as pd

from dataset.list import one_hot_list
from dataset.list import one_hot_condition_list


def make_dataset(race_data_path, horse_data_path,
                 horse_name, father_list,
                 mother_father_list, jokey_list):
    # csvのファイル名を取得
    csv_file_name = race_data_path.split('/')[-1]
    # レースIDの取得
    race_id = csv_file_name[:-4]
    # 馬のデータを読み込む
    horse_data_path = horse_data_path + horse_name + '.csv'
    horse_df = pd.read_csv(horse_data_path)
    num = 0
    for i in range(len(horse_df)):
        if (horse_df.at[i, 'レースID'] == race_id):
            num = i
            break
    # 3走分作成する
    csv_out_list = dataset(num, horse_data_path, father_list, mother_father_list, jokey_list)
    return csv_out_list


def dataset(num, horse_data_path, father_list, mother_father_list, jokey_list):
    default_header = ['頭数', '枠番', '馬番', 'オッズ', '人気', '着順',
                      '斤量', '条件', '距離', '良', '稍', '重', '不',
                      '走破タイム', '着差', '上がり', '馬体重', '増減',
                      '賞金加算', '馬場指数', 'スピード指数']
    # 出力するリストの初期化
    header = []
    csv_out_list = []
    df = pd.read_csv(horse_data_path)
    father = df.at[0, '父']
    mother_father = df.at[0, '母父']
    # one_hotした父のリスト
    father_list_content = one_hot_list(father_list, father, 0)
    # one_hotした母父のリスト
    mother_father_list_content = one_hot_list(mother_father_list, mother_father, 1)
    # ヘッダー、CSVで出力するものを父、母父追加
    header += father_list
    header += mother_father_list
    csv_out_list += father_list_content
    csv_out_list += mother_father_list_content
    # defalutのリストとジョッキーのリストを追加
    header += (default_header + jokey_list) * 3
    if (num >= 3):
        csv_out_list += make_csv_out_list(num+1, num-2, df, jokey_list)
    elif(num == 2):
        csv_out_list += make_csv_out_list(num+1, num-1, df, jokey_list)
        csv_out_list += [0] * len(default_header)
        csv_out_list += [0] * len(jokey_list)
    elif(num == 1):
        csv_out_list += make_csv_out_list(num+1, num, df, jokey_list)
        csv_out_list += [0] * len(default_header)
        csv_out_list += [0] * len(jokey_list)
        csv_out_list += [0] * len(default_header)
        csv_out_list += [0] * len(jokey_list)
    elif (num == 0):
        csv_out_list = [0] * len(header)
    return csv_out_list


def make_csv_out_list(num, end_num, df, jokey_list):
    csv_out_list = []
    for i in reversed(range(end_num, num)):
        # 頭数
        csv_out_list.append(df.at[i-1, '頭数'])
        # 枠番
        csv_out_list.append(df.at[i-1, '枠番'])
        # 馬番
        csv_out_list.append(df.at[i-1, '馬番'])
        # オッズ
        csv_out_list.append(df.at[i-1, 'オッズ'])
        # 人気
        csv_out_list.append(df.at[i-1, '人気'])
        # 着順
        result = str(df.at[i-1, '着順'])
        if (len(result) > 2):
            result = result.split('(')[0]
        csv_out_list.append(result)
        # 斤量
        csv_out_list.append(df.at[i-1, '斤量'])
        # 条件(0⇨芝、1⇨ダート)
        csv_out_list.append(df.at[i-1, '条件'])
        # 距離
        csv_out_list.append(df.at[i-1, '距離'])
        # 馬場状態
        condition_list = one_hot_condition_list(df.at[i-1, '馬場状態'])
        csv_out_list += condition_list
        # 走破タイム
        csv_out_list.append(df.at[i-1, '走破タイム'])
        # 着差
        csv_out_list.append(df.at[i-1, '着差'])
        # 上がり
        csv_out_list.append(df.at[i-1, '上がり'])
        # 馬体重
        csv_out_list.append(df.at[i-1, '馬体重'])
        # 増減
        csv_out_list.append(df.at[i-1, '増減'])
        # 賞金加算
        prize_money = df.at[i-1, '賞金加算'].replace(',', '')
        csv_out_list.append(float(prize_money))
        csv_out_list.append(float(df.at[i-1, '馬場指数']))
        # スピード指数
        csv_out_list.append(float(df.at[i-1, 'スピード指数']))
        # 騎手
        jokey = df.at[i-1, '騎手']
        one_hot_jokey_list = one_hot_list(jokey_list, jokey, 2)
        csv_out_list += one_hot_jokey_list
    return csv_out_list

