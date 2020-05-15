import pandas as pd
import numpy
from scipy.sparse import dok_matrix, coo_matrix
from sklearn.feature_selection import mutual_info_classif, SelectKBest
from sklearn.tree import DecisionTreeClassifier
from data import load_articledict
from data.eval.random_sampling import get_random_data

DATASPARK = "W:/Data/Wikipedia/spark"
FEATUREJSON = DATASPARK+"/featuresJSON/part-00000-10d943e0-5c94-4432-970d-1971f93d8b89-c000.json"

def n(title):
    return title.replace("_", " ").lower()


def training_data():
    ad = load_articledict()

    titles = [n(a) for a in ad if ad[a]["Seed"]]
    y = ['1' for t in titles]

    titles_r, y_r = get_random_data()
    return titles + titles_r, y + y_r


def build_index(df, title_to_rowindex, feature_to_colindex):
    for index, row in df.iterrows():
        title = row['title']
        features = row['features']
        title_to_rowindex[n(title)] = index
        for f in features:
            if f not in feature_to_colindex:
                findex = len(feature_to_colindex)
                feature_to_colindex[f] = findex
    return title_to_rowindex, feature_to_colindex


def df_to_dok_matrix(df_features_reader2, feature_to_colindex):
    print("Create Sparse Matrix")
    matrix = dok_matrix((len(title_to_rowindex), len(feature_to_colindex)), dtype=numpy.int8)
    print("   dimensions: " + str(len(title_to_rowindex)) + " x " + str(len(feature_to_colindex)))
    for chunk in df_features_reader2:
        print("Process chunk")
        matrix = chunk_to_dok_matrix(chunk, feature_to_colindex, matrix)
    return matrix


def chunk_to_dok_matrix(df, feature_to_index, matrix):
    for index, row in df.iterrows():
        features = row['features']
        for f in features:
            index_f = feature_to_index[f]
            matrix[index, index_f] = 1
    return matrix


def df_to_coo_matrix(df_features_reader, feature_to_index):
    chunk_counter = 1
    data, rows, cols = [], [], []
    for chunk in df_features_reader:
        print("  chunk" + str(chunk_counter))
        chunk_counter += 1
        data, rows, cols = chunk_to_coo_matrix(chunk, feature_to_index, data, rows, cols)
    return coo_matrix((numpy.array(data, dtype=numpy.uint8),
                       (numpy.array(rows, dtype=numpy.uint32), numpy.array(cols, dtype=numpy.uint32))))


def chunk_to_coo_matrix(chunk, feature_to_index, data, rows, cols):
    for row_index, row in chunk.iterrows():
        features = row['features']
        for f in features:
            col_index = feature_to_index[f]
            data.append(1)
            rows.append(row_index)
            cols.append(col_index)
    return data, rows, cols


def read_features_table():
    return pd.read_json(
        FEATUREJSON,
        dtype={'title': object, 'features': "category"}, lines=True, orient='records', chunksize=500000)


if __name__ == '__main__':
    print("Creating Reader Object")
    df_features_reader = read_features_table()
    df_features_reader2 = read_features_table()

    print("Creating Index")
    feature_to_colindex = dict()
    title_to_rowindex = dict()
    chunk_counter = 1
    for chunk in df_features_reader:
        print("  chunk" + str(chunk_counter))
        chunk_counter += 1
        title_to_rowindex, feature_to_colindex = build_index(chunk, title_to_rowindex, feature_to_colindex)

    print("Build coo matrix")
    matrix = df_to_coo_matrix(df_features_reader2, feature_to_colindex)

    print("Check training rows - Some articles in the old training data may have been lost")
    titles_train_pre, y_train_pre = training_data()
    titles_train, y_train = [], []
    for i in range(len(titles_train_pre)):
        title = n(titles_train_pre[i])
        if title in title_to_rowindex:
            titles_train.append(title)
            y_train.append(y_train_pre[i])
    lost_titles = [t for t in titles_train_pre if t not in title_to_rowindex]
    print(str(lost_titles))

    print("Extract Training Matrix from Full Matrix")
    trainindexlist = [title_to_rowindex[t] for t in titles_train]
    select_ind = numpy.array(trainindexlist)
    matrix = matrix.tocsr()
    X_train = matrix[select_ind, :]

    print("Feature Selection")
    selector = SelectKBest(mutual_info_classif, k=22)
    result = selector.fit(X_train, y_train)
    X_train = selector.transform(X_train)

    print("Train Decision Tree")
    dtc = DecisionTreeClassifier(random_state=0)
    dtc = dtc.fit(X_train, y_train, check_input=True)
    print("Self Accuracy: " + str(dtc.score(X_train, y_train)))
