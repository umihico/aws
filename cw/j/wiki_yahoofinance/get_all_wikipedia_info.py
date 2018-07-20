# from webscraping_commons.proxy.multithreading import multithreading
from umihico_commons.functools import map_multithreading
from umihico_commons.requests_wrapper import get_with_proxy
from umihico_gist.get_info_wikipedia.get_info_wikipedia import get_info_wikipedia
from umihico_gist.get_stock_info_yahoo.get_stock_info_yahoo import get_stock_info_yahoo, gen_url
from umihico_gist.get_anonymous_proxy.get_anonymous_proxy import get_anonymous_proxy
from umihico_gist.get_stock_metadata.get_stock_metadata import get_stock_metadata
from umihico_commons.functools import save_as_txt, load_from_txt
from lxml import html
from traceback import print_exc
import queue
from traceback import format_exc
from time import time


def yahoo_main():
    codes = _get_stock_codes()
    proxy_queue = queue.Queue()
    for proxy in load_proxy():
        proxy_queue.put((0, proxy))
    args_rows = [(code, proxy_queue) for code in codes]
    result_list = map_multithreading(job_func_yahoo, args_rows=args_rows)
    save_as_txt("yahoo_finace.txt", result_list)


def wikipedia_main():
    urls = _get_wiki_urls()
    proxy_queue = queue.PriorityQueue()
    for proxy in load_proxy():
        proxy_queue.put((1, proxy))
    # urls = list(urls)[:10]
    jobs = [(job_func_wiki, url) for url in urls]
    result = multithreading(proxies, jobs)
    save_as_txt("wiki.txt", result, mode='w')


def job_func_yahoo(code, proxy_queue):
    print(code, "start")
    start_time = time()
    urls = gen_url(code)
    while True:
        proxy_score, proxy = proxy_queue.get()
        print(proxy_score, proxy)
        try:
            responses = [get_with_proxy(url, proxy) for url in urls]
            lxmltrees = [html.fromstring(response.text)
                         for response in responses]
            try:
                result_dict = get_stock_info_yahoo(lxmltrees)
            except (Exception, ) as e:
                format_exc()
            result_dict['code'] = code
        except (Exception, ) as e:
            proxy_score += 10
        else:
            print(code, "end")
            proxy_queue.put((0, proxy))
            return result_dict
        proxy_queue.put((proxy_score, proxy))
        if time() - start_time > 300:
            return {}


def job_func_wiki(proxy, url):
    res = get_with_proxy(url, proxy)
    try:
        result = get_info_wikipedia(html.fromstring(res.text))
        print(result["title"])
    except (Exception, ) as e:
        result = {}
    return result


def save_proxy_local():
    proxys = get_anonymous_proxy()
    save_as_txt("proxys.txt", proxys, mode='w')


def load_proxy():
    return load_from_txt("proxys.txt")


def save_stock_metadata_local():
    stock_metadata = get_stock_metadata()
    save_as_txt("stock_metadata.txt", stock_metadata, mode='w')


def load_stock_metadata():
    return load_from_txt("stock_metadata.txt")


def _get_stock_codes():
    codes = [str(d["コード"])
             for d in load_stock_metadata() if d['市場・商品区分'] != 'ETF・ETN']
    return codes


def _get_wiki_urls():
    raw_merged_dict = {}
    for filename in ["public_company_urls.txt", "all_company_urls.txt"]:
        raw_merged_dict.update(load_from_txt(filename))
    urls = [url for name, url in raw_merged_dict.items()]
    urls = [url if url.startswith(
        "http") else "https://ja.wikipedia.org" + url for url in urls]
    nondeplicate_urls = set(urls)
    return nondeplicate_urls


if __name__ == '__main__':
    # save_proxy_local()
    yahoo_main()
    print("done")
