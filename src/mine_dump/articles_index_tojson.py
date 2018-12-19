from data import DATAP
from json import load, dump
import time
from mine_dump import hms_string


def articles_annotate_index():
    with open(DATAP + '/dump/enwiki-20180901-pages-articles-multistream-index.txt', 'r', encoding='UTF8') as f:
        with open(DATAP + '/dump/articles.json', 'r', encoding='UTF8') as f_art:
            adict = load(f_art)
        for line in f:
            splits = line.split(':')
            byteindex = splits[0]
            title = ''.join(splits[2:]).strip().replace(' ', '_')
            if title in adict:
                adict[title]["byteindex"] = byteindex
        with open(DATAP + '/dump/articles.json', 'w', encoding='UTF8') as f_art:
            dump(adict, f_art)
    for a in adict:
        if "byteindex" not in adict[a]:
            print(a)


if __name__ == "__main__":
    start_time = time.time()
    articles_annotate_index()
    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))
