
from umihico_commons.csv_wrapper import xlsx_to_list_of_list, xlsx_from_list_of_list
from tqdm import tqdm
from urllib import request
import re


def get_all_date():
    list_of_list = xlsx_to_list_of_list("pic_texts.xlsx")
    output = []
    for url, text in tqdm(list_of_list):
        date = get_date(text)
        print(date)
        output.append([url, text, date])
    xlsx_from_list_of_list("pic_texts_dates.xlsx", output)


def get_date(text):
    try:
        date = _date_mining_in_text(text)
    except (Exception, ) as e:
        # raise
        return "not found"
    return date


def _date_mining_in_text(word):
    patterns = [r"\d{2,4}/\d{1,2}/\d{1,2}", r"\d{2,4}年\d{1,2}月\d{1,2}日"]
    dates = [*re.findall(patterns[0], word), *
             re.findall(patterns[1], word)]
    date = dates[0] if dates else 'not found'
    return date


def test_get_date():
    url = "http://www.chibabank.co.jp/assets/img/company/info/outline/orgchart/index/index_il001.gif"
    print(get_date(url))


if __name__ == '__main__':
    get_all_date()
