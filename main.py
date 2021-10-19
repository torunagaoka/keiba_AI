import configparser
import datetime

from keiba_common.search import search_number_of_times_held
from keiba_common.search import search_number_of_days
from keiba_common.search import search_number_of_race
from keiba_common.search import get_race_info
# from keiba_common.csv import make_race_csv

from utils.url import create_url

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('./conf/config.ini', encoding='utf-8')

# config.iniから値取得
year = config_ini.get('DEFAULT', 'YEAR')
BASE_URL = config_ini.get('DEFAULT', 'BASE_URL')
RACE_PATH = config_ini.get('DEFAULT', 'RACE_PATH')
HORCE_PATH = config_ini.get('DEFAULT', 'HORCE_PATH')

# 馬名を取得し、馬ごとにcsvを作成する。
# その際、レースデータも取得する
for where in range(1, 11):
    # maxのmanyを取得する
    max_many = search_number_of_times_held(BASE_URL, year, where)
    for many in range(1, max_many):
        max_day = search_number_of_days(BASE_URL, year, where, many)
        for day in range(1, max_day):
            max_race = search_number_of_race(BASE_URL, year, where, many, day)
            for race in range(1, max_race):
                url = create_url(BASE_URL, year, where, many, day, race)
                print(datetime.datetime.now())
                print(url)
                # レースのcsvを作成する
                get_race_info(url, where)

