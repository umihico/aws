from umihico_commons.chrome_wrapper import Chrome
from requests import get


def test():
    url = "http://shop.kitamura.jp/used/list.html?f%5B%5D=k3&q=4549292037692&n1c=3"
    res = get(url, params=None)
    print(res.text)
    # c=Chrome()
    # c.get(url)


if __name__ == '__main__':
    test()
