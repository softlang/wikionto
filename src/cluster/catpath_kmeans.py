from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql.functions import regexp_extract
from os.path import join
from cluster.by_catpath import get_path_to_contents_article
from data import DATAP
from json import load
from mine_dump import start_time, stop_time


def annotate_catpath():
    with open(DATAP + '/dump/tocatlinks_category_reverse.json') as f:
        cat_to_cat_reverse = load(f)
        cat_to_cat_reverse = {int(key): [int(v) for v in values] for key, values in cat_to_cat_reverse.items()}
    with open(DATAP + '/dump/tocatlinks_article.json') as f:
        cat_front = load(f)
        cat_front = {int(key): [int(v) for v in values] for key, values in cat_front.items()}

    con = SparkConf() \
        .setAppName("Main").setMaster("local[" + str(4) + "]") \
        .set("spark.local.dir", join("", "pyspark")) \
        .set("spark.driver.memory", "12g") \
        .set("spark.executor.memory", "12g") \
        .set("spark.driver.maxResultSize", "12g") \
        .set("spark.executor.heartbeatInterval", "100s") \
        .set("spark.network.timeout", "1000s")
    sc = SparkContext(conf=con)
    sql_sc = SQLContext(sc)

    get_path = udf(lambda pid: get_path_to_contents_article(pid, cat_to_cat_reverse, cat_front), StringType())

    df = sql_sc.read.parquet(DATAP + '/dump/articles_annotated_catpath')
    df = df.repartition(1000)
    df = df.withColumn("path", get_path(df.id))
    df['id', 'path'].write.parquet(DATAP + '/dump/articles_annotated_catpath2')


def dataframe_without_text():
    con = SparkConf() \
        .setAppName("Main").setMaster("local[" + str(4) + "]") \
        .set("spark.local.dir", join("", "pyspark")) \
        .set("spark.driver.memory", "12g") \
        .set("spark.executor.memory", "12g") \
        .set("spark.driver.maxResultSize", "12g") \
        .set("spark.executor.heartbeatInterval", "100s") \
        .set("spark.network.timeout", "1000s")
    sc = SparkContext(conf=con)
    sql_sc = SQLContext(sc)

    schema = StructType([
        StructField("id", StringType()),
        StructField("title", StringType()),
        StructField("text", StringType())
    ])

    df = sql_sc.read \
        .format("com.databricks.spark.csv") \
        .schema(schema) \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ',') \
        .load(DATAP + '/dump/articles_inscope.csv')
    # df = df.repartition(1)
    df['id', 'title'].write \
        .parquet(DATAP + '/dump/articles_annotated_catpath')


if __name__ == "__main__":
    t = start_time()
    annotate_catpath()
    stop_time(t)
