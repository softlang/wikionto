from data import load_articledict, DATAP
from data.explore.feature_freq import analyze_feature_frequency
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import dok_matrix
import csv
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import balanced_accuracy_score, f1_score, recall_score, precision_score
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif
from yellowbrick.features import RFECV
from json import dump
from classify.dottransformer import transform

F_SETNAMES = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "COPHypernym", "Wikipedia_Lists", "Lemmas"] #Words

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
    print("Total number of features:" + str(len(f_to_id)))
    return f_to_id, fs


def build_id_to_a(A_p, aid=0):
    matrix_id_to_a = {}
    for a in A_p:
        matrix_id_to_a[aid] = a
        aid += 1
    return matrix_id_to_a


def build_dok_matrix(id_to_a, f_to_id, ad, F_Names):
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


def train_decisiontree_with(y_train, y_test, f_to_id, id_to_a_train, id_to_a_test, k, export=True):
    assert k > 0

    dtc = DecisionTreeClassifier(random_state=0)
    selector = SelectKBest(chi2, k=k)

    X_train = build_dok_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    X_test = build_dok_matrix(id_to_a_test, f_to_id, ad, F_SETNAMES)

    result = selector.fit(X_train, y_train)
    X_train = selector.transform(X_train)
    X_test = selector.transform(X_test)
    fitted_ids = [i for i in result.get_support(indices=True)]
    flen = len(fitted_ids)

    clf = dtc.fit(X_train, y_train, check_input=True)

    if export:
        export_graphviz(clf, out_file=DATAP + "/temp/lemmatrees2/sltree" + str(k) + ".dot", filled=True)
        transform(fitted_ids, k)

    # id_to_a_test = build_id_to_a(A_test)
    # X_test = build_doc_matrix(id_to_a_test, f_to_id, ad, F_SETNAMES)
    print("Learned with " + str(k) + ": " + str(dtc.score(X_train, y_train)) + " self accuracy ")
    # "and " + str(dtc.score(X_test, y_test)) + " test accuracy")

    y_test_predicted = dtc.predict(X_test)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for x in range(len(y_test)):
        if y_test[x] == '1' and y_test_predicted[x] == '1':
            tp += 1
        if y_test[x] == '1' and y_test_predicted[x] == '0':
            fn += 1
            print(str(x)+":"+str(id_to_a_test[x]))
        if y_test[x] == '0' and y_test_predicted[x] == '0':
            tn += 1
        if y_test[x] == '0' and y_test_predicted[x] == '1':
            fp += 1

    return selector, dtc, {"TP": tp, "TN": tn, "FP": fp, "FN": fn, "k": k, "#Features": flen,
                           "Balanced_Accuracy": balanced_accuracy_score(y_test, y_test_predicted),
                           "F_Measure": f1_score(y_test, y_test_predicted, pos_label='1'),
                           "TPR": recall_score(y_test, y_test_predicted, pos_label='1'),
                           "PPV": precision_score(y_test, y_test_predicted, pos_label='1')}


def train_decisiontree_exploration(ad):
    (A_train, y_train), (A_test, y_test), (f_to_id, fs) = get_data_sets(ad)
    id_to_a_train = build_id_to_a(A_train)
    id_to_a_test = build_id_to_a(A_test)
    evals = []
    id_to_a_all = build_id_to_a([a for a in ad])
    X_all0 = build_dok_matrix(id_to_a_all, f_to_id, ad, F_SETNAMES)
    for k in range(1, 20, 1):
        selector, dtc, eval_dict = train_decisiontree_with(y_train, y_test, f_to_id, id_to_a_train, id_to_a_test, k)
        X_allk = selector.transform(X_all0)
        y_all = dtc.predict(X_allk)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        evals.append(eval_dict)
    df = pd.DataFrame(evals)
    ax = df.plot(x="k", y="TPR")
    df.plot(x="k", y="PPV", ax=ax)
    df.plot(x="k", y="Balanced_Accuracy", ax=ax)
    df.plot(x="k", y="F_Measure", ax=ax)
    plt.show()
    df.to_csv(DATAP + "/dct_kbest.csv")


def crossvalidation_search_decision_tree(ad):
    (A_train, y_train), (A_test, y_test), f_to_id = get_data_sets(ad)
    A = A_train + A_test
    id_to_a_train = build_id_to_a(A)
    y = y_train + y_test
    dtc = DecisionTreeClassifier(random_state=0)
    selector = RFECV(dtc)
    X = build_dok_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    print("built matrix")
    selector = selector.fit(X, y)
    print("finished fit")
    selector.poof()
    # export_graphviz(selector.estimator_, out_file=DATAP + "/temp/trees/sltree_crossval.dot")


if __name__ == '__main__':
    ad = load_articledict()
    # crossvalidation_search_decision_tree(ad)
    train_decisiontree_exploration(ad)
