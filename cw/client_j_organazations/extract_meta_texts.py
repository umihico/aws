from umihico_commons.chrome_wrapper import Chrome, Keys
from umihico_commons.google_search import extract_meta_texts
import sys
from traceback import format_exc
from time import sleep
import os


def _gen_url(i):
    print('url', i)
    list_of_list = csv_wrapper.xlsx_to_list_of_list("combined_names.xlsx")
    search_words = [x[0] for x in list_of_list]
    if i >= len(search_words):
        return False
    search_word = search_words[i]
    if len(search_word) < 5:
        return False
    url = f"https://www.google.co.jp/search?q={search_word}&tbm=isch"
    print(search_word)
    return url


def _save_as_excel(i, raw_meta_texts):
    print('saving as excel...')
    filename = f'result/raw_meta_texts{i}.xlsx'.replace('/', os.sep)
    list_of_list = map(lambda x: [x, ], raw_meta_texts)
    csv_wrapper.xlsx_from_list_of_list(filename, list_of_list)


def create_filtered_url():
    hpurl_base_dict = {}
    extract_urls_generator = _extract_urls_generator()
    for urls in extract_urls_generator:
        if 'organization' not in ''.join(urls):
            continue
        image_url, hp_url = urls
        old_image_url = hpurl_base_dict[hp_url] if hp_url in hpurl_base_dict else 'dummy'
        new_image_url = old_image_url if 'organization' in old_image_url else image_url
        hpurl_base_dict[hp_url] = new_image_url
    texts = ['\t'.join([str(i), hp_url, image_url]) for i, (hp_url,
                                                            image_url) in enumerate(hpurl_base_dict.items())]
    combined_text = '\n'.join(texts)
    with open('urls.txt', 'w') as f:
        f.write(combined_text)


def _get_filenames():
    abspath_this = os.path.abspath(__file__)
    dirpath_here = os.path.dirname(abspath_this)
    meta_texts_dir = os.path.join(dirpath_here, 'result')
    return list(map(lambda x: os.path.join(meta_texts_dir, x),  os.listdir(meta_texts_dir)))


def _raw_meta_text_generator():
    filenames = _get_filenames()
    for filename in filenames:
        xlsx = csv_wrapper.xlsx_to_list_of_list(filename)
        yield from _raw_meta_text_generator_xlsx(xlsx)


def _raw_meta_text_generator_xlsx(xlsx):
    for row in xlsx:
        raw_meta_text = row[0]
        yield raw_meta_text


def _extract_urls_generator():
    raw_meta_text_generator = _raw_meta_text_generator()
    for meta_text in raw_meta_text_generator:
        dict_ = json.loads(meta_text)
        image_url, hp_url = _meta_dict_to_urls(dict_)
        yield image_url, hp_url


if __name__ == '__main__':
    args = sys.argv
    this_filename, i = args
    url = _gen_url(int(i))
    if not url:
        return
    raw_meta_texts = get_raw_meta_texts(url)
    _save_as_excel(i, raw_meta_texts)
    with open(f'result_report.txt', 'a') as f:
        text = f'index{i} wrote {len(raw_meta_texts)} meta datas\n'
        f.write(text)
        print(text)
