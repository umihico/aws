
from umihico_commons.requests_common import headers_dict_user_agent
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from requests import get
from PIL import Image
from io import BytesIO
import hashlib
from lxml.html import fromstring
from re import findall
from datetime import datetime, timedelta


# category = _to_list_category(raw_category)
# end_date = _to_date(end_date_raw_text, end_time_raw_text)


def get_image_hash(image):
    hash = hashlib.sha256(image.tobytes()).hexdigest()
    return hash


def get_image(image_url):
    image = Image.open(
        BytesIO(get(image_url, headers=headers_dict_user_agent).content))
    return image


def main():
    try:
        b = load_xlsx("place.xlsx")[0][0]
    except (Exception, ) as e:
        b = 1
    try:
        saved_data = load_xlsx("data.xlsx")
    except (Exception, ) as e:
        saved_data = []
    base_itemlist_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?select=06&ei=UTF-8&n=100&auccat=26318&istatus=1"
    urls = next_page_url_generator(base_itemlist_url, first_i=b)
    for url in urls:
        try:
            itemlist = parse(url)
        except (Exception, ) as e:
            from traceback import format_exc
            print(format_exc())
            break


def _date2text(datetime_):
    return datetime_.strftime("%Y%m%d%H%M")


def _text2date(text):
    s = "{0:-12d}".format(text)
    return datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]), hour=s[8:10], minute=s[10:12])


def _to_date(date_raw_text, time_raw_text):
    month, day = [int(x.strip()) for x in date_raw_text.split('/')]
    hour, minute = [int(x.strip()) for x in time_raw_text.split(':')]
    year = datetime.now().year
    date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    if date > datetime.now():
        date -= timedelta(years=1)
    str_date = _date2text(date)
    return str_date


def _to_list_category(category_raw_string):
    category_raw_string = category_raw_string.replace("\n", "__n__")
    category_raw_string = category_raw_string.replace("\xa0", "__xa0__")
    category_raw_string = category_raw_string.replace(
        "カテゴリ__n__", "", 1)
    # print(category_raw_string)
    raw_re_result = findall("__n__.+?__n__", category_raw_string)
    category_list = [x.replace("__n__", "")
                     for x in raw_re_result if x != '__n____xa0__>__xa0____n__']
    if len(category_list) == 0:
        raise Exception(f"{[category_raw_string,]}")
    return category_list

    # text = get(itemlist_url, headers=headers_dict_user_agent).text
    # lxml_root = fromstring(text)


if __name__ == '__main__':
    base_itemlist_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?select=06&ei=UTF-8&n=100&auccat=26318&istatus=1"
    urls = next_page_url_generator(base_itemlist_url, n=100)
    for i, url in enumerate(urls):
        if i > 2:
            break
        itemlist = parse(url)
        print([x[1] for x in itemlist])
        print(itemlist)
        print(len(itemlist))
    raise
    from pprint import pprint
    print(itemlist)
    print(max([len(list_) for list_ in itemlist]))
    print(min([len(list_) for list_ in itemlist]))
    image_url = "https://wing-auctions.c.yimg.jp/sim?furl=auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr520/auc0406/users/4/0/9/6/silverstar_car-imgbatch_1529893712/500x466-2013101900004.jpg&dc=1&sr.fs=20000"
    image = get_image(image_url)
    hash = get_image_hash(image)
    print(hash)
