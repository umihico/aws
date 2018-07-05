from umihico_commons.xlsx_wrapper import load_xlsx

rows = load_xlsx("proxy.xlsx")

ip_list = [row[0] for row in rows]


if __name__ == '__main__':
    from pprint import pprint
    pprint(ip_list)
