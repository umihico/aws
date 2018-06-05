
from umihico_commons.google_cloud_vision_api import gen_ocr_pair_on_new_xlsx

if __name__ == '__main__':
    gen_ocr_pair_on_new_xlsx("pic_urls.xlsx", "pic_urls_results.xlsx")
