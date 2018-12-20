from data import load_articledict, DATAP
import numpy
from scipy.sparse import dok_matrix
import csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
from json import dump

def get_negative_training_set():
    with open(DATAP + "/eval/random.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        A_random = []
        y = []
        for row in reader:
            A_random.append(row[0])
            y.append(row[1])

        return A_random, y


def get_seed(ad):
    S = [a for a in ad if ad[a]["Seed"]]
    y = [1 for s in S]
    return S, y


def build_f_to_id(FS, ad):
    Ff = {F: set(f for a in ad if F in ad[a] for f in ad[a][F]) for F in FS}
    F_len = 0
    fid = 0
    f_to_id = {}
    for F, fset in Ff.items():
        F_len += len(fset)
        for f in fset:
            f_to_id[F + "::" + f] = fid
            fid += 1
    return f_to_id


def build_id_to_a(A_p):
    matrix_id_to_a = {}
    aid = 0
    for a in A_p:
        matrix_id_to_a[aid] = a
        aid += 1
    return matrix_id_to_a


def build_doc_matrix(id_to_a, f_to_id, ad, FS):
    flen = len(f_to_id)
    matrix = dok_matrix((len(id_to_a), flen), dtype=numpy.int8)
    for aid, a in id_to_a.items():
        for F in FS:
            if F in ad[a]:
                for f in ad[a][F]:
                    matrix[aid, f_to_id[F + "::" + f]] = 1
    return matrix


def to_frame():
    ad = load_articledict()
    F_SetNames = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "COPHypernym", "Wikipedia_Lists"]

    A_seed, y_seed = get_seed(ad)
    A_neg, y_neg = get_negative_training_set()

    A_train = A_seed + A_neg
    y = y_seed + y_neg

    f_to_id = build_f_to_id(F_SetNames, ad)

    with open(DATAP+'/f_to_id.json', 'w', encoding='utf-8') as f:
        dump(f_to_id, f, indent=1)

    id_to_a_train = build_id_to_a(A_train)

    dc = DecisionTreeClassifier(random_state=0, criterion='entropy')

    X = build_doc_matrix(id_to_a_train, f_to_id, ad, F_SetNames)
    clf = dc.fit(X, y, sample_weight=None, check_input=True, X_idx_sorted=None)
    print("fitted")

    A_test = [a for a in ad if a not in A_train]

    id_to_a_test = build_id_to_a(A_test)
    X_test = build_doc_matrix(id_to_a_test, f_to_id, ad, F_SetNames)
    y_test = dc.predict(X_test)

    dot_data = export_graphviz(clf, out_file=DATAP + "/sltree.dot")
    graph = graphviz.Source(dot_data)
    #graph.render("softlang.pdf")


if __name__ == '__main__':
    to_frame()
