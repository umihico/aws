from umihico_commons.csv_wrapper import load_csv
from os import path as ospath
from os import sep
import codecs
from lxml import html, etree


def gen_path_list(filename="002_image_paths.csv"):
    def to_windows_abs_path(path):
        return ospath.join(ospath.dirname(ospath.abspath(__file__)), path.replace("./", "", 1).replace('/', sep))
    rows = load_csv(filename)
    paths = [to_windows_abs_path(row[0]) for row in rows]
    return paths


def tolxml(local_html_path):
    f = codecs.open(local_html_path, 'r', 'utf-8')
    source = f.read()
    f.close()
    try:
        root = html.fromstring(source)
    except (Exception, ) as e:
        print(local_html_path)
        print(e)
    else:
        return root
    f = open(local_html_path, 'br')
    source = f.read()
    root = html.fromstring(source)
    f.close()
    return root


def get_metadata(lxmlroot):
    name_xpath = "//table//tr//td[contains(.,'【会社名】')]/following-sibling::td"
    date_xpath = "//table//tr//td[contains(.,'【提出日】')]/following-sibling::td"
    sec_code_xpath = "//*[@name='jpdei_cor:SecurityCodeDEI']"

    def falible_text_content(lxmlroot, xpath):
        try:
            return lxmlroot.xpath(xpath)[0].text_content()
        except (Exception, ) as e:
            return ""
    name, date_, sec_code = [falible_text_content(
        lxmlroot, x) for x in [name_xpath, date_xpath, sec_code_xpath]]
    if sec_code:
        if len(sec_code) != 5 or not sec_code.isdigit() or not sec_code[-1] == "0":
            raise Exception(f"{path} has sec_code:{sec_code}")
        sec_code = sec_code[:4]
    return name, date_, sec_code
