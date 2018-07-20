from umihico_commons.xlsx_wrapper import load_xlsx, to_xlsx
from PIL import Image
from io import BytesIO
from umihico_commons.requests_wrapper import get
from tqdm import tqdm
from time import sleep
image_url_dict = {}


def gen_global_image_url_dict():
    global image_url_dict
    rows = load_xlsx("closed_itemlist.xlsx")
    for row in rows:
        auc_id = row[-1].split('/')[-1]
        image_url = "https://" + row[2]
        image_url_dict[auc_id] = image_url


gen_global_image_url_dict()


def get_image_url(auc_id):
    global image_url_dict
    return image_url_dict[auc_id]


def load_data():
    rows = load_xlsx("closed_items.xlsx")
    field_names = rows[0]
    dicts = []
    for row in rows[1:]:
        dict_ = {fn: col for fn, col in zip(field_names, row)}
        dict_["sold_count"] = min([dict_["quantity"], dict_['bids']])
        dict_["name"] = dict_["出品者"] + dict_['productName']
        dicts.append(dict_)
    return dicts


def get_image(image_url):
    image = Image.open(
        BytesIO(get(image_url).content))
    return image


def merge_same_id_same_title(dicts):
    owner_title_base_dict = {}
    for dict_ in dicts:
        owner_name = dict_['出品者']
        title = dict_['productName']
        owner_title_base_dict.setdefault(
            owner_name, {}).setdefault(title, []).append(dict_)
    return owner_title_base_dict


def gen_raw_final():
    dicts = load_data()
    owner_title_base_dict = merge_same_id_same_title(dicts)
    rows = []
    field_names = set()
    for owner_name, productName_base_dict in owner_title_base_dict.items():
        for productName, same_productName_item_list in productName_base_dict.items():
            starting_prices = [d_["開始時の価格"]
                               for d_ in same_productName_item_list]
            if any([bool("1円" == text) for text in starting_prices]):
                print("1円", "hit")
                continue

            common_row_keys = ["出品者", "productName", ]
            common_row = {
                key: same_productName_item_list[0][key] for key in common_row_keys}
            if "バッテリー" in common_row['productName']:
                print("バッテリー", "hit")
                continue
            common_row["url"] = "https://page.auctions.yahoo.co.jp/jp/auction/" + \
                same_productName_item_list[0]['productID']
            common_row["image_url"] = get_image_url(
                same_productName_item_list[0]['productID'])
            joined_row_keys = ["sold_count", "price", "productID"]
            joined_row = {key: [] for key in joined_row_keys}
            for dict_ in same_productName_item_list:
                for key in joined_row_keys:
                    joined_row[key].append(dict_[key])
            common_row['sold_count_sum'] = str(int(sum(
                int(x) for x in joined_row['sold_count'])))
            joined_row = {k: ','.join(v) for k, v in joined_row.items()}
            row = {**common_row, **joined_row}

            rows.append(row)
            field_names.update(list(row.keys()))
            break  # only oneowner-onetitle in final list
    rows = [[r.get(fn, "") for fn in field_names] for r in rows]
    rows.insert(0, field_names)
    to_xlsx("raw_final.xlsx", rows)


def gen_final():
    rows = load_xlsx("raw_final.xlsx")
    keys = rows[0]
    dicts = [{fn: c for fn, c in zip(keys, r)} for r in rows]
    import xlsxwriter
    workbook = xlsxwriter.Workbook("final.xlsx")
    worksheet = workbook.add_worksheet()
    field_names = ["image", "sold_count_sum", "price", "productName", "出品者",
                   "url", "productID", "sold_count"]
    for c, fieldname in enumerate(field_names):
        worksheet.write(0, c, fieldname)
    for raw_row_int, dict_ in enumerate(tqdm(dicts[1:101])):
        row_int = raw_row_int + 1
        # url	sold_count_sum	image_url	productName	productID	出品者	price	sold_count
        image = get_image(dict_['image_url'])
        image_path = f"temp_images/{row_int}.png"
        image.thumbnail((200, 200))
        image.save(image_path, 'png')
        sleep(1)
        worksheet.insert_image(f'A{row_int+1}', image_path)
        for col, key in enumerate(field_names):
            if col == 0:
                continue
            worksheet.write(row_int, col + 1, dict_[key])
    workbook.close()


if __name__ == '__main__':
    gen_raw_final()
    # gen_final()
