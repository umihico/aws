
from umihico_commons.csv_wrapper import xlsx_to_list_of_list
import xlsxwriter
from tqdm import tqdm
import os
from PIL import Image


def conv_if_gif(image_filename):
    try:
        img = Image.open(image_filename)
        rest, filetype = os.path.splitext(image_filename)
        if filetype.lower() != ".gif":
            return image_filename
        new_path = rest + '.png'
        try:
            img = Image.open(new_path)
        except (Exception, ) as e:
            img.save(new_path, 'png')

    except (Exception, ) as e:
        return False
    return new_path


def write_xlsx():
    base_data_rows = xlsx_to_list_of_list("raw_final.xlsx")
    # print(base_data_rows[-2])
    # raise
    # base_data_rows = csv_wrapper.xlsx_to_list_of_list("combined.xlsx")
    split_here = True
    split_file_num = 0
    print('writing...')
    for row in tqdm(base_data_rows):
        if split_here:
            row_int = 0
            split_file_num += 1
            filename = f'finals/data{split_file_num}.xlsx'
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            for c, fieldname in enumerate(['url', 'title', 'date in text', 'file date', 'today', 'text', 'picture']):
                worksheet.write(0, c, fieldname)
            split_here = False
        hp_url, image_url, title, image_filename, date_text_mining, date_timestamp, date_today, image_text = row
        image_filename = image_filename.replace("/", os.sep)
        rest, filetype = os.path.splitext(image_filename)
        if filetype == '.svg':
            continue
        new_image_filename = conv_if_gif(image_filename)
        if not new_image_filename:
            continue
        worksheet.insert_image(f'G{row_int+2}', new_image_filename)
        try:
            for col_int, text in enumerate([hp_url, title, date_text_mining, date_timestamp, date_today, image_text]):
                worksheet.write(row_int + 1, col_int, text)
        except (Exception, ) as e:
            pass
        else:
            # print('printed')
            row_int += 1
        if row_int >= 1000:
            workbook.close()
            print(filename + ' is done.')
            split_here = True
            row_int = 0


if __name__ == '__main__':
    write_xlsx()
