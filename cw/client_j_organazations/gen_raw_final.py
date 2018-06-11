
from umihico_commons.csv_wrapper import xlsx_to_list_of_list, xlsx_from_list_of_list
from os.path import basename, join
import datetime


def today_str():
    return str(datetime.date.today()).replace('-', '/')


def merge_and_gen_raw_final():
    index_hpurl_imageurl = xlsx_to_list_of_list("urls.xlsx")
    imageurl_text_date = xlsx_to_list_of_list("pic_texts_dates.xlsx")
    imageurl_base_text_date_dict = {
        imageurl: (text, date) for imageurl, text, date in imageurl_text_date}
    picurl_base_modifieddate_dict = dict(xlsx_to_list_of_list("dates.xlsx"))
    hpurl_base_title_dict = dict(xlsx_to_list_of_list("titles.xlsx"))
    output_list = []
    for index_, hpurl, imageurl in index_hpurl_imageurl:
        text, date_on_text = imageurl_base_text_date_dict.get(
            imageurl, ('empty', "not found"))
        if text == 'empty':
            continue
        title = hpurl_base_title_dict.get(hpurl, '')
        modifieddate = picurl_base_modifieddate_dict.get(imageurl, "not found")
        image_filename = join(
            "C:/Users/umi/Desktop/pics", str(int(float(index_) - 1)) + basename(imageurl))
        row = [hpurl, imageurl, title, image_filename, date_on_text,
               modifieddate, today_str(), text]
        output_list.append(row)
    xlsx_from_list_of_list("raw_final.xlsx", output_list)


if __name__ == '__main__':
    merge_and_gen_raw_final()
