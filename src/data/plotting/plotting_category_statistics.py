from data import load_catdict, KEYWORDS
import matplotlib.pyplot as plt
from pandas import DataFrame, Series


def plot_statistics():
    cd = load_catdict()
    df = DataFrame(columns=['#Positive', '#Negative'], index=cd.keys())
    for c in cd:
        df.loc[c] = Series({'#Positive': cd[c]["#Positive"],
                            '#Negative': cd[c]["#Negative"]})
    # print(df)
    df = df.fillna(0)
    # print(df)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    df = df.sort_values(["#Positive", "#Negative"], ascending=[0, 1])
    # df.plot(x="#Positive", y="#Negative", kind="scatter", ax=ax[0], color="blue")
    df[(df["#Positive"] + df["#Negative"]) < 5].plot(y="#Positive", kind="line", ax=ax, color="grey")
    df[(df["#Positive"] == 0) & (df["#Negative"] == 0)].plot(y="#Negative", kind="line", ax=ax, color="red")

    ax.set_title('Assessing Categories - Lines')
    plt.show()


def plot_scatter(minsize, r):
    cd = load_catdict()
    cat_strats, article_strats = get_strats(minsize, r, cd)
    lonelies_cats, tps_cats, tns_cats, mixed_cats = cat_strats

    positive_url_cats = [c for c in cd if cd[c]["URLPattern"] or cd[c]["URLBracesPattern"]]

    lonelies = DataFrame(columns=['#Positive', '#Negative'], index=lonelies_cats)
    for c in lonelies_cats:
        lonelies.loc[c] = Series({'#Positive': cd[c]["#Positive"], '#Negative': cd[c]["#Negative"]})
    tps = DataFrame(columns=['#Positive', '#Negative'], index=tps_cats)
    for c in tps_cats:
        tps.loc[c] = Series({'#Positive': cd[c]["#Positive"], '#Negative': cd[c]["#Negative"]})
    tns = DataFrame(columns=['#Positive', '#Negative'], index=tns_cats)
    for c in tns_cats:
        tns.loc[c] = Series({'#Positive': cd[c]["#Positive"], '#Negative': cd[c]["#Negative"]})
    mixed = DataFrame(columns=['#Positive', '#Negative'], index=mixed_cats)
    for c in mixed_cats:
        mixed.loc[c] = Series({'#Positive': cd[c]["#Positive"], '#Negative': cd[c]["#Negative"]})
    positive_url = DataFrame(columns=['#Positive', '#Negative'], index=positive_url_cats)
    for c in positive_url_cats:
        positive_url.loc[c] = Series({'#Positive': cd[c]["#Positive"], '#Negative': cd[c]["#Negative"]})

    linedf = DataFrame(columns=['#Positive', '#Negative'], index=cd.keys())
    x = 1
    for c in cd:
        if x < 2000:
            linedf.loc[c] = Series({'#Positive': x,
                                    '#Negative': x})
        x += 1

    fig, ax = plt.subplots(nrows=1, ncols=1)
    mixed.plot(x="#Positive", y="#Negative", kind="scatter", ax=ax, color="blue", loglog=False)
    lonelies.plot(x="#Positive", y="#Negative", kind="scatter", ax=ax, color="grey", marker="x")
    tps.plot(x="#Positive", y="#Negative", kind="scatter", ax=ax, color="green")
    tns.plot(x="#Positive", y="#Negative", kind="scatter", ax=ax, color="black")
    linedf.plot(x="#Positive", y="#Negative", ls="--", ax=ax, color="grey")
    positive_url.plot(x="#Positive", y="#Negative", kind="scatter", marker="x", ax=ax, color="pink")

    ax.set_title('Assessing Categories - ' + str(r))
    ax.legend(["Regression Line", "Mixed", "Too Small", "Positive", "Negative"])
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()


def get_strats(minsize, r, cd=load_catdict()):
    lonelies_cats = [c for c in cd if (cd[c]["#Positive"] + cd[c]["#Negative"]) < minsize]
    tps_cats = [c for c in cd if cd[c]["#Positive"] > minsize and (cd[c]["#Positive"] * r) > cd[c]["#Negative"]]
    tns_cats = [c for c in cd if cd[c]["#Negative"] > minsize and (cd[c]["#Negative"] * r) > cd[c]["#Positive"]]
    mixed_cats = [c for c in cd if ((cd[c]["#Positive"] + cd[c]["#Negative"]) >= minsize) and
                  (cd[c]["#Positive"] * r) <= cd[c]["#Negative"] and (cd[c]["#Negative"] * r) <= cd[c]["#Positive"]]

    cat_strats = lonelies_cats, tps_cats, tns_cats, mixed_cats
    atps = set(a for c in tps_cats for a in cd[c]["articles"])
    atns = set(a for c in tns_cats for a in cd[c]["articles"])
    amixed = set(a for c in mixed_cats for a in cd[c]["articles"] if a not in atps and a not in atns)
    alonelies = set(
        a for c in lonelies_cats if "articles" in cd[c] for a in cd[c]["articles"] if
        a not in atps and a not in atns and a not in amixed)
    article_strats = alonelies, atps, atns, amixed
    print("Presumably Positive: " + str(len(atps)))
    print("Presumably Negative: " + str(len(atns)))
    print("Presumably Mixed: " + str(len(amixed)))
    print("Presumably Lonely: " + str(len(alonelies)))
    return cat_strats, article_strats


if __name__ == '__main__':
    plot_scatter(5, 0.3)
