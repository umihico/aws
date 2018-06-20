from umihico_commons.chrome_wrapper import Chrome
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from umihico_gist.google_search import search_keyword
from tqdm import tqdm


def _load_data():
    filename = "search_words.xlsx"
    rows = load_xlsx(filename)
    keywords = [row[0] for row in rows]
    return keywords


def main():
    keywords = _load_data()
    for i, keyword in tqdm(enumerate(keywords)):
        print(i, keyword)
        filename_num = str(i).zfill(3)
        filename = f"{filename_num}{keyword}.xlsx"
        result = search_keyword(keyword)
        to_xlsx(filename, result)


if __name__ == '__main__':
    main()
