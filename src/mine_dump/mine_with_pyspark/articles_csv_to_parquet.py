from data import DATAP
from pyspark.sql.types import StructType, StructField, StringType
from mine_dump.pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from os.path import join


def convert():
    schema = StructType([
        StructField("title", StringType()),
        StructField("text", StringType())
    ])
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
    df = sql_sc.read \
        .format("com.databricks.spark.csv") \
        .schema(schema) \
        .option("header", "false") \
        .option("quotechar", '|') \
        .option("delimiter", ',') \
        .load(DATAP + '/dump/articles.csv')

    df.write.parquet(DATAP + '/dump/articles.parquet')


if __name__ == '__main__':
    convert()
