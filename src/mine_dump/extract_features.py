from data import DATAP
from mine_dump.articles_tocsv import hms_string
from mine_dump.extractors.first_sentence import extract_first_sentence
from mine_dump.extractors.infobox_names import extract_names
from mine_dump.extractors.url_words import extract_urlpattern
from mine_dump.extractors.nlp_based import extract_nouns
from mine_dump.extractors.nlp_based import extract_hypernyms
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from os.path import join
import time
import os
from pathlib import Path


def extract_pre(sql_sc):
    schema = StructType([
        StructField("title", StringType()),
        StructField("text", StringType())
    ])
    first_ex = udf(extract_first_sentence, StringType())
    inf_ex2 = udf(extract_names, StringType())
    url_ex = udf(extract_urlpattern, StringType())

    df = sql_sc.read \
        .format("com.databricks.spark.csv") \
        .schema(schema) \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ',') \
        .load(DATAP + '/dump/articles.csv.bz2')

    df = df.withColumn("first_sentence", first_ex(df.text))
    df = df.withColumn('infoboxnames', inf_ex2(df.text))
    df = df.withColumn("urlwords", url_ex(df.title))
    df['title', 'first_sentence', 'infoboxnames', 'urlwords'].write \
        .format("com.databricks.spark.csv") \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ",") \
        .csv(DATAP + '/dump/articles_annotated_pre')


def extract_nlp(sql_sc):
    schema = StructType([
        StructField("title", StringType()),
        StructField("first_sentence", StringType()),
        StructField("infoboxnames", StringType()),
        StructField("urlwords", StringType())
    ])

    noun_ex = udf(extract_nouns, StringType())
    pos_ex = udf(extract_hypernyms, StringType())

    df = sql_sc.read \
        .format("com.databricks.spark.csv") \
        .schema(schema) \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ',') \
        .load(DATAP + '/dump/articles_annotated_pre.csv')
    df = df.withColumn("nouns", noun_ex(df.first_sentence))
    df = df.withColumn("pos_hyps", pos_ex(df.first_sentence))
    df['title', 'urlwords', 'infoboxnames', 'nouns', 'pos_hyps'].write \
        .format("com.databricks.spark.csv") \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ",") \
        .csv(DATAP + '/dump/articles_annotated')


def merge_csvs(folderpath, newfilepath):
    fnew = open(newfilepath, 'w', encoding='UTF-8')
    for filename in os.listdir(folderpath):
        if filename.endswith(".csv"):
            text = Path(os.path.join(folderpath, filename)).read_text(encoding='UTF-8')
            fnew.write(text + '\n')
    fnew.close()


def spark_stuff():
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
    extract_pre(sql_sc)
    # print(df.columns)


if __name__ == "__main__":
    # merge_csvs("C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre",
    #           "C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre.csv")
    start_time = time.time()
    spark_stuff()
    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))
