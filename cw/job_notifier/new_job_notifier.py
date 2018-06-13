
from feedparser import parse
from time import sleep
from datetime import datetime, timedelta
from umihico_commons.pickle_wrapper import save, load
from umihico_commons.notifier_via_chatwork import ChatworkApi


def delete_deplicate(all_entries):
    url_base = {e['link']: e for e in all_entries}
    return list(url_base.values())


def to_entries(rss_url, genre):
    raw_parsed = parse(rss_url)
    entries = []
    keys = 'title,link,description,published,published_parsed'.split(",")
    for raw_entry in raw_parsed.entries:
        entry = {key: getattr(raw_entry, key) for key in keys}
        entry['genre'] = genre
        entries.append(entry)
    return entries


def filter_recent(entries, within_seconds):
    filtered_entries = []
    for entry in entries:
        published_date = to_datetime(entry)
        now = datetime.today()
        delta = now - published_date
        delta_seconds = delta.total_seconds()
        if delta_seconds < within_seconds * 2:
            filtered_entries.append(entry)
    return filtered_entries


def filter_keyword(entries, genre):
    keywords = ['python',  'selenium', '自動化', 'VBA',
                'マクロ', 'スクレイピング', 'モノレート', 'Amazon', 'アマゾン']
    filtered_entries = []
    for entry in entries:
        if genre != 'all':
            entry['matched_keywords'] = genre
            filtered_entries.append(entry)
        else:
            all_words = entry['title'].lower() + entry['description'].lower()
            matched_keywords = [
                keyword for keyword in keywords if keyword in all_words]
            if matched_keywords:
                entry['matched_keywords'] = '/'.join(matched_keywords)
                filtered_entries.append(entry)
    return filtered_entries


def post_entries(cw_api, entries):
    for e in entries:
        cw_api.post_in_mychat(
            '\n'.join([e['title'], e['matched_keywords'], e['link'], e['description'][:200]]))


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
    cw_api.post_in_mychat('job_notifier started.')
    rss_urls_with_desc = {
        "https://crowdworks.jp/public/jobs.rss": 'all',
        "https://crowdworks.jp/public/jobs/category/249.rss": 'simple_data_collecting'}
    prev_entry_urls = set()
    while True:
        refresh_frequency = 60
        print(datetime.today())
        all_entries = []
        for rss_url, genre in rss_urls_with_desc.items():
            genre_entries = to_entries(rss_url, genre)
            print(genre, len(genre_entries))
            print("most_recent_date", most_recent_date(genre_entries))
            genre_entries = filter_recent(
                genre_entries, within_seconds=refresh_frequency)
            print(genre, 'recent', len(genre_entries))
            genre_entries = filter_keyword(
                genre_entries, genre)
            print(genre, 'keyword', len(genre_entries))
            all_entries.extend(genre_entries)
        all_entries = delete_deplicate(all_entries)
        new_entries = [e for e in all_entries if e['link']
                       not in prev_entry_urls]
        prev_entry_urls = set(e['link'] for e in new_entries)
        post_entries(cw_api, new_entries)
        sleep(refresh_frequency)


def _test_post_chat():
    post_in_mychat('\n'.join(["title", "link", "description"]))


if __name__ == '__main__':
    # parse_rss_test()
    main()
