from data import DATAP
from json import load
from lxml import etree


def extract_with_xpath(elem, abstract_xpath, url_xpath, title_to_id, scope, f):
    # title_r = title_xpath(elem)
    abstract_r = abstract_xpath(elem)
    if abstract_r:
        url = url_xpath(elem)[0].text
        abstract = abstract_r[0].text
        if abstract is None:
            abstract = " "
        title = url.replace("https://en.wikipedia.org/wiki/", "")
        f.write(title + ",|" + abstract + "|\n")


def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


def get_abstract():
    with open(DATAP + '/dump/article_ids_reverse.json', "r", encoding="UTF8") as f:
        title_to_id = load(f)
    with open(DATAP + '/dump/articles_inscope.json', "r", encoding="UTF8") as f:
        scope = load(f)
        scope = {int(key): values for key, values in scope.items()}
    f = open(DATAP + '/dump/articles_all_abstracts.csv', "w", encoding="UTF8")
    abstract_xpath = etree.ETXPath("child::abstract")
    url_xpath = etree.ETXPath("child::url")
    context = etree.iterparse(DATAP + '/dump/enwiki-20180901-abstract.xml', events=('end',), tag="doc")
    fast_iter(context,
              lambda elem: extract_with_xpath(elem, abstract_xpath, url_xpath, title_to_id, scope, f))
    f.close()


# Just for fun: Nearly half of the abstracts are dirty. {, } and = hint at dirty abstracts where templates haven't
# been unfolded in a correct way.
def evaluation():
    with open(DATAP + '/dump/articles_all_abstracts.csv', "r", encoding="UTF8") as f:
        dirty_count = 0
        all_count = 0
        for line in f:
            if "{" in line or "=" in line or "}" in line:
                dirty_count += 1
            all_count += 1
        print(str(dirty_count) + " out of " + str(all_count) + " are dirty!")


if __name__ == '__main__':
    evaluation()
