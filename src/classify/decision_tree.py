# my
from data import load_articledict, save_articledict, DATAP
from data.explore.feature_freq import analyze_feature_frequency
from data.eval.random_sampling import get_random_data
# learn
from scipy.sparse import dok_matrix
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import balanced_accuracy_score, f1_score, recall_score, precision_score
from sklearn.feature_selection import SelectKBest, SelectFpr, chi2, mutual_info_classif, f_classif
from classify.dottransformer import transform
from imblearn.under_sampling import RepeatedEditedNearestNeighbours
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN
# util
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from json import dump
from collections import Counter

F_SETNAMES = ["DbpediaInfoboxTemplate", "URL_Braces_Words", "COPHypernym", "Lemmas", "Wikipedia_Lists"]  # Lemmas,


def get_seed(ad):
    S = [a for a in ad if ad[a]["Seed"]]
    y = ['1' for s in S]
    return S, y


def build_f_to_id(FS, ad):
    freq = analyze_feature_frequency(ad, FS)
    print("Total number of features:" + str(len(freq)))
    fs = [f for f, count in freq.items() if count > 10]

    fids = list(range(len(fs)))
    f_to_id = dict(zip(fs, fids))
    with open(DATAP + '/f_to_id.json', 'w', encoding='utf-8') as f:
        dump(f_to_id, f, indent=1)
    print("Reduced number of features:" + str(len(f_to_id)))
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
                    if F_Name + "::" + f in f_to_id:
                        matrix[aid, f_to_id[F_Name + "::" + f]] = 1
    return matrix


def build_train_data(ad, f_to_id, splitnr=3000):
    A_seed, y_seed = get_seed(ad)
    # A_seed, y_seed = [], []
    A_random, y_random = get_random_data()
    A_train, y_train = A_seed + A_random[:splitnr], y_seed + y_random[:splitnr]
    id_to_a_train = build_id_to_a(A_train)
    X_train = build_dok_matrix(id_to_a_train, f_to_id, ad, F_SETNAMES)
    return X_train, y_train, id_to_a_train


def build_validation_data(ad, f_to_id, splitnr=3000, splitsize=1000):
    splitnr2 = splitnr + splitsize
    A_random, y_random = get_random_data()
    A_validate, y_validate = A_random[splitnr:splitnr2], y_random[splitnr:splitnr2]
    id_to_a_validate = build_id_to_a(A_validate)
    X_validate = build_dok_matrix(id_to_a_validate, f_to_id, ad, F_SETNAMES)
    return X_validate, y_validate, id_to_a_validate


def build_eval_data_single(ad, f_to_id):
    A_eval, y_eval = zip(*[(a, ad[a]["SL1"]) for a in ad if "SL1" in ad[a]])
    id_to_a_eval = build_id_to_a(A_eval)
    X_eval = build_dok_matrix(id_to_a_eval, f_to_id, ad, F_SETNAMES)
    return X_eval, y_eval, id_to_a_eval


def build_eval_data_double(ad, f_to_id):
    A_eval, y_eval = zip(*[(a, ad[a]["SL2"]) for a in ad if "SL2" in ad[a]])
    id_to_a_eval = build_id_to_a(A_eval)
    X_eval = build_dok_matrix(id_to_a_eval, f_to_id, ad, F_SETNAMES)
    return X_eval, y_eval, id_to_a_eval


def train_decisiontree_FPR(configurationname, train_data, score_function, undersam=False, oversam=False, export=False):
    print("Training with configuration " + configurationname)
    X_train, y_train, id_to_a_train = train_data
    dtc = DecisionTreeClassifier(random_state=0)

    print("Feature Selection")
    # selector = SelectFpr(score_function)
    selector = SelectFpr(score_function)
    result = selector.fit(X_train, y_train)
    X_train = selector.transform(X_train)

    fitted_ids = [i for i in result.get_support(indices=True)]

    print("Apply Resampling")
    print(Counter(y_train))
    if undersam and not oversam:
        renn = RepeatedEditedNearestNeighbours()
        X_train, y_train = renn.fit_resample(X_train, y_train)
    if oversam and not undersam:
        # feature_indices_array = list(range(len(f_to_id)))
        # smote_nc = SMOTENC(categorical_features=feature_indices_array, random_state=0)
        # X_train, y_train = smote_nc.fit_resample(X_train, y_train)
        sm = SMOTE(random_state=42)
        X_train, y_train = sm.fit_resample(X_train, y_train)
    if oversam and undersam:
        smote_enn = SMOTEENN(random_state=0)
        X_train, y_train = smote_enn.fit_resample(X_train, y_train)
    print(Counter(y_train))

    print("Train Classifier")
    dtc = dtc.fit(X_train, y_train, check_input=True)

    if export:
        export_graphviz(dtc, out_file=DATAP + "/temp/trees/sltree_" + configurationname + ".dot", filled=True)
        transform(fitted_ids)

    print("Self Accuracy: " + str(dtc.score(X_train, y_train)))

    return selector, dtc


