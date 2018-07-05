
from umihico_commons.chrome_wrapper import Chrome
from traceback import print_exc


def _strip_proxy(proxy):
    for replace in [' ', "　", "\n", "\t", "\xa0", ]:
        proxy = proxy.replace(replace, '')
    proxy = proxy.strip()
    return proxy


def _is_proxy(proxy):
    return True


def _strip_proxy_list(proxy_list):
    stripped_proxy_list = [_strip_proxy(proxy) for proxy in proxy_list]
    ok_proxy_list = [
        proxy for proxy in stripped_proxy_list if _is_proxy(proxy)]
    return ok_proxy_list


def get_cybersyndrome():
    chrome = Chrome()
    url = "http://www.cybersyndrome.net/"
    chrome.get(url)
    anonymous_page_link_xpath = "//td[contains(.,'Anonymous') and .//following-sibling::td[contains(.,'ユーザのIPアドレスを含む環境変数を出力しないプロキシ')]]"
    chrome.xpath(anonymous_page_link_xpath)[0].click()
    proxy_list_xpath = "//ol/li/a"
    proxy_elements = chrome.xpath(proxy_list_xpath)
    anonymous_proxy_list = [e.text for e in proxy_elements]
    anonymous_proxy_list = _strip_proxy_list(anonymous_proxy_list)
    return anonymous_proxy_list


def get_freeproxylists():
    chrome = Chrome()
    url = "http://www.freeproxylists.net/ja/?c=&pt=&pr=&a%5B%5D=1&a%5B%5D=2&u=0"
    chrome.get(url)
    all_anonymous_proxy_list = []
    while True:
        try:
            trs_xpath = "//table[@class='DataGrid']/tbody/tr"
            trs = chrome.xpath(trs_xpath)
            header_names = [td.text for td in trs[0].xpath("./td")]
            ideal_names = ["IPアドレス", 'ポート', 'プロトコル', '匿名性', '国',
                           '地域', '市', '稼働率', '応答速度', '転送速度', ]
            for ideal, actual in zip(ideal_names, header_names):
                if ideal != actual:
                    raise Exception(f"{ideal_names},{header_names}")
            for tr in trs[1:]:
                td_texts = [td.text for td in tr.xpath('./td')]
                dict_ = {name: text for name,
                         text in zip(ideal_names, td_texts)}
                if "Anonymous" in dict_["匿名性"]:
                    ip = dict_["IPアドレス"]
                    port = dict_["ポート"]
                    proxy = f'{ip}:{port}'
                    anonymous_proxy_list.append(proxy)
            nexts = chrome.xpath("//div[@class='page']/a[contains(.,'次へ')]")
            if len(nexts) > 0:
                nexts[0].click()
            else:
                break
            anonymous_proxy_list = _strip_proxy_list(anonymous_proxy_list)
            all_anonymous_proxy_list.extend(anonymous_proxy_list)
        except (Exception, ) as e:
            print_exc()
            break
    return all_anonymous_proxy_list


def save_scrapped_proxy():
    from umihico_commons.xlsx_wrapper import to_xlsx
    anonymous_proxy_list = []
    try:
        anonymous_proxy_list.extend(get_cybersyndrome())
    except (Exception, ) as e:
        print_exc()
    try:
        anonymous_proxy_list.extend(get_freeproxylists())
    except (Exception, ) as e:
        print_exc()
    rows = [[p, ] for p in anonymous_proxy_list]
    to_xlsx("proxy.xlsx", rows)


if __name__ == '__main__':
    save_scrapped_proxy()
