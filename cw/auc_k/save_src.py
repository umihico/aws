from umihico_commons.chrome_wrapper import Chrome
import codecs
if __name__ == '__main__':
    c = Chrome()
    # c.get("https://auctions.yahoo.co.jp/closedsearch/closedsearch?select=06&ei=UTF-8&n=100&auccat=26318&istatus=1")
    # with codecs.open('src0.txt', 'w', 'utf-8') as f:
    #     f.writelines(c.page_source)
    c.get("https://page.auctions.yahoo.co.jp/jp/auction/w220186143")
    with codecs.open('src1.txt', 'w', 'utf-8') as f:
        f.writelines(c.page_source)
