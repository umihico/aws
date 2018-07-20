import os

from common_funcs import gen_path_list, tolxml
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from lxml import html
import codecs
from tqdm import tqdm


def _gen_same_dir_group_dict():
    with open("004_htmls.csv", mode='r') as f:
        paths = f.read().split('\n')
        paths = [p for p in paths if p]
        # print(paths[:3])
        # ['./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0000000_header_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm', './zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0101010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm',
        #     './zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0102010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm']
    same_dir_group_dict = {}
    for path in paths:
        dirname, filename = os.path.split(path)
        same_dir_group_dict.setdefault(dirname, []).append(path)
    return same_dir_group_dict


def gen_merged_htmls():
    same_dir_group_dict = _gen_same_dir_group_dict()
    for dirname, paths in tqdm(same_dir_group_dict.items()):
        # print(same_dir_html_paths)
        # raise
        _gen_merged_html(dirname, paths)
        raise


def _gen_merged_html(dirname, paths):
    print(paths)
    dirnames = [os.path.split(path)[0] for path in paths]
    for dirname in dirnames:
        if dirname != dirnames[0]:
            raise Exception(f"dirnames are not same. paths:{paths}")
    dirname = dirnames[0]
    # print(dirname)
    output_path = os.path.join(dirname, "merged.html")
    # print(output_path)
    joined_source = "<html>" + '\n'.join(
        [html.tostring(tolxml(path).body, encoding="unicode") for path in paths]) + "</html>"
    with codecs.open(output_path, 'w', 'utf-8') as f:
        f.write(joined_source)
    return output_path


def test_merge_htmls():
    dirname = "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc"
    paths = [
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0000000_header_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0101010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0102010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0103010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0104010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105000_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105310_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105320_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105330_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105340_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105400_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0105410_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0106010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0107010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
        "./zips/Xbrl_Search_20180630_223953/S1008A7H/XBRL/PublicDoc/0201010_honbun_jpcrp030000-asr-001_E31524-000_2016-06-30_01_2016-09-29_ixbrl.htm",
    ]
    gen_merged_html(dirname, paths)


if __name__ == '__main__':
    main()
