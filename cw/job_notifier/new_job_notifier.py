
from feedparser import parse
from time import sleep
from datetime import datetime, timedelta
from umihico_commons.pickle_wrapper import save, load
from umihico_commons.notifier_via_chatwork import ChatworkApi


def to_entries(rss_url):
    raw_parsed = parse(rss_url)
    entries = []
    keys = 'title,link,description,published,published_parsed'.split(",")
    for raw_entry in raw_parsed.entries:
        entry = {key: getattr(raw_entry, key) for key in keys}
        entries.append(entry)
    return entries


def filter_recent(entries, within_seconds):
    filtered_entries = []
    for entry in entries:
        published_date = to_datetime(entry)
        now = datetime.today()
        delta = now - published_date
        delta_seconds = delta.total_seconds()
        if delta_seconds < within_seconds:
            filtered_entries.append(entry)
    return filtered_entries


def filter_keyword(entries, genre):
    if genre == "simple_data_collecting":
        filtered_entries = entries[:]
        return filtered_entries
    elif genre == 'all':
        filtered_entries = []
        keywords = ['python',  'selenium', '自動化', 'VBA',
                    'マクロ', 'スクレイピング', 'モノレート', '画像', 'Amazon', 'アマゾン']
        for entry in entries:
            entry_word = entry['title'].lower() + entry['description'].lower()
            if any(bool(keyword in entry_word) for keyword in keywords):
                filtered_entries.append(entry)
        return filtered_entries
    else:
        raise Exception("unknown genre:{genre}")


def post_entries(cw_api, entries):
    for e in entries:
        cw_api.post_in_mychat(
            '\n'.join([e['title'], e['link'], e['description']]))


def to_datetime(entry):
    date = datetime(*entry['published_parsed'][:6])
    adj_hour_text = entry['published'][len(entry['published']) - 5:]
    if adj_hour_text == "+0900":
        adj = timedelta(hours=9)
    else:
        raise Exception(f"unknown date:{entry['published']}>{adj_hour_text}")
    date = date + adj
    return date
    # datetime()


def most_recent_date(entries):
    datetimes = [to_datetime(entry) for entry in entries]
    return max(datetimes)


def main():
    cw_api = ChatworkApi()
    rss_urls_with_desc = {
        "https://crowdworks.jp/public/jobs.rss": 'all',
        "https://crowdworks.jp/public/jobs/category/54/u/all.rss": 'simple_data_collecting'}

    try:
        while True:
            refresh_frequency = 60
            print(datetime.today())
            for rss_url, genre in rss_urls_with_desc.items():
                entries = to_entries(rss_url)
                print(genre, len(entries))
                print("most_recent_date", most_recent_date(entries))
                entries = filter_recent(
                    entries, within_seconds=refresh_frequency)
                print(genre, 'recent', len(entries))
                entries = filter_keyword(
                    entries, genre)
                print(genre, 'keyword', len(entries))
                post_entries(cw_api, entries)
            sleep(refresh_frequency)
    except KeyboardInterrupt:
        pass


def _test_post_chat():
    post_in_mychat('\n'.join(["title", "link", "description"]))


if __name__ == '__main__':
    # parse_rss_test()
    main()
