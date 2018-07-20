from lxml import html, etree
from common_funcs import gen_path_list as gen_all_path_list
from common_funcs import tolxml
# html.fromstring()
from tqdm import tqdm
from re import findall
import codecs
from os import path as ospath
from umihico_commons.xlsx_wrapper import to_xlsx
from pprint import pprint


def get_metadata(path):
    root = tolxml(path)
    name_xpath = "//table//tr//td[contains(.,'【会社名】')]/following-sibling::td"
    date_xpath = "//table//tr//td[contains(.,'【提出日】')]/following-sibling::td"
    sec_code_xpath = "//*[@name='jpdei_cor:SecurityCodeDEI']"

    def falible_text_content(root, xpath):
        try:
            return root.xpath(xpath)[0].text_content()
        except (Exception, ) as e:
            return ""
    name, date_, sec_code = [falible_text_content(
        root, x) for x in [name_xpath, date_xpath, sec_code_xpath]]
    if sec_code:
        if len(sec_code) != 5 or not sec_code.isdigit() or not sec_code[-1] == "0":
            raise Exception(f"{path} has sec_code:{sec_code}")
        sec_code = sec_code[:4]
    return name, date_, sec_code


def test_get_metadata():
    path = "C:/Users/umi/AppData/Local/Temp/Temp1_Xbrl_Search_20180630_232424.zip/S100D4PC/XBRL/PublicDoc/0000000_header_jpcrp030000-asr-001_E01124-000_2018-03-31_01_2018-06-08_ixbrl.htm"
    print(get_metadata(path))


def gen_path_list():
    path_list = gen_all_path_list(filename="007_merged_html_paths.csv")
    return path_list


def get_date_all_htmls():
    path_list = gen_path_list()
    output_rows = []
    for i, file_path in tqdm(enumerate(path_list)):
        try:
            name, date_, sec_code = get_metadata(file_path)
        except (Exception, ) as e:
            print(file_path)
            raise
        row = (ospath.dirname(file_path), name, date_, sec_code)
        # print(row)
        output_rows.append(row)
    to_xlsx("009_metadata.xlsx", output_rows)


def test_get_date():
    path = r"C:/Users/umi/GitHub/aws/cw/j/edinet/zips/Xbrl_Search_20180630_224031/S1008MY3/XBRL/PublicDoc/0000000_header_jpcrp030000-asr-001_E03410-000_2016-06-20_01_2016-09-12_ixbrl.htm"
    print(get_date(path))


if __name__ == '__main__':
    # test_get_date()
    # test_get_metadata()
    get_date_all_htmls()
