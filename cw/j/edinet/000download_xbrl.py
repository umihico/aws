from umihico_commons.chrome_wrapper import Chrome, default_custom_desired_capabilities, default_custom_chrome_options
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
from time import sleep
from winsound import Beep
from traceback import print_exc


def test_proxy():
    c = Chrome(chrome_options=default_custom_chrome_options)
    c.get("http://cgi.members.interq.or.jp/tokyo/bell/cgi-bin/env.cgi")
    from time import sleep
    sleep(10)


def _every_downloads_chrome(driver):
    driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)


def wait_download_end(chrome):
    WebDriverWait(chrome, 600).until(_every_downloads_chrome)


def gen_monthly_urls():
    example_url = "https://disclosure.edinet-fsa.go.jp/E01EW/BLMainController.jsp?uji.verb=W1E63021CXP002002DSPSch&uji.bean=ee.bean.parent.EECommonSearchBean&PID=W1E63021&TID=W1E63021&SESSIONKEY=1530354755536&lgKbn=2&pkbn=0&skbn=1&dskb=&askb=&dflg=0&iflg=0&preId=1&xbr=on&sec=&scc=&shb=&snm=&spf1=2&sti=0050&sti=1050&sti=2050&sti=3050&sti=3100&sti=3150&sti=3200&sti=3250&sti=3300&sti=3350&sti=3400&sti=3450&sti=3500&sti=3550&sti=3600&sti=3650&sti=3700&sti=3750&sti=3800&sti=4050&sti=5050&sti=5100&sti=5150&sti=5200&sti=5250&sti=6050&sti=6100&sti=7050&sti=7100&sti=7150&sti=7200&sti=8050&sti=9050&spf2=1&iec=&icc=&inm=&spf3=1&fdc=&fnm=&spf4=1&spf5=2&otd=120&cal=2&yer=2017&mon=4&psr=1&pfs=5&row=100&idx=0&str=&kbn=1&flg=&syoruiKanriNo="
    replace_target = "yer=2017&mon=4"
    search_list = []
    search_list.extend([(2016, x) for x in range(6, 13)])
    search_list.extend([(2017, x) for x in range(1, 13)])
    search_list.extend([(2018, x) for x in range(1, 5)])
    urls = []
    urls.extend([example_url.replace(
        replace_target, f"yer={year}&mon={month}") for year, month in search_list])
    # 2017.3 is too many. devided by 2
    return urls


def download_all(monthly_url, c=None):
    c = c or Chrome()
    download_xpath = "//input[@id='xbrlbutton']"
    nextpage_xpath = "//a[@href='#' and text()='次ページ']"
    current_month_xpath = "//p[text()='決算期／提出期間を指定する']"
    c.get(monthly_url)
    c.find_element_by_xpath(current_month_xpath).click()
    # print(c.xpath_lxml("//p[@id='pageTop']/text()")[0])
    done_urls = []
    while True:
        print(c.current_url)
        done_urls.append(c.current_url)
        c.xpath(download_xpath)[0].click()
        # try:
        # except (Exception, ) as e:
        #     try:
        #         last_suceed_url = done_urls[-2]
        #     except (Exception, ) as e:
        #         last_suceed_url = monthly_url
        #     sleep(60)
        #     download_all(last_suceed_url)
        #     return
        sleep(3)
        c.switch_to.alert.accept()
        sleep(3)
        next_buttons = c.xpath(nextpage_xpath)
        if len(next_buttons) > 0:
            next_buttons[0].click()
        else:
            break
    wait_download_end(c)


def main():
    monthly_urls = gen_monthly_urls()
    c = Chrome()
    for i, monthly_url in enumerate(monthly_urls):
        download_all(monthly_url, c)


if __name__ == '__main__':
    # test_proxy()
    main()
