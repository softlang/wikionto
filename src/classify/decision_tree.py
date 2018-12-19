from data import load_articledict, DATAP
import numpy
from pandas import read_csv
from scipy.sparse import dok_matrix
import csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

def to_frame():
    ad = load_articledict()
    S = [a for a in ad if ad[a]["Seed"]]

    FS = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "Wikipedia_Lists", "COPHypernym"]
    Ff = {F: set(f for a in ad if F in ad[a] for f in ad[a][F]) for F in FS}
    flen = 0
    fid = 0
    f_to_id = {}
    for F, fset in Ff.items():
        flen += len(fset)
        for f in fset:
            f_to_id[F + "::" + f] = fid
            fid += 1

    mat = dok_matrix((len(ad), flen), dtype=numpy.int8)
    matrix_id_to_a = {}
    aid = 0
    for a in ad:
        if a in S:
            continue
        matrix_id_to_a[aid] = a
        for F in FS:
            if F in ad[a]:
                for f in ad[a][F]:
                    mat[aid, f_to_id[F + "::" + f]] = 1
        aid += 1

    dc = DecisionTreeClassifier(random_state=0)
    S_ids = zip(range(len(S) - 1), S)
    S_mat = dok_matrix((len(S), flen), dtype=numpy.int8)
    for sid, s in S_ids:
        for F in FS:
            if F in ad[s]:
                for f in ad[s][F]:
                    S_mat[sid, f_to_id[F + "::" + f]] = 1

    y = [1 for s in S]
    X = S_mat
    clf = dc.fit(X, y, sample_weight=None, check_input=True, X_idx_sorted=None)
    print("fitted")

    dot_data = export_graphviz(clf, out_file=DATAP+"/sltree.dot")
    graph = graphviz.Source(dot_data)
    graph.render("iris")


def get_frame():
    df = read_csv(DATAP + "/articledict.csv", sep=",", quotechar="|", quoting=csv.QUOTE_ALL)
    return df


if __name__ == '__main__':
    to_frame()
