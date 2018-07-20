from lxml import html, etree
from common_funcs import gen_path_list, tolxml
# html.fromstring()
from tqdm import tqdm
from re import findall
import codecs
from os import path as ospath
from umihico_commons.xlsx_wrapper import to_xlsx
from pprint import pprint
from traceback import format_exc


def get_image_paths(root, htmlfile_path):
    image_paths = root.xpath("//img/@src")
    full_image_paths = [ospath.join(ospath.dirname(
        htmlfile_path), image_path) for image_path in image_paths]
    # if len(full_image_paths) > 0:
    #     print(full_image_paths)
    return full_image_paths


def get_bracket_string(root):
    images = root.xpath("//img")
    # splitter = etree.Element("splitter")
    for image in images:
        image.text = "__split_here__"
    # images.addnext(splitter)
    all_text = root.xpath("//html")[0].text_content()
    splited_texts = all_text.split("__split_here__")
    splited_texts.pop(len(splited_texts) - 1)
    titles_images = findall("(__split_here__|【.+?】)", all_text)
    # ['【企業情報】', '【企業の概況】', '【主要な経営指標等の推移】', '【沿革】', '【事業の内容】', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '__split_here__', '【関係会社の状況】', '【従業員の状況】']
    title_indexs = [i for i, x in enumerate(
        titles_images) if x != "__split_here__"]
    image_indexs = [i for i, x in enumerate(
        titles_images) if x == "__split_here__"]
    match_titles = []
    for image_index in image_indexs:
        match_title_index = [i for i in title_indexs if i < image_index][-1]
        match_titles.append(titles_images[match_title_index])
    return match_titles


def get_bracket(path):
    root = tolxml(path)
    image_paths = get_image_paths(root, htmlfile_path=path)
    if len(image_paths) > 0:
        titles = get_bracket_string(root)
        title_dict = {image_path: title for image_path,
                      title in zip(image_paths, titles)}
        return title_dict
    else:
        return {}


def get_bracket_all_htmls():
    path_list = gen_path_list(filename="007_merged_html_paths.csv")
    output_rows = []
    error_logs = []
    for i, file_path in tqdm(enumerate(path_list)):
        try:
            title_dict = get_bracket(file_path)
        except (Exception, ) as e:
            error_logs.append(file_path)
            error_logs.append(format_exc())
        for image_path, title in title_dict.items():
            row = (file_path, image_path, title)
            # print(title)
            output_rows.append(row)
        if divmod(i, 10000)[1] == 0:
            to_xlsx("008_image_titles.xlsx", output_rows)
    to_xlsx("008_image_titles.xlsx", output_rows)
    for error_log in error_logs:
        print(error_log)


def test_process_html_file():
    path = r"C:/Users/umi/GitHub/aws/cw/j/edinet/zips/Xbrl_Search_20180630_224157/S100ATOT/XBRL/PublicDoc/0104010_honbun_jpcrp030000-asr-001_E05622-000_2016-08-31_02_2017-07-04_ixbrl.htm"
    get_bracket(path)


if __name__ == '__main__':
    # test_process_html_file()
    get_bracket_all_htmls()
