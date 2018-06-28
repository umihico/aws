from umihico_commons.chrome_wrapper import Chrome
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from selenium.webdriver.support.ui import WebDriverWait


def _every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)


def wait_download_end(chrome):
    WebDriverWait(chrome, 600).until(_every_downloads_chrome)


def gen_urls():
    example_url = "https://disclosure.edinet-fsa.go.jp/E01EW/BLMainController.jsp?uji.verb=W1E63021CXP002002DSPSch&uji.bean=ee.bean.parent.EECommonSearchBean&PID=W1E63021&TID=W1E63021&SESSIONKEY=1530163677547&lgKbn=2&pkbn=0&skbn=1&dskb=&askb=&dflg=0&iflg=0&preId=1&sec=&scc=&shb=&snm=&spf1=1&spf2=1&iec=&icc=&inm=&spf3=1&fdc=&fnm=&spf4=1&spf5=2&otd=120&cal=2&yer=2018&mon=4&psr=1&pfs=4&row=100&idx=0&str=&kbn=1&flg=&syoruiKanriNo="
    replace_target = "yer=2018&mon=4"
    search_list = [
        # (2017, 10),
        # (2017, 11),
        # (2017, 12),
        # (2018, 1),
        # (2018, 2),
        # (2018, 3),
        (2018, 4),
    ]
    urls = [example_url.replace(
        "yer=2018&mon=4", f"yer={year}&mon={month}") for year, month in search_list]
    return urls


def download(url):
    c = Chrome()
    c.get(url)
    download_xpath = "//input[@id='xbrlbutton']"
    nextpage_xpath = "//a[@href='#' and text()='次ページ']"
    while True:
        c.xpath(download_xpath)[0].click()
        alert = c.switch_to.alert
        alert.accept()
        next_buttons = c.xpath(nextpage_xpath)
        if len(next_buttons) > 0:
            next_buttons[0].click()
        else:
            break
    wait_download_end(c)


def main():
    urls = gen_urls()
    for url in urls:
        download(url)


if __name__ == '__main__':
    main()
