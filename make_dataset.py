import configparser
import glob

from dataset.csv import remove_duplicate
from dataset.csv import add_ground_speed_index
# from dataset.create_dataset import make_dataset
from dataset.list import make_father_list
from dataset.list import make_jokey_list

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('./conf/config.ini', encoding='utf-8')

# config.iniから値取得
race_data_path = config_ini.get('DATASET', 'RACE_DATA_PATH')
horce_data_path = config_ini.get('DATASET', 'HORCE_DATA_PATH')
dataset_path = config_ini.get('DATASET', 'DATASET_PATH')

# 馬のデータを綺麗にする
# print('馬のデータを綺麗にしてる')
horce_path_list = glob.glob(horce_data_path + '*.csv')
# for i in range(len(horce_path_list)):
#     if(i % 5000 == 0):
#         print('{}件'.format(i))
#     remove_duplicate(horce_path_list[i])

# 馬場指数、スピード指数を馬データに追加する
# print('馬場指数、スピード指数を馬データに追加中')
# for j in range(len(horce_path_list)):
#     if(j % 5000 == 0):
#         print('{}件'.format(j))
#     add_ground_speed_index(horce_path_list[j], race_data_path)

# 父、母父のリストを作成する
print('父、母父のリストを作成中')
father_list, mother_father_list = make_father_list(horce_data_path)
print(father_list)
print('--------------')
print(mother_father_list)
print('--------------')

# ジョッキーのリストを作成する
print('ジョッキーのリストを作成中')
jokey_list = make_jokey_list(horce_data_path)
print(jokey_list)

# データセットを作成する
# race_path_list = glob.glob(race_data_path + '*.csv')
# for k in range(len(race_path_list)):
#     make_dataset(race_path_list[k])


"""
3走前まで使用する

・前回との変更点
①2017のデータを過去走として使用する（学習はしない）
②one-hotに関しては、一連の流れで行う（前回は辞書をベタ書き）
③馬場指数／スピード指数に関してはもう求めているのでレースIDで引っ掛かれば見つかる
"""