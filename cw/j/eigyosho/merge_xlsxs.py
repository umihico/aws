from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from umihico_commons.functools import chunks
from tqdm import tqdm


def merge_xlsxs():
    merged_rows = [["企業名", "トップurl", "情報取得url", "周辺テキスト", "住所", "TEL"], ]
    for i in tqdm(range(0, 12)):
        filename = f"eigyousho_final{i}.xlsx"
        merged_rows.extend(load_xlsx(filename))
    merged_rows = [(title, shorten_url(top_url), shorten_url(page_url), text, ad, tel)
                   for title, top_url, page_url, text, ad, tel in merged_rows]
    for i, chunk_rows in enumerate(chunks(merged_rows, 30000)):
        to_xlsx(f"final{i}.xlsx", chunk_rows)


# Excel2010で65,530個を超えるハイパーリンクは挿入できない
# https://answers.microsoft.com/ja-jp/msoffice/forum/msoffice_excel-mso_winother-mso_2010/excel2010%E3%81%A765530%E5%80%8B%E3%82%92%E8%B6%85/c42e7a67-e691-4e5c-8d00-aa2db19ab5a1
def shorten_url(url):
    if len(url) > 250:
        url = url.replace("https:", '').replace("http:", '')
    return url


if __name__ == '__main__':
    merge_xlsxs()
