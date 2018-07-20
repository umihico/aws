from umihico_commons.functools import load_from_txt
from umihico_commons.xlsx_wrapper import to_xlsx
from collections import Counter


def gen_excel_raw_data():
    filenames = ["wiki.txt", "yahoo_finace.txt"]
    srcs = ["wikipedia", "yahoo_finace"]
    for filename, src in zip(filenames, srcs):
        filednames = []
        filednames_counter = []
        rows = load_from_txt(filename)
        for dict_ in rows:
            filednames_counter.extend(dict_.keys())
            for key in dict_.keys():
                if key not in filednames:
                    filednames.append(key)
        counter_dict = {word: count for word, count in Counter(
            filednames_counter).most_common()}
        filednames = [name for name in filednames if counter_dict[name] > 1000]
        result = []
        result.append(filednames)
        for dict_ in rows:
            if dict_:
                result_row = [dict_.get(key, "")
                              for key in filednames]
                result.append(result_row)
        to_xlsx(src + ".xlsx", result)


if __name__ == '__main__':
    gen_excel_raw_data()
