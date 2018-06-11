from umihico_commons.chrome_wrapper import Chrome
from umihico_commons.csv_wrapper import xlsx_to_list_of_list, xlsx_from_list_of_list


# def get_info(c):
# xpath_ = "//div[@class='co-detail-tbl-row']"
# rows = c.xpath(xpath_)
#     dict_ = {}
#     for row in rows:
#         rows.find_element_by_xpath

def test_access():
    url = "https://b2b-ch.infomart.co.jp/company/search/list.page?1942&chi=23&cha=13"
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.keys import Keys
    c = Chrome()
    actions = ActionChains(c)
    c.get(url)
    links = c.find_elements_by_xpath("//a[@id='lnkCompanyName']")
    main_tab = c.current_window_handle
    for link in links:
        actions.key_down(Keys.CONTROL).click(
            link).key_up(Keys.CONTROL).perform()
        while True:
            try:
                c.switch_tab(index=1)
                xpath_ = "//div[@class='co-detail-tbl-row']"
                rows = c.find_elements_by_xpath(xpath_)
                if len(rows) == 0:
                    raise

                text = c.find_element_by_xpath("//div[@class='main-area']")
                print(text.text)

                # tab.close()
                c.close()
                # len_ = len(c.window_handles)
                # while True:
                #     c.close_tab()
                #     if len(c.window_handles) == 1:
                #         break
                c.switch_to_window(main_tab)
            except (Exception, ) as e:
                print(e)
            else:
                break
    c.quit()


if __name__ == '__main__':
    test_access()
