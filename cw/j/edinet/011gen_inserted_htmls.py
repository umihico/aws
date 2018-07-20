from common_funcs import gen_path_list, tolxml, get_metadata
from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from lxml import etree, html
import codecs
import os
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def gen_inserted_htmls():
    # paths = gen_path_list(filename="007_merged_html_paths.csv")
    paths = [x[0] for x in load_xlsx("009_metadata_only_new.xlsx")]
    _text_rows = load_xlsx("003_images_text_dict.xlsx")
    text_dict = {image_path: text for image_path, text in _text_rows}
    _title_rows = load_xlsx("008_image_titles.xlsx")
    title_dict = {}
    for html_path, image_path, title in _title_rows:
        title_dict.setdefault(html_path, {})[
            image_path.replace('/', os.sep)] = title

    itrs = [(os.path.join(path, "merged.html"), title_dict, text_dict)
            for path in paths]
    Poolbar(gen_inserted_html_thread, itrs)
    # gen_inserted_html_thread(path, title_dict, text_dict)
    # print(path)
    # raise
    # metadata_rows = []
    # for path in tqdm(paths):
    #     name, date_, sec_code = get_metadata_path(path)
    #     metadata_rows.append((name, date_, sec_code))
    # to_xlsx("011_metadata.xlsx", metadata_rows)


def get_metadata_path(path):
    lxmlroot = tolxml(path)
    name, date_, sec_code = get_metadata(lxmlroot)
    return name, date_, sec_code


def gen_inserted_html_thread(args):
    path, title_dict, text_dict = args
    lxmlroot = tolxml(path)
    name, date_, sec_code = get_metadata(lxmlroot)
    images = lxmlroot.xpath("//img")
    dirname, filename = os.path.split(path)
    for image in images:
        src = image.attrib["src"]
        image_abs_path = os.path.join(dirname, src)
        image_abs_path = image_abs_path.replace('/', os.sep)
        detected_text = text_dict[image_abs_path]
        detected_title = title_dict[path][image_abs_path]

        br0 = etree.Element("br")
        image.addnext(br0)
        br1 = etree.Element("br")
        br0.addnext(br1)
        text_detection = etree.Element("text_detection",)
        br1.addnext(text_detection)
        text_detection.text = "【IMAGE_TEXT_DETECTION】"
        br = etree.SubElement(
            text_detection, "br")
        text_detection_title = etree.SubElement(
            text_detection, "text_detection_title")
        text_detection_title.text = detected_title
        detected_text_list = detected_text.split("\n")
        for detected_text_line in detected_text_list:
            br = etree.SubElement(
                text_detection, "br")
            detected_text_line_element = etree.SubElement(
                text_detection, "detected_text_line_element")
            detected_text_line_element.text = detected_text_line
        text_detection.tail = "【IMAGE_TEXT_DETECTION_END】"
    output_path = os.path.join(dirname, "inserted.html")
    with codecs.open(output_path, 'w', 'utf-8') as f:
        f.write(html.tostring(lxmlroot, encoding="unicode"))


def Poolbar(func, iter):
    '''-1 or making process priority low'''
    with Pool(cpu_count()) as p:
        # with Pool(cpu_count()) as p:
        #     parent = psutil.Process()
        #     parent.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        #     for child in parent.children():
        #         child.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        return list(tqdm(p.imap(func, iter), total=len(iter)))


#
if __name__ == '__main__':
    gen_inserted_htmls()
    # test_merge_htmls()
