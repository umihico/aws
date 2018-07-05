try:
    from scraping_common import lxmls_to_onetext, strip_string
except (Exception, ) as e:
    from .scraping_common import lxmls_to_onetext, strip_string


def beautify_raw_dict(raw_info_dict):
    info_dict = {}
    for key, value in raw_info_dict.items():
        new_key = strip_string(key)
        new_value = strip_string(value)
        info_dict[new_key] = new_value
    return info_dict


def parse(lxml_root):
    prices_trs = lxml_root.xpath(
        "//div[@class='untHead' and contains(.,'商品の情報')]/following-sibling::div[contains(@class,'untBody')]//div[contains(@class,'untTaxPrice')]//table")[0].xpath("./tbody/tr")
    details_trs = lxml_root.xpath("//div[./p[contains(.,'詳細情報')]]//tr")
    seller_trs = lxml_root.xpath(
        "//div[@class='untHead' and contains(.,'出品者の情報')]/following-sibling::div[contains(@class,'untBody')]//table")[0].xpath(".//tr")
    payment_trs = lxml_root.xpath(
        "//div[@class='untHead' and contains(.,'支払いについて')]/following-sibling::div[contains(@class,'untBody')]//table")[0].xpath(".//tr")
    shipping_trs = lxml_root.xpath(
        "//div[@class='untHead' and contains(.,'送料、商品の受け取りについて')]/following-sibling::div[contains(@class,'untBody')]//table")[0].xpath(".//tr")
    raw_info_dict = {}
    for trs in [prices_trs, details_trs, seller_trs, payment_trs, shipping_trs]:
        chunk_info_dict = {lxmls_to_onetext(
            tr.xpath(".//th")): lxmls_to_onetext(tr.xpath(".//td")) for tr in trs}
        raw_info_dict.update(chunk_info_dict)
    info_dict = beautify_raw_dict(raw_info_dict)
    info_dict["bid_count"] = lxml_root.xpath(
        "//b[@property='auction:Bids']")[0].text_content()
    info_dict["title"] = lxml_root.xpath(
        "//h1[@property='auction:Title']")[0].text_content()

    return info_dict


if __name__ == '__main__':
    from lxml.html import fromstring
    from pprint import pprint
    from umihico_commons.requests_wrapper import get
    url = "https://page.auctions.yahoo.co.jp/jp/auction/r250894053"
    res = get(url)
    print(res.text)
    lxml_root = fromstring(res.text)

    # [print(()) for x in lxml_root.xpath("//*[@property]")]
    [print(x.attrib["property"], x.text_content())
     for x in lxml_root.xpath("//*[@property]")]
    # print(lxml_root.xpath(
    #     "//script[@type='text/javascript']")[0].text_content())
    raw_info_dict = parse(lxml_root)
    pprint(raw_info_dict)
