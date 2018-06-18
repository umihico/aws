
from umihico_gist.get_related_keywords import get_related_keywords
from umihico_commons.chrome_wrapper import Chrome
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from pprint import pprint
from tqdm import tqdm
from time import sleep
from itertools import zip_longest


def get_popular_keywords(data_path):
    data = load_xlsx(data_path)
    # pprint(data)
    popular_keywords = []
    for row in data[3:]:
        kw = row[0]
        try:
            min = float(row[3])
        except (Exception, ) as e:
            print(row)
        max = float(row[4])
        if min >= 1000:
            popular_keywords.append(kw)
    return popular_keywords


def gen_xlsx_format(popular_keywords):
    c = Chrome(headless=True)
    cols = []
    for i, kw in tqdm(enumerate(popular_keywords)):
        col = [kw, ]
        related_keywords = get_related_keywords(kw, c)
        col.extend(related_keywords)
        cols.append(col)
        print(kw, len(related_keywords))
    reversed_cols = list(zip_longest(*cols, fillvalue=''))
    to_xlsx('each_list.xlsx', reversed_cols)
    del reversed_cols
    all_keywords = []
    for col in cols:
        all_keywords.extend(col[1:])
    all_keywords.sort()
    to_xlsx('all_keywords.xlsx', [[kw, ] for kw in all_keywords])
    no_deplicate_all_keywords = list(set(all_keywords))
    no_deplicate_all_keywords.sort()
    to_xlsx('all_keywords_nodeplicate.xlsx', [
            [kw, ] for kw in no_deplicate_all_keywords])


def main(data_path='data.xlsx'):
    popular_keywords = get_popular_keywords(data_path)
    gen_xlsx_format(popular_keywords)


if __name__ == '__main__':
    main()
