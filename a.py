from keiba_common.csv import make_race_csv
from utils.beautiful_util import init_beautifulsoup
from keiba_common.odds import get_tansho_fukusho
from keiba_common.odds import get_ren_sanren

horse_path = '/Users/nagaokatooru/Desktop/競馬AI_改訂版/ソース/データ/馬/2018/'
odds_path = '/Users/nagaokatooru/Desktop/競馬AI_改訂版/ソース/データ/オッズ/2018/'
aa = '/Users/nagaokatooru/Desktop/aa'
file_name = '2021札幌01200010053001'
url = 'https://race.netkeiba.com/race/result.html?race_id=201805010304'


make_race_csv(url, aa, 2018, 5, 4)


