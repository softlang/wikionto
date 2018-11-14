from data import DATAP, ROOTS, INDICATORS
from pandas import DataFrame, Series
from json import load


def is_seed(l, d):
    return "Seed" in d[l] and d[l]["Seed"] == 1


def check_sl(l, d):
    return any(d[l][c] == 1 for c in INDICATORS)


def print_reduction():
    ton = 9
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    langdict = load(f)
    df = DataFrame(columns=['#seed', '#art', '#rec_art', '#rec_nonseed', 'reduced %'],
                   index=['Formal languages', 'Computer file formats', 'Installation software'])
    for c in ROOTS:
        articles = [a for a in langdict if c + "Depth" in langdict[a]]
        seed_articles = [sa for sa in articles if is_seed(sa, langdict)]
        recovered_articles = [ra for ra in articles if check_sl(ra, langdict)]
        nonseed_articles = [nsa for nsa in articles if not is_seed(nsa, langdict) and check_sl(nsa, langdict)]
        percentage = 100 * (len(recovered_articles) / len(articles))
        FL_overlap = [fl for fl in recovered_articles if "Category:Formal_LanguagesDepth" in langdict[fl]]
        print(len(FL_overlap))
        CFF_overlap = [cff for cff in recovered_articles if "Category:Computer_file_formatsDepth" in langdict[cff]]
        print(len(CFF_overlap))
        IS_overlap = [i for i in recovered_articles if "Category:Installation_softwareDepth" in langdict[i]]
        print(len(IS_overlap))
        df.loc[c.replace("Category:", "").replace("_", " ")] = Series(
            {'#art': len(articles), '#seed': len(seed_articles),
             '#rec_art': len(recovered_articles), '#rec_nonseed': len(nonseed_articles),
             'reduced %': percentage})
        print("----")
    print(df)
    print(df.to_latex())

    nogo = [l for l in langdict if is_seed(l, langdict) and not check_sl(l, langdict)]
    print(nogo)
    print(langdict["Augmented_Backus–Naur_Form"])


if __name__ == "__main__":
    print_reduction()
