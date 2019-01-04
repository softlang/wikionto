from data import load_articledict, DATAP
from data.explore.feature_freq import analyze_feature_frequency
import numpy
from scipy.sparse import dok_matrix
import csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from json import dump

F_SETNAMES = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "COPHypernym", "Wikipedia_Lists"]


def get_random_training_set():
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
    with open(DATAP + '/f_to_id.json', 'w', encoding='utf-8') as f:
        dump(f_to_id, f, indent=1)
    return f_to_id


def build_id_to_a(A_p):
    matrix_id_to_a = {}
    aid = 0
    for a in A_p:
        matrix_id_to_a[aid] = a
        aid += 1
    return matrix_id_to_a


def build_doc_matrix(id_to_a, f_to_id, ad, F_Names):
    flen = len(f_to_id)
    matrix = dok_matrix((len(id_to_a), flen), dtype=numpy.int8)
    for aid, a in id_to_a.items():
        for F_Name in F_Names:
            if F_Name in ad[a]:
                for f in ad[a][F_Name]:
                    matrix[aid, f_to_id[F_Name + "::" + f]] = 1
    return matrix


def get_training_set(ad):
    A_seed, y_seed = get_seed(ad)
    A_neg, y_neg = get_random_training_set()

    A_train = A_seed + A_neg
    y = y_seed + y_neg

    f_to_id = build_f_to_id(F_SETNAMES, ad)

    id_to_a_train = build_id_to_a(A_train)

    return A_train, y, f_to_id, id_to_a_train


def train_decisiontree(ad):
    A_train, y, f_to_id, id_to_a_train = get_training_set(ad)

    dtc = DecisionTreeClassifier(random_state=0, criterion='entropy', min_samples_leaf=10)

    X = build_doc_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    clf = dtc.fit(X, y, check_input=True)
    print("fitted")
    export_graphviz(clf, out_file=DATAP + "/sltree.dot")


def test_decisiontree(dtc, ad, A_train, f_to_id):
    A_test = [a for a in ad if a not in A_train]
    id_to_a_test = build_id_to_a(A_test)
    X_test = build_doc_matrix(id_to_a_test, f_to_id, ad, F_SETNAMES)
    y_test = dtc.predict(X_test)


if __name__ == '__main__':
    ad = load_articledict()
    train_decisiontree(ad)
