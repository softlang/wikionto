from data import load_articledict, DATAP
from data.explore.feature_freq import analyze_feature_frequency
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import dok_matrix
import csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.feature_selection import SelectKBest, chi2
from yellowbrick.features import RFECV
from json import dump

F_SETNAMES = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "COPHypernym", "Wikipedia_Lists"]


def get_random_data():
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
    fs = [F + "::" + f for F, fset in Ff.items() for f in fset]
    fids = list(range(len(fs)))
    f_to_id = dict(zip(fs, fids))
    with open(DATAP + '/f_to_id.json', 'w', encoding='utf-8') as f:
        dump(f_to_id, f, indent=1)
    return f_to_id, fs


def build_id_to_a(A_p, aid=0):
    matrix_id_to_a = {}
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


def get_data_sets(ad):
    A_seed, y_seed = get_seed(ad)
    A_random, y_random = get_random_data()

    A_data, y_data = A_random + A_seed, y_random + y_seed

    A_test, y_test = A_data[:500], y_data[:500]
    A_train, y_train = A_data[:-500], y_data[:-500]

    (f_to_id, fs) = build_f_to_id(F_SETNAMES, ad)

    return (A_train, y_train), (A_test, y_test), (f_to_id, fs)


def train_decisiontree_with(A_train, y_train, A_test, y_test, f_to_id, fs, id_to_a_train, k_best):
    dtc = DecisionTreeClassifier(random_state=0)

    X_train = build_doc_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    if k_best > 0:
        X_train = SelectKBest(k=k_best).fit_transform(X_train, y_train)
    clf = dtc.fit(X_train, y_train, check_input=True)
    # print("fitted")
    export_graphviz(clf, out_file=DATAP + "/temp/trees/sltree" + str(k_best) + ".dot", impurity=True, filled=True,
                    leaves_parallel=True, proportion=True)

    id_to_a_test = build_id_to_a(A_test)
    X_test = build_doc_matrix(id_to_a_test, f_to_id, ad, F_SETNAMES)
    print("Learned with " + str(k_best) + ": " + str(dtc.score(X_train, y_train)) + " self accuracy ")
    # "and " + str(dtc.score(X_test, y_test)) + " test accuracy")

    y_test_predicted = dtc.predict(X_train)
    y_test = y_train
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for x in range(len(y_test)):
        if y_test[x] == '1' and y_test_predicted[x] == '1':
            tp += 1
        if y_test[x] == '1' and y_test_predicted[x] == '0':
            fn += 1
        if y_test[x] == '0' and y_test_predicted[x] == '0':
            tn += 1
        if y_test[x] == '0' and y_test_predicted[x] == '1':
            fp += 1

    print("TP:" + str(tp) + " TN:" + str(tn) + " FP:" + str(fp) + " FN:" + str(fn))
    print("TPR:" + str(tp / (tp + fn)) + " PPV:" + str(tp / (tp + fp)))
    print("------")

    return {"TP": tp, "TN": tn, "FP": fp, "FN": fn, "k": k_best}


def train_decisiontree_exploration(ad):
    (A_train, y_train), (A_test, y_test), (f_to_id, fs) = get_data_sets(ad)
    id_to_a_train = build_id_to_a(A_train)
    evals = []
    for k_best in range(0, 100, 1):
        eval_dict = train_decisiontree_with(A_train, y_train, A_test, y_test, f_to_id, fs, id_to_a_train, k_best)
        evals.append(eval_dict)
    df = pd.DataFrame(evals)
    df["TPR"] = df["TP"] / (df["TP"] + df["FN"])

    df.plot(x="k", y="TPR")
    plt.show()


def crossvalidation_search_decision_tree(ad):
    (A_train, y_train), (A_test, y_test), f_to_id = get_data_sets(ad)
    A = A_train + A_test
    id_to_a_train = build_id_to_a(A)
    y = y_train + y_test
    dtc = DecisionTreeClassifier(random_state=0)
    selector = RFECV(dtc)
    X = build_doc_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    print("built matrix")
    selector = selector.fit(X, y)
    print("finished fit")
    selector.poof()
    # export_graphviz(selector.estimator_, out_file=DATAP + "/temp/trees/sltree_crossval.dot")


if __name__ == '__main__':
    ad = load_articledict()
    # crossvalidation_search_decision_tree(ad)
    train_decisiontree_exploration(ad)
