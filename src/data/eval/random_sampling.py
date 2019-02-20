from data import DATAP, INDICATORS
from json import load
import random
import pandas as pd
import csv
import webbrowser


def perform_eval():
    with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
        ad = load(f)
        S = set(a for a in ad if ad[a]["Seed"])

    articles_visited = set()
    with open(DATAP + '/eval/random.csv', 'r', encoding="UTF8") as f:
        olddata = ""
        count = 0
        for line in f:
            title = line.split(",")[0].replace("|", "")
            if title in ad and not ad[title]["IsStub"]:
                count += 1
                articles_visited.add(title)
                olddata += line
        olddata += "\n"
    print("old size: " + str(len(articles_visited)))

    with open(DATAP + '/eval/random.csv', 'w', encoding="UTF8") as f:
        f.write(olddata)
        articles = list(ad.keys())
        articles.sort()
        x = count
        while x < 4000:
            index = random.randint(0, len(ad))
            article = articles[index]
            if article in articles_visited or article in S or "List_of" in article or ad[article]["IsStub"]:
                continue
            else:
                articles_visited.add(article)
                print("https://en.wikipedia.org/wiki/" + article)
                webbrowser.open("https://en.wikipedia.org/wiki/" + article, new=2)
                agreement = ""
                while agreement not in ["yes", "no"]:
                    agreement = input(str(x) + " Enter 'yes' or 'no'!")
                if agreement == "yes":
                    agreement_int = "1"
                if agreement == "no":
                    agreement_int = "0"
                f.write("|" + article + "|,|" + agreement_int + "|\n")
                f.flush()
                x += 1


def get_classification(title, langdict):
    resultdict = {ind: langdict[title][ind] for ind in INDICATORS if ind in langdict[title]}
    resultdict['Complementary'] = sum(resultdict.values()) > 0
    return resultdict


def get_random_data():
    with open(DATAP + "/eval/random.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)

        A_random = []
        y = []
        for row in reader:
            A_random.append(row[0])
            y.append(row[1])

        return A_random, y


# one row per article, indicators are columns
def get_article_tags():
    with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)
    with open(DATAP + '/eval/random.csv', 'r', encoding="UTF8") as f:
        df = pd.read_csv(f, delimiter=',', quotechar='|', names=['title', 'tag'])
        df.set_index('title')
        indicatorrow = dict()
        for ind in INDICATORS + ["Complementary"]:
            indicatorrow[ind] = []

        for title in df['title']:
            if title not in langdict:
                print(title)
                continue
            classifdict = get_classification(title, langdict)
            for ind in INDICATORS + ["Complementary"]:
                indicatorrow[ind].append(classifdict[ind])
        for ind in INDICATORS + ["Complementary"]:
            df[ind] = indicatorrow[ind]
    return df


def analyze_language_class():
    df = get_article_tags()

    dfsum = pd.DataFrame()
    rownames = INDICATORS + ["Complementary"]
    dfsum['Name'] = rownames
    dfsum.set_index('Name')
    tps = []
    for name in rownames:
        tps.append(get_count(df, name, 1, 1))
    fps = []
    for name in rownames:
        fps.append(get_count(df, name, 0, 1))
    tns = []
    for name in rownames:
        tns.append(get_count(df, name, 0, 0))
    fns = []
    for name in rownames:
        fns.append(get_count(df, name, 1, 0))

    dfsum['TP'] = tps
    dfsum['FP'] = fps
    dfsum['TN'] = tns
    dfsum['FN'] = fns
    dfsum['Prec'] = dfsum.TP / (dfsum.TP + dfsum.FP)
    # dfsum['Negative-Prec'] = dfsum.TN / (dfsum.FN + dfsum.TN)
    dfsum['Rec'] = dfsum.TP / (dfsum.TP + dfsum.FN)
    # dfsum['specificity'] = dfsum.TN / (dfsum.FP + dfsum.TN)
    dfsum['Acc'] = (dfsum.TP + dfsum.TN) / (dfsum.TP + dfsum.TN + dfsum.FP + dfsum.FN)
    # dfsum['F1'] = (2 * dfsum.TP) / (2 * dfsum.TP + dfsum.FP + dfsum.FN)
    # dfsum['g-mean'] = numpy.sqrt(dfsum.Rec * dfsum.specificity)

    # dfsum['Noise'] = dfsum.TN + dfsum.FN
    return dfsum


def analyze_noise_class():
    df = get_article_tags()
    headers = INDICATORS + ["Complementary"]

    dfsum = pd.DataFrame()
    dfsum['Name'] = headers
    dfsum.set_index('Name')
    tps = []
    for name in headers:
        tps.append(get_count(df, name, 0, 0))
    fps = []
    for name in headers:
        fps.append(get_count(df, name, 1, 0))
    tns = []
    for name in headers:
        tns.append(get_count(df, name, 1, 1))
    fns = []
    for name in headers:
        fns.append(get_count(df, name, 0, 1))
    dfsum['TP'] = tps
    dfsum['FP'] = fps
    dfsum['TN'] = tns
    dfsum['FN'] = fns
    dfsum['Prec'] = dfsum.TP / (dfsum.TP + dfsum.FP)
    dfsum['Rec'] = dfsum.TP / (dfsum.TP + dfsum.FN)
    return dfsum


def get_count(df, indicator, expected, actual):
    return len(df[(df['tag'] == expected) & (df[indicator] == actual)].index)


def debug_evaluation():
    indicators = ["POS", "COP"]
    df = get_article_tags()
    for ind in indicators:
        print(ind + ": False Positives")
        dffp = df[(df.tag == 0) & (df[ind] == 1)]
        dffp = dffp['title']
        print(dffp)
        print("")
        print(ind + ": False Negatives")
        dffn = df[(df.tag == 1) & (df[ind] == 0)]
        dffn = dffn['title']
        print(dffn)
        print("")


if __name__ == "__main__":
    perform_eval()
    # df = analyze_language_class()
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    print(df)
    # debug_evaluation()
