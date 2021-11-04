import configparser
import datetime

from keiba_common.search import search_number_of_times_held
from keiba_common.search import search_number_of_days
from keiba_common.search import search_number_of_race
from keiba_common.csv import make_race_csv
from keiba_common.csv import write_horse_csv
from keiba_common.csv import make_odds_csv
from utils.url import create_url
from index.ground_index import ground_index_add
from index.speed_index import make_speed_index

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('./conf/config.ini', encoding='utf-8')

# config.iniから値取得
year = config_ini.get('DEFAULT', 'YEAR')
BASE_URL = config_ini.get('DEFAULT', 'BASE_URL')
RACE_PATH = config_ini.get('DEFAULT', 'RACE_PATH')
HORCE_PATH = config_ini.get('DEFAULT', 'HORCE_PATH')
ODDS_PATH = config_ini.get('DEFAULT', 'ODDS_PATH')

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
                # レースのcsvを作成する。その際、ファイル名も取得する。（レースIDとするため）
                file_name, soup, condition = make_race_csv(url, RACE_PATH, year, where, race)
                if (condition == 2):
                    pass
                else:
                    # 払い戻しを取得する
                    make_odds_csv(file_name, ODDS_PATH, soup)
                    # 馬の詳細を作成する
                    write_horse_csv(file_name, url, HORCE_PATH)
            # 馬場指数を作成する
            ground_index_add(0)
            ground_index_add(1)
            # スピード指数を作成する
            make_speed_index(0, RACE_PATH)
            make_speed_index(1, RACE_PATH)

