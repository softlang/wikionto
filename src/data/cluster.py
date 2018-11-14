from data import DATAP
from json import load
from sklearn.cluster import KMeans
import pandas


def preprocess():
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    rows = ['CLDepth', 'CFFDepth', 'properties', 'Summary', 'cats', 'wikidataid', 'Revision']
    for cl in langdict:
        for f in langdict[cl]:
            if f in rows:
                langdict[cl][f] = 0
    print("loading")
    df = pandas.DataFrame(langdict)
    df = df.drop(rows=rows)
    print("transposing")
    df = df.transpose()
    print("Filling")
    df.fillna(0, inplace=True)
    f = open(DATAP + '/langdict_precluster.json', 'w', encoding="UTF8")
    df.to_json(f, orient='index')

def cluster():
    f = open(DATAP + '/langdict_precluster.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    df = pandas.DataFrame(langdict)

    dataset_array = df.values
    print(dataset_array.dtype)
    print(dataset_array)

    mat = df.as_matrix()
    # Using sklearn
    km = KMeans(n_clusters=5, n_jobs=-1)
    km.fit(mat)
    # Get cluster assignment labels
    labels = km.labels_
    # Format results as a DataFrame
    results = pandas.DataFrame([df.index, labels]).T.set_index(0)
    f = open(DATAP + '/langcluster.json', 'w', encoding="UTF8")
    results.to_json(f, orient='index')
    f.flush()
    f.close()
    print(results)


def is_valid():
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    f = open(DATAP + '/langcluster.json', 'r', encoding="UTF8")
    langcluster = load(f)
    f.close()
    gitclusters = set()
    for cl in langdict:
        if langdict[cl]["GitSeed"] == 1:
            gitclusters.add(langcluster[cl]["1"])
    return gitclusters


if __name__ == '__main__':
    preprocess()
    cluster()
    print(is_valid())