def train_decisiontree_with(configurationname, train_data, k, score_function, undersam=False, oversam=False,
                            export=False):
    assert k > 0
    print("Training with configuration " + configurationname)
    X_train, y_train, id_to_a_train = train_data
    dtc = DecisionTreeClassifier(random_state=0)

    print("Feature Selection")
    # selector = SelectFpr(score_function)
    selector = SelectKBest(score_function, k=k)
    result = selector.fit(X_train, y_train)
    X_train = selector.transform(X_train)

    fitted_ids = [i for i in result.get_support(indices=True)]

    print("Apply Resampling")
    print(Counter(y_train))
    if undersam and not oversam:
        renn = RepeatedEditedNearestNeighbours()
        X_train, y_train = renn.fit_resample(X_train, y_train)
    if oversam and not undersam:
        # feature_indices_array = list(range(len(f_to_id)))
        # smote_nc = SMOTENC(categorical_features=feature_indices_array, random_state=0)
        # X_train, y_train = smote_nc.fit_resample(X_train, y_train)
        sm = SMOTE(random_state=42)
        X_train, y_train = sm.fit_resample(X_train, y_train)
    if oversam and undersam:
        smote_enn = SMOTEENN(random_state=0)
        X_train, y_train = smote_enn.fit_resample(X_train, y_train)
    print(Counter(y_train))

    print("Train Classifier")
    dtc = dtc.fit(X_train, y_train, check_input=True)

    if export:
        export_graphviz(dtc, out_file=DATAP + "/temp/trees/sltree_" + configurationname + ".dot", filled=True)
        transform(fitted_ids, configurationname)

    print("Self Accuracy: " + str(dtc.score(X_train, y_train)))

    return selector, dtc


def classifier_score(id_to_a_test, classifier, selector, X_test, y_test):
    X_test = selector.transform(X_test)
    y_test_predicted = classifier.predict(X_test)

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for x in range(len(y_test)):
        if y_test[x] == '1' and y_test_predicted[x] == '1':
            tp += 1
        if y_test[x] == '1' and y_test_predicted[x] == '0':
            fn += 1
            print("FN: " + id_to_a_test[x])
        if y_test[x] == '0' and y_test_predicted[x] == '0':
            tn += 1
        if y_test[x] == '0' and y_test_predicted[x] == '1':
            fp += 1
            # print("FP: " + id_to_a_test[x])
    print("Recall: " + str(tp / (tp + fn)))
    print("Specificity: " + str(tn / (fp + tn)))

    return {"TP": tp, "TN": tn, "FP": fp, "FN": fn,
            "Balanced_Accuracy": balanced_accuracy_score(y_test, y_test_predicted),
            "F_Measure": f1_score(y_test, y_test_predicted, pos_label='1'),
            "Recall": recall_score(y_test, y_test_predicted, pos_label='1'),
            "Negative-Recall": tn / (fp + tn),
            "Precision": precision_score(y_test, y_test_predicted, pos_label='1'),
            "Accuracy": classifier.score(X_test, y_test)}


def train_decisiontree_exploration(ad, trainsize):
    evals = []
    f_to_id, fs = build_f_to_id(F_SETNAMES, ad)
    # training
    X_train, y_train, id_to_a_train = build_train_data(ad, f_to_id, trainsize)
    train_data = X_train, y_train, id_to_a_train
    # validation
    # X_validate, y_validate, id_to_validate = build_validation_data(ad, f_to_id, 3000, 1000)
    # test
    X_eval2, y_eval2, id_to_a_eval2 = build_eval_data_double(ad, f_to_id)

    id_to_a_all = build_id_to_a([a for a in ad])
    X_all0 = build_dok_matrix(id_to_a_all, f_to_id, ad, F_SETNAMES)

    k0, kmax, kstep = (1, 100, 1)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_chi2_NoResampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, chi2)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_f_classif_NoResampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, f_classif)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_mutual_info_classif_NoResampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, mutual_info_classif)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_chi2_Oversampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, chi2, oversam=True)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_f_classif_Oversampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, f_classif, oversam=True)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    for k in range(k0, kmax, kstep):
        configurationname = "KBest_" + str(k) + "_mutual_info_classif_Oversampling"
        selector, classifier = train_decisiontree_with(configurationname, train_data, k, mutual_info_classif,
                                                       oversam=True)
        X_allk = selector.transform(X_all0)
        y_all = classifier.predict(X_allk)
        eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
        eval_dict["Positive"] = len([y for y in y_all if y == '1'])
        eval_dict["Negative"] = len([y for y in y_all if y == '0'])
        eval_dict["Name"] = configurationname + "_eval2"
        evals.append(eval_dict)

    return pd.DataFrame(evals)


