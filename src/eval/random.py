from data import DATAP
from json import load
import random
import pandas as pd
import numpy

def perform_eval():
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)

    articles_visited = set()
    with open(DATAP + '/eval/random.csv', 'r', encoding="UTF8") as f:
        olddata = ""
        count = 0
        for line in f:
            olddata += line
            count += 1
            articles_visited.add(line.split(",")[0].replace("|", ""))

    with open(DATAP + '/eval/random.csv', 'w', encoding="UTF8") as f:
        f.write(olddata)
        articles = list(langdict.keys())
        articles.sort()

        for x in range(count, 1483):
            index = random.randint(0, len(langdict))
            article = articles[index]
            if article in articles_visited:
                x -= 1
            else:
                articles_visited.add(article)
                print(str(x) + " https://en.wikipedia.org/wiki/" + article)
                agreement = ""
                while agreement not in ["yes", "no"]:
                    agreement = input("Enter 'yes' or 'no'!")
                if agreement == "yes":
                    agreement_int = "1"
                if agreement == "no":
                    agreement_int = "0"
                f.write("|" + article + "|,|" + agreement_int + "|\n")


def get_classification(title, langdict):
    indicators = ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS"]
    resultdict = {ind: langdict[title][ind] for ind in indicators}
    for ind in indicators:
        if ind not in resultdict:
            resultdict[ind] = 0
    resultdict['Complementary'] = sum(resultdict.values()) > 0
    return resultdict


def get_article_tags():
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)
    with open(DATAP + '/eval/random.csv', 'r', encoding="UTF8") as f:
        df = pd.read_csv(f, delimiter=',', quotechar='|', names=['title', 'tag'])
        df.set_index('title')
        vi = []
        urlbp = []
        iwl = []
        pos = []
        comp = []
        for title in df['title']:
            classifdict = get_classification(title, langdict)
            vi.append(classifdict['ValidInfobox'])
            urlbp.append(classifdict['URLBracesPattern'])
            iwl.append(classifdict['In_Wikipedia_List'])
            pos.append(classifdict['POS'])
            comp.append(classifdict['Complementary'])
        df['ValidInfobox'] = vi
        df['URLBracesPattern'] = urlbp
        df['In_Wikipedia_List'] = iwl
        df['POS'] = pos
        df['Complementary'] = comp
    return df


def analyze_language_class():
    df = get_article_tags()

    dfsum = pd.DataFrame()
    dfsum['Name'] = ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]
    dfsum.set_index('Name')
    tps = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        tps.append(get_count(df, name, 1, 1))
    fps = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        fps.append(get_count(df, name, 0, 1))
    tns = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        tns.append(get_count(df, name, 0, 0))
    fns = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        fns.append(get_count(df, name, 1, 0))

    dfsum['TP'] = tps
    dfsum['FP'] = fps
    dfsum['TN'] = tns
    dfsum['FN'] = fns
    dfsum['Prec'] = dfsum.TP / (dfsum.TP + dfsum.FP)
    dfsum['Rec'] = dfsum.TP / (dfsum.TP + dfsum.FN)
    print(dfsum)


def analyze_noise_class():
    df = get_article_tags()

    dfsum = pd.DataFrame()
    dfsum['Name'] = ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]
    dfsum.set_index('Name')
    tps = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        tps.append(get_count(df, name, 0, 0))
    fps = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        fps.append(get_count(df, name, 1, 0))
    tns = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        tns.append(get_count(df, name, 1, 1))
    fns = []
    for name in ['ValidInfobox', "URLBracesPattern", "In_Wikipedia_List", "POS", "Complementary"]:
        fns.append(get_count(df, name, 0, 1))

    dfsum['TP'] = tps
    dfsum['FP'] = fps
    dfsum['TN'] = tns
    dfsum['FN'] = fns
    dfsum['Prec'] = dfsum.TP / (dfsum.TP + dfsum.FP)
    dfsum['Rec'] = dfsum.TP / (dfsum.TP + dfsum.FN)
    print(dfsum)


def get_count(df, indicator, expected, actual):
    return len(df[(df['tag'] == expected) & (df[indicator] == actual)].index)


def debug_evaluation():
    df = get_article_tags()
    print(df[(df.tag == 0) & (df.POS == 1)])


if __name__ == "__main__":
    analyze_language_class()
