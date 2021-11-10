import pandas as pd
import glob


def make_father_list(horce_data_path):
    """
    父、母父の一意のリストを作成する
    その他も追加する

    Parameters
    ----------
    horce_data_path : str
        CSVのファイルのパス（馬のデータ）

    Returns
    -------
    father_list : list
        父名のリスト
    mother_father_list : list
        母父のリスト
    """
    father_list = []
    mother_father_list = []
    horce_path_list = glob.glob(horce_data_path + '*.csv')
    for i in range(len(horce_path_list)):
        df = pd.read_csv(horce_path_list[i])
        father_name = df.at[0, '父']
        mother_father_name = df.at[0, '母父']
        if (('父名_' + father_name) not in father_list):
            father_list.append('父名_' + father_name)
        if (('母父名_' + mother_father_name) not in mother_father_list):
            mother_father_list.append('母父名_' + mother_father_name)
    father_list.append('その他')
    mother_father_list.append('その他')
    return father_list, mother_father_list


def make_jokey_list(horce_data_path):
    """
    ジョッキーの一意のリストを作成する
    その他も作成する

    Parameters
    ----------
    horce_data_path : str
        CSVのファイルのパス（馬のデータ）

    Returns
    -------
    jokey_list : list
        ジョッキーのリスト
    """
    jokey_list = []
    horce_path_list = glob.glob(horce_data_path + '*.csv')
    for i in range(len(horce_path_list)):
        df = pd.read_csv(horce_path_list[i])
        for j in range(len(df)):
            jokey_name = df.at[j, '騎手']
            if (jokey_name not in jokey_list):
                jokey_list.append(jokey_name)
    jokey_list.append('その他')
    return jokey_list


def one_hot_list(list_header, name, contents):
    """
    父、母父、ジョッキーをone-hotするのを想定し作成
    リストに値がない場合はその他でone-hot

    Parameters
    ----------
    list_header : list
        ヘッダーとなるリスト
    name : str
        リストヘッダーから取得する名前
    content : int
        0⇨父のリストをone-hot
        1⇨母父のリストをone-hot
        2⇨ジョッキーのリストをone-hot

    Returns
    -------
    zero_list : list
        one-hotしたリスト
    """
    zero_list = [0] * len(list_header)
    if (contents == 0):
        try:
            index = list_header.index('父名_' + name)
        except ValueError:
            index = -1
    elif(contents == 1):
        try:
            index = list_header.index('母父名_' + name)
        except ValueError:
            index = -1
    elif(contents == 2):
        try:
            index = list_header.index(name)
        except ValueError:
            index = -1
    zero_list[index] = 1
    return zero_list


def one_hot_condition_list(value):
    """
    馬場状態をone-hot

    Parameters
    ----------
    value : str
        条件

    Returns
    -------
    zero_list : list
        one-hotしたリスト
    """
    condition_list = ['良', '稍', '重', '不']
    zero_list = [0, 0, 0, 0]
    index = condition_list.index(value)
    zero_list[index] = 1
    return zero_list

