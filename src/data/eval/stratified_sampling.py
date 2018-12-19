from data.plotting.plotting_category_statistics import get_strats
import random
from data import DATAP


def sample():
    cat_strats, art_strats = get_strats(5, 0.3)
    samples = [sample_from(art_strat, 100) for art_strat in art_strats]
    for x in range(len(samples)):
        sample = samples[x]
        with open(DATAP + "/eval/sample" + str(x), "w", encoding="utf-8") as f:
            for article in sample:
                f.write("https://en.wikipedia.org/wiki/" + article + "\n")
                f.flush()


def sample_from(articles, count):
    if len(articles) < count:
        count = len(articles)
    sample = set()
    for x in range(count):
        index = random.randint(0, len(articles))

        article = list(articles)[index]
        while article in sample or "List of" in article or "Comparison of" in article:
            index = random.randint(0, len(articles))
            article = list(articles)[index]
        sample.add(article)
    return sample


if __name__ == '__main__':
    sample()
