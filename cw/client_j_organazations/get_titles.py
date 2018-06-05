
from umihico_commons.csv_wrapper import xlsx_to_list_of_list, xlsx_from_list_of_list
from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_all_title():
    list_of_list = xlsx_to_list_of_list("urls.xlsx")
    urls = [list_[1] for list_ in list_of_list]
    output = []
    cnt = 0
    for url in tqdm(urls):
        cnt += 1
        title = get_title(url)
        print(title)
        output.append([url, title])
        if cnt > 1000:
            xlsx_from_list_of_list("titles.xlsx", output)
            cnt = 0


def get_title(url):
    res = get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    if soup.title is None:
        return ""
    else:
        return soup.title.string


def test_get_title():
    url = "https://qiita.com/Azunyan1111/items/9b3d16428d2bcc7c9406"
    print(get_title(url))


if __name__ == '__main__':
    get_all_title()
