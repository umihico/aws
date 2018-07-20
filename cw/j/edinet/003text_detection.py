from umihico_commons.google_cloud_vision_api.request import get_text_dict
from umihico_commons.xlsx_wrapper import to_xlsx, load_xlsx
from umihico_commons.csv_wrapper import load_csv
from umihico_commons.functools import chunks
from tqdm import tqdm
from os import path as ospath
from pprint import pprint
from os import sep
from common_funcs import gen_path_list


def _get_saved_text_dict():
    try:
        rows = load_xlsx("003_images_text_dict.xlsx")
    except (Exception, ) as e:
        rows = []
    text_dict = {row[0]: row[1] for row in rows}
    return text_dict


def _save_current_text_dict(text_dict):
    data = [(path, text) for path, text in text_dict.items()]
    to_xlsx("003_images_text_dict.xlsx", data)


def detect_all_text():
    all_paths = gen_path_list()
    images_text_dict = _get_saved_text_dict()
    done_paths = list(images_text_dict.keys())
    undone_paths = [p for p in all_paths if p not in done_paths]
    path_chunks = chunks(undone_paths, 16)
    for i, path_chunk in tqdm(enumerate(path_chunks)):
        new_text_dict = get_text_dict(path_chunk)
        pprint(new_text_dict.items())
        print(path_chunk)
        print(len(path_chunk))
        print(i)
        images_text_dict.update(new_text_dict)
        q, mod = divmod(i, 100)
        if mod == 0:
            _save_current_text_dict(images_text_dict)
    _save_current_text_dict(images_text_dict)


if __name__ == '__main__':
    detect_all_text()
