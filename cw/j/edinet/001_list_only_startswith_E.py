import zipfile
# filename = "Xbrl_Search_20180630_193400.zip"
# from csv import
# with zipfile.ZipFile(filename, 'r') as post:
#     # zipファイルを開いて、中に格納されいるファイル名を表示
#     for info in post.infolist():
#         print(info.filename)
#
#     print(repr(post.read("XbrlSearchDlInfo.csv")))
from umihico_commons.csv_wrapper import load_csv
filename = "001_dirlist_in_zip.csv"
rows = load_csv(filename, delimiter=",")
ok_dirnames = [row[0]
               for row in rows if len(row) > 1 and row[2].startswith("E")]
with open("001_ok_dirlist_in_zip.csv", mode='w') as f:
    f.writelines('\n'.join(ok_dirnames))

# from pprint import pprint
# pprint(ok_dirnames)
# with open(filename) as f:
#     print(f.readline())
