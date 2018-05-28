from chrome_wrapper import Chrome, Keys
import csv_wrapper


def gen_urls_func(i):
    list_of_list = csv_wrapper.xlsx_to_list_of_list("combined_names.xlsx")
    search_word = [x[0] for x in list_of_list][i]
    del list_of_list
    url = f"https://www.google.co.jp/search?q={search_word}&tbm=isch"
    c = Chrome()
    c.get(url)
    image_xpath = "//a[@class='rg_l']/img"
    done_image_urls = set()
    done_hp_urls = set()
    soshikizu_bools = []
    results = []
    element_int = 0
    while True:
        image_elements = c.xpath(image_xpath)
        try:
            image_element = image_elements[element_int]
        except (IndexError, ) as e:
            try:
                c.xpath("//input[@id='smb']").click()
            except (Exception, ) as e:
                pass
            try:
                image_element = image_elements[element_int]
            except (IndexError, ) as e:
                break
        element_int += 1
        # if element_int > 300:
        #     raise StopIteration
        try:
            image_element.click()
        except (Exception, ) as e:
            break
        # sleep(0.1)
        divs = c.xpath_lxml("//div[@id='irc_cc']/div")
        # for image_url, hp_url, description in zip(image_urls, hp_urls, descriptoins):
        for div in divs:
            description = div.xpath(".//div[@class='irc_it']")
            image_url = div.xpath(".//img[@class='irc_mi']/@src")
            # //div[@id='irc_cc']/div[2]//img[@class='irc_mi']/@src
            hp_url = div.xpath(".//img[@class='irc_mi']/../@href")
            if max(map(len, [description, image_url, hp_url])) > 1:
                raise
            description = description[0].text_content() if len(
                description) > 0 else ""
            image_url = str(image_url[0]) if len(
                image_url) > 0 else ""
            hp_url = str(hp_url[0]) if len(hp_url) > 0 else ""
            if image_url in done_image_urls or hp_url in done_hp_urls:
                continue
            else:
                done_image_urls.add(image_url)
                done_hp_urls.add(hp_url)
            all_text = ''.join([image_url, hp_url, description])
            if 'organization' in all_text:
                soshikizu_bools.append(True)
                print(image_url)
                print(hp_url)
                print(search_word)
                print(i)
                results.append((image_url, hp_url))
            else:
                soshikizu_bools.append(False)
        len_soshikizu_bools = len(soshikizu_bools)
        len_okay_soshikizu_bools = len(list(filter(bool, soshikizu_bools)))
        if len(soshikizu_bools) > 100:
            soshikizu_bools.pop(0)
        rate = len_okay_soshikizu_bools / len_soshikizu_bools
        if len(soshikizu_bools) == 100 and rate < 0.1:
            break
        print(len_okay_soshikizu_bools,
              len_soshikizu_bools, round(rate, ndigits=3))
    c.quit()
    text = '\n'.join(
        [i + ',' + image_url + ',' + hp_url for image_url, hp_url in results]) + '\n'
    with open("results.txt", 'a') as f:
        f.write(text)


if __name__ == '__main__':
    import sys
    args = sys.argv
    this_filename, i = args
    gen_urls_func(int(i))
