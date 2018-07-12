from umihico_commons.functools import map_multithreading, load_from_txt
# from umihico_gist.get_address_regex.get_address_regex import get_address_regex_lxmltree
from requests import get
from lxml import html
import queue
import threading
import re
from tqdm import tqdm
import urllib
from pprint import pprint
from umihico_commons.xlsx_wrapper import to_xlsx


def get_url_dict():
    dicts = load_from_txt("wiki.txt")
    url_dict = {d['title']: d["外部リンク"] for d in dicts if "外部リンク" in d.keys()}
    return url_dict


def scrap_eigyosho(title, given_url):
    print(title, given_url)
    if given_url.startswith("www"):
        given_url = "http://" + given_url
    try:
        res = get(given_url)
    except (Exception, ) as e:
        return []
    link_kwargs = ["会社", "概要", "情報", "企業", "案内", "事業", "紹介",
                   "組織図", "グループ", "店舗", "事業", "一覧", "関連", "拠点", "営業所", ]
    try:
        lxml_ = html.fromstring(res.text)
    except (Exception, ) as e:
        return []
    links = lxml_.xpath("//a")
    links = [link for link in links if any(
        bool(kw in link.text_content()) for kw in link_kwargs)]
    links = {link.get("href"): link for link in links if link.get(
        "href") is not None and "#" not in link.get("href")}.values()
    lxmltree_dict = {given_url: lxml_, }
    for link in links:
        try:
            link_url = link.get("href")
            if link_url.startswith("/") or "://" not in link_url:
                link_url = urllib.parse.urljoin(given_url, link_url)
            lxmltree_dict[link_url] = html.fromstring(get(link_url).text)
            print(link_url)
        except (Exception, ) as e:
            pass
    result_rows = get_eigyousho(lxmltree_dict)
    final_rows = [(title, given_url, *row) for row in result_rows]
    return final_rows


add_compiled = re.compile(
    "...??[都道府県].+?[市区町村].+")
tel_compiled = re.compile(
    r'[\(]{0,1}[0-9]{2,4}[\)\-\(]{0,1}[0-9]{2,4}[\)\-]{0,1}[0-9]{3,4}')


def get_eigyousho(lxmltree_dict):
    result_rows = []
    for url, lxmltree in lxmltree_dict.items():
        eigyousho_rows = get_eigyousho_func(lxmltree)
        result_rows.extend([(url, *row)for row in eigyousho_rows])
    return result_rows


def get_eigyousho_func(lxmltree):
    element_rows = []
    text_dict = {}
    all_detected_words = []
    for i, text in enumerate(lxmltree.itertext()):
        adds = add_compiled.findall(text)
        tels = tel_compiled.findall(text)
        all_detected_words.extend(tels)
        all_detected_words.extend(adds)
        row = (i, text, adds, tels)
        text_dict[i] = text
        element_rows.append(row)
    add_exist_index = [i for i, text, ad_list,
                       tel_list in element_rows if len(ad_list) > 0]
    if len(add_exist_index) <= 1:
        return []
    add_min_distance = min([aftr_i - prev_i for prev_i,
                            aftr_i in zip(add_exist_index, add_exist_index[1:])])
    tel_exist_index = [i for i, text, ad_list,
                       tel_list in element_rows if len(tel_list) > 0]
    if len(tel_exist_index) <= 1:
        return []
    tel_min_distance = min([aftr_i - prev_i for prev_i,
                            aftr_i in zip(tel_exist_index, tel_exist_index[1:])])
    min_distance = min([add_min_distance, tel_min_distance])
    result_rows = []
    for i, text, adds, tels in element_rows:
        if len(adds) + len(tels) > 0:
            texts_between = " ".join([text_dict.get(i - j, "")
                                      for j in range(min_distance)])
            for all_detected_word in all_detected_words:
                texts_between = texts_between.replace(
                    all_detected_word, "").replace("  ", ' ')
            texts_between = texts_between[:100]
            row = (texts_between, ",".join(adds), ",".join(tels))
            result_rows.append(row)
    # pprint(result_rows)
    return result_rows


def main(command_int=-1):
    url_dict = get_url_dict()
    # for title, url in tqdm(list(url_dict.items())[:100]):
    args_rows = [(title, url) for title, url in url_dict.items()]
    if command_int == -1:
        raise Exception(f"command_int:{command_int}")
    l_slice_index = int(command_int) * 500
    r_slice_index = l_slice_index + 500
    args_rows = args_rows[l_slice_index:r_slice_index]
    filename = f"eigyousho_final{command_int}.xlsx"
    rows_list = map_multithreading(scrap_eigyosho, args_rows=args_rows)
    excel_rows = []
    for rows in rows_list:
        excel_rows.extend(rows)
    to_xlsx(filename, excel_rows)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
