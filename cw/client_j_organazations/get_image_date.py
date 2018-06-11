
from umihico_commons.csv_wrapper import xlsx_to_list_of_list, xlsx_from_list_of_list
from tqdm import tqdm
from urllib import request
import re


def get_all_date():
    list_of_list = xlsx_to_list_of_list("urls.xlsx")
    urls = [list_[2] for list_ in list_of_list]
    urls = urls[9000:]
    output = []
    cnt = 0
    for url in tqdm(urls):
        cnt += 1
        date = get_date(url)
        print(date)
        output.append([url, date])
        if cnt > 1000 or url == urls[-1]:
            xlsx_from_list_of_list("dates.xlsx", output)
            cnt = 0


def get_date(url):
    try:
        date_timestamp = _headers_to_last_modified_date(request.urlopen(
            url, timeout=5).headers['last-modified'])
    except (Exception, ) as e:
        # raise
        return "not found"
    return date_timestamp


def _headers_to_last_modified_date(date_str='Thu, 02 Feb 2017 14:44:07 GMT'):
    pattern = r"[0-9]{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9]{4}"
    re_date_str = re.search(pattern, date_str).group()
    day_str, month_str, year_str = re_date_str.split()
    month_strs = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    month_nums = '01 02 03 04 05 06 07 08 09 10 11 12'.split()
    month_num = dict(zip(month_strs, month_nums))[month_str]
    date_str = '/'.join([year_str, month_num, day_str])
    return date_str


def test_get_date():
    url = "http://www.chibabank.co.jp/assets/img/company/info/outline/orgchart/index/index_il001.gif"
    print(get_date(url))


if __name__ == '__main__':
    get_all_date()
