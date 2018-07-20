from umihico_commons.xlsx_wrapper import to_xlsx, load_xlsx
from umihico_commons.functools import chunks
from common_funcs import get_metadata, tolxml, gen_path_list
from tqdm import tqdm
import xlsxwriter
import os
from PIL import Image
from datetime import datetime
from time import sleep


def get_today():
    return str(datetime.today()).split(' ')[0]


def gen_raw_final():
    paths = gen_path_list(filename="007_merged_html_paths.csv")
    # meta_rows = load_xlsx("009_metadata.xlsx")
    text_rows = load_xlsx("003_images_text_dict.xlsx")
    title_rows = load_xlsx("008_image_titles.xlsx")
    text_dict = {image_path: text for image_path, text in text_rows}
    output_rows = []
    for path in tqdm(paths):
        lxmlroot = tolxml(path)
        name, date_, sec_code = get_metadata(lxmlroot)
        dir_path, filename = os.path.split(path)
        title_dict = {image_path.replace(
            '/', os.sep): title for html_path, image_path,
            title in title_rows if dir_path in html_path}
        for image_path, title in title_dict.items():
            text = text_dict[image_path].replace("__empty__", "")
            output_row = (dir_path, name, date_, image_path, title, text)
            output_rows.append(output_row)
    to_xlsx("010_raw_final.xlsx", output_rows)


def gen_final():
    def row_generator():
        rows = load_xlsx("010_raw_final.xlsx")
        for i, row in enumerate(rows):
            yield i, row
    rows = row_generator()
    chunk_id = 0
    while True:
        chunk_id += 1
        filename = f'final{chunk_id}.xlsx'
        print(filename)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        for c, fieldname in enumerate(['time', 'name', 'document_date', 'title', 'text']):
            worksheet.write(0, c, fieldname)
        row_int = 0
        while True:
            row_int += 1
            try:
                i, (dir_path, name, date_, image_path, title, text) = next(rows)
            except StopIteration:
                workbook.close()
                return
            try:
                imagepath_wo_type, image_filetype = os.path.splitext(
                    image_path)
                if image_filetype.lower() == ".gif":
                    image_path = temp_png_from_gif(image_path)
                if os.path.isfile(image_path):
                    worksheet.insert_image(f'F{row_int+1}', image_path)
                else:
                    raise Exception("insert_image error")
            except (Exception, ) as e:
                row_int -= 1
                continue
            else:
                worksheet.write(row_int, 0,   get_today())
                worksheet.write(row_int, 1,   name)
                worksheet.write(row_int, 2,   date_)
                worksheet.write(row_int, 3,   title)
                worksheet.write(row_int, 4,   text)
            if row_int >= 1000:
                break
        workbook.close()
        print(i)


def temp_png_from_gif(path):
    image = Image.open(path, mode="r")
    path_wo_type, filetype = os.path.splitext(path)
    new_path = path_wo_type + '.png'
    if not os.path.isfile(new_path):
        image.save(new_path, 'PNG')
        sleep(1)
    return new_path


def test_temp_png_from_gif():
    path = r"C:\Users\umi\GitHub\aws\cw\j\edinet\zips\Xbrl_Search_20180630_223953\S1008A7H\XBRL\PublicDoc\fuzoku\50_8052200102809.gif"
    new_path = temp_png_from_gif(path)
    print(new_path)


if __name__ == '__main__':
    # merge_all()
    # gen_final()
    gen_raw_final()
    # test_temp_png_from_gif()
