from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from json import load
from data import DATAP

def cluster():
    ld = load(open(DATAP+'\\temp\olangdict.json','r',encoding='UTF-8'))

    spark = SparkSession.builder\
                        .master("local")\
                        .appName("Word Count")\
                        .config("spark.some.config.option", "some-value")\
                        .getOrCreate()

    df = spark.createDataFrame([["0"],
                                ["1"],
                                ["2"],
                                ["3"],
                                ["4"]],
                               ["id"])
    df.show()

    vecAssembler = VectorAssembler(inputCols=["feat1", "feat2"], outputCol="features")
    new_df = vecAssembler.transform(df)

    kmeans = KMeans(k=2, seed=1)  # 2 clusters here
    model = kmeans.fit(new_df.select('features'))
    transformed = model.transform(new_df)
    print(transformed.show())


if __name__ == "__main__":
    cluster()