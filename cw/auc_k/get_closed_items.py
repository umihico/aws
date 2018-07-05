
from proxies import ip_list
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from umihico_commons.requests_wrapper import get_with_proxy
from threading import Thread
from queue import Queue, LifoQueue
from time import sleep
import scrap_closed_item
from lxml.html import fromstring


def load_urls():

    rows = load_xlsx("closed_itemlist.xlsx")
    urls = ["https://" + row[-1] for row in rows]
    return urls

# def filter_dictinfo(dictinfo):
#     if


def _threading_pages_thread(proxy, url_queue, res_queue):
    sleep_time = 10
    while True:
        url = url_queue.get()
        try:
            res = get_with_proxy(url, proxy)
            lxml_root = fromstring(res.text)
            dictinfo = scrap_closed_item.parse(lxml_root)
        except (Exception, ) as e:
            url_queue.put(url)
            sleep_time * 2
            sleep(sleep_time)
        else:
            print(url)
            res_queue.put(dictinfo)
            sleep_time = 0


def _url_adder(url_queue):
    urls = load_urls()
    for url in urls:
        while True:
            if url_queue.empty():
                url_queue.put(url)
                break
            else:
                sleep(0.1)


def save_dicts(dicts, filename):
    field_names = set()
    for dict_ in dicts:
        field_names.update(dict_.keys())
    rows = [list(field_names), ]
    for dict_ in dicts:
        row = [dict_.get(field_name, "") for field_name in field_names]
        rows.append(row)
    to_xlsx(filename, rows)


def threading_pages():
    url_queue = LifoQueue()
    res_queue = Queue()
    for p in ip_list:
        Thread(target=_threading_pages_thread,
               args=(p, url_queue, res_queue)).start()
    Thread(target=_url_adder,  args=(url_queue,)).start()
    dicts = []
    saved_row_count = 100
    for dictinfo in iter(res_queue.get, None):
        # if filter_dictinfo(dictinfo):
        print(len(dicts))
        dicts.append(dictinfo)
        if len(dicts) > saved_row_count:
            save_dicts(dicts, "closed_items.xlsx")
            saved_row_count += 100


if __name__ == '__main__':
    # print(load_urls())
    threading_pages()
