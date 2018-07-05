
from proxies import ip_list
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from umihico_commons.requests_wrapper import get_with_proxy
from threading import Thread
from queue import Queue, LifoQueue
from time import sleep
import scrap_closed_list
from lxml.html import fromstring
import datetime
example_cats_dict = {
    'パーツ': "26322",
    'アクセサリー': "26320",
    'カーナビ': "23879",
    'メンテナンス': "26092",
    'カーオーディオ': "23852",
    'カタログ、パーツリスト、整備書': "2084005545",
    '自動車関連グッズ': "2084005546",
    '工具': "24650",
    'セキュリティ': "2084005799",
    'ETC': "2084048326",
    'セーフティ': "2084005798", }


example_NG_NAMES = [
    "azzurri_produce",
    "azzurri_shop",
    "world_wing_shop",
    "min_min_min7007",
    "sss_sss0101",
    "nanananani0810",
    "world_wing_shop2",
    "fourms_shop",
    "middlereus",
    "carparts003",
    "zzzz_yumo",
    "bnr3234gc10",
    "yous_shop",
    "yous_shop_net",
    "saito0204sp",
    "t_r_s_0204",
    "taro_zumi",
    "a_next_shop",
    "plum_shop_net",
    "topsense_brake",
    "carparts003",
    "a_ria_net",
    "office_k_1314",
    "daitouryou7",
    "takeboo_net",
    "bigbird_7jp",
    "pearl_line_go",
    "gekiyasuitibanya",
    "itatuka",
    "partstec2",
    "partstec3",
    "motorpower4",
    "wzyzzyzw",
    "motorpower6",
    "motorpower7", ]


def next_page_url_generator(base_url, first_i=1, n=100):
    cnt = first_i
    while True:
        if cnt == 1:
            url = base_url
        else:
            url = base_url + f"&b={cnt}"
        cnt += n
        yield url


def mixed_cat_url_generator(cat_ids):
    base_urls = [
        f"https://auctions.yahoo.co.jp/closedsearch/closedsearch?ei=UTF-8&n=100&auccat={cat_id}&istatus=1&s1=bids&o1=a" for cat_id in cat_ids]
    next_page_url_gens = [next_page_url_generator(
        base_url) for base_url in base_urls]
    while True:
        for next_page_url_gen in next_page_url_gens:
            yield next(next_page_url_gen)


def test_mixed_cat_url_generator():
    urls = mixed_cat_url_generator(cat_ids=example_cats_dict.values())
    from time import sleep
    for url in urls:
        print(url)
        sleep(0.5)


def _threading_pages_thread(proxy, url_queue, res_queue):
    sleep_time = 10
    while True:
        url = url_queue.get()
        try:
            res = get_with_proxy(url, proxy)
            lxml_root = fromstring(res.text)
            dictinfo_list = scrap_closed_list.parse(lxml_root)
            for d in dictinfo_list:
                d["searched_url"] = url
                for key, value in d.items():
                    if "https://" in value:
                        d[key] = value.replace("https://", "")
        except (Exception, ) as e:
            url_queue.put(url)
            sleep_time * 2
            sleep(sleep_time)
        else:
            print(url)
            res_queue.put(dictinfo_list)
            sleep_time = 0


def _url_adder(url_queue):
    urls = mixed_cat_url_generator(cat_ids=example_cats_dict.values())
    for url in urls:
        while True:
            if url_queue.empty():
                url_queue.put(url)
                break
            else:
                sleep(0.1)


def filter_dictinfo(dictinfo):
    if dictinfo['seller_name'] in example_NG_NAMES:
        return False
    month_str, day_str = dictinfo['end_date_raw_text'].split('/')
    closed_day = datetime.date(2018, int(month_str), int(day_str))
    # print(closed_day)
    today = datetime.date.today()
    dt_days = (today - closed_day).days
    if dt_days <= 30:
        return True
    else:
        return False


def test_filter_dictinfo():
    test_dict = {'end_date_raw_text': '07/05',
                 'end_time_raw_text': '14:10',
                 'image_url': 'https://wing-auctions.c.yimg.jp/sim?furl=auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0407/users/65e56ad7f7d6aac52da6a078b34c6c6f08956b6a/i-img600x450-1530665135x5a71l37312.jpg&dc=1&sr.fs=20000',
                 'raw_category': 'カテゴリメルセデス・ベンツ用>エンジン、過給器>エンジン部品',
                 'seller_name': 'lenexs_parts',
                 'title': 'エンジンマウント左右セット+ミッションマウントベンツW202W203W210W211C180C200C220C230C280E280E3202102400217',
                 'url': 'https://page.auctions.yahoo.co.jp/jp/auction/e285519723'}
    print(filter_dictinfo(test_dict))


def filter_dictinfo_list(dictinfo_list):
    ok_dictinfos = [d for d in dictinfo_list if filter_dictinfo(d)]
    return ok_dictinfos


def threading_pages():
    url_queue = LifoQueue()
    res_queue = Queue()
    for p in ip_list:
        Thread(target=_threading_pages_thread,
               args=(p, url_queue, res_queue)).start()
    Thread(target=_url_adder,  args=(url_queue,)).start()
    rows = []
    saved_row_count = 1000
    for dictinfo_list in iter(res_queue.get, None):
        ok_dictinfos = filter_dictinfo_list(dictinfo_list)
        new_rows = []
        for ok_dictinfo in ok_dictinfos:
            sorted_list_ = sorted(
                list(ok_dictinfo.items()), key=lambda x: x[0])
            only_values = [x[1] for x in sorted_list_]
            new_rows.append(only_values)
            # print(only_values)
        rows.extend(new_rows)
        print(len(rows))
        if len(rows) > saved_row_count:
            try:
                to_xlsx("closed_itemlist.xlsx", rows)
            except (Exception, ) as e:
                print(e)
            saved_row_count += 5000


if __name__ == '__main__':
    # test_filter_dictinfo()
    threading_pages()
    # test_mixed_cat_url_generator()
