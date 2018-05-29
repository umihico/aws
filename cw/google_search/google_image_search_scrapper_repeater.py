from google_image_search_scrapper import gen_urls_func


def gen_urls_func_reverse_repeat(i):
    for j in reversed(list(range(0, i))):
        print(f"gen_urls_func_reverse_repeat:{j}")
        gen_urls_func(j, filename="reverse_results.txt")


if __name__ == '__main__':
    import sys
    args = sys.argv
    this_filename, i = args
    gen_urls_func_reverse_repeat(int(i))