def final_classification(ad, test=True):
    f_to_id, fs = build_f_to_id(F_SETNAMES, ad)
    # training
    X_train, y_train, id_to_a_train = build_train_data(ad, f_to_id, 4000)
    train_data = X_train, y_train, id_to_a_train
    # validation
    # X_validate, y_validate, id_to_validate = build_validation_data(ad, f_to_id, 3000, 1000)
    # test
    X_eval2, y_eval2, id_to_a_eval2 = build_eval_data_double(ad, f_to_id)

    id_to_a_all = build_id_to_a([a for a in ad])
    X_all0 = build_dok_matrix(id_to_a_all, f_to_id, ad, F_SETNAMES)

    k = 22
    configurationname = "KBest_" + str(k) + "_mutual_info_classif_Oversampling"
    selector, classifier = train_decisiontree_with(configurationname, train_data, k, mutual_info_classif,
                                                   oversam=True, export=True)
    X_allk = selector.transform(X_all0)
    y_all = classifier.predict(X_allk)

    if not test:
        for x in range(len(y_all)):
            title = id_to_a_all[x]
            ad[title]["Class"] = y_all[x]
        save_articledict(ad)

    eval_dict = classifier_score(id_to_a_eval2, classifier, selector, X_eval2, y_eval2)
    eval_dict["Positive"] = len([y for y in y_all if y == '1'])
    eval_dict["Negative"] = len([y for y in y_all if y == '0'])
    eval_dict["Name"] = configurationname + "_eval2"

    return pd.DataFrame([eval_dict])


if __name__ == '__main__':
    ad = load_articledict()
    df = train_decisiontree_exploration(ad, 2000)
    df = df.set_index("Name")
    df.to_csv(DATAP + "/exploration_2000.csv")
    df = train_decisiontree_exploration(ad, 3000)
    df = df.set_index("Name")
    df.to_csv(DATAP + "/exploration_3000.csv")
    df = train_decisiontree_exploration(ad, 4000)
    df = df.set_index("Name")
    df.to_csv(DATAP + "/exploration_4000.csv")
    # ax = df.plot.scatter(x="FPR", y="TPR", style="x", c="blue")
    # df.plot(x="k", y=["Recall", "Negative-Recall", "Precision", "Balanced_Accuracy", "F_Measure"], title="KBest")
    # df = train_decisiontree_exploration(ad, splitnr=2000)
    # df.plot.scatter(x="FPR", y="TPR", ax=ax, style="x", c="orange")
    # df = train_decisiontree_exploration(ad, splitnr=3000)
    # df.plot.scatter(x="FPR", y="TPR", ax=ax, style="x", c="red")
    # df = train_decisiontree_exploration(ad, train_data, undersam=True)
    # df.to_csv(DATAP + "/dct_kbest_undersam.csv")
    # df.plot.scatter(x="FPR", y="TPR", ax=ax, style="o", c="purple")
    # df.plot(x="k", y=["TPR", "FPR", "Balanced_Accuracy", "F_Measure", "Self_Accuracy"], title="KBest Undersampling")
    # df = train_decisiontree_exploration(ad, train_data, oversam=True)
    # df.to_csv(DATAP + "/dct_kbest_oversam.csv")
    # df.plot.scatter(x="FPR", y="TPR", ax=ax, style="o", c="orange")
    # df.plot(x="k", y=["TPR", "FPR", "Balanced_Accuracy", "F_Measure", "Self_Accuracy"], title="KBest Oversampling")
    # df = train_decisiontree_exploration(ad, train_data, oversam=True, undersam=True)
    # df.to_csv(DATAP + "/dct_kbest_combinesam.csv")
    # df.plot.scatter(x="FPR", y="TPR", ax=ax, style="o", c="red")
    # df.plot(x="k", y=["TPR", "FPR", "Balanced_Accuracy", "F_Measure", "Self_Accuracy"], title="KBest Combined Resampling")
    # plt.show()
